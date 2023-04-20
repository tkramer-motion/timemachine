#include "constants.hpp"
#include "context.hpp"

#include "fixed_point.hpp"
#include "flat_bottom_bond.hpp"
#include "gpu_utils.cuh"
#include "kernels/kernel_utils.cuh"
#include "langevin_integrator.hpp"
#include "local_md_potentials.hpp"
#include "math_utils.cuh"
#include "pinned_host_buffer.hpp"
#include "set_utils.hpp"
#include <cub/cub.cuh>
#include <memory>

namespace timemachine {

Context::Context(
    int N,
    const double *x_0,
    const double *v_0,
    const double *box_0,
    std::shared_ptr<Integrator> intg,
    std::vector<std::shared_ptr<BoundPotential>> bps,
    std::shared_ptr<MonteCarloBarostat> barostat)
    : N_(N), barostat_(barostat), step_(0), d_sum_storage_(nullptr), d_sum_storage_bytes_(0), intg_(intg), bps_(bps) {
    d_x_t_ = gpuErrchkCudaMallocAndCopy(x_0, N * 3);
    d_v_t_ = gpuErrchkCudaMallocAndCopy(v_0, N * 3);
    d_box_t_ = gpuErrchkCudaMallocAndCopy(box_0, 3 * 3);
    cudaSafeMalloc(&d_u_buffer_, N * sizeof(*d_u_buffer_));

    unsigned long long *d_in_tmp = nullptr;  // dummy
    unsigned long long *d_out_tmp = nullptr; // dummy

    // Compute the storage size necessary to reduce energies
    cub::DeviceReduce::Sum(d_sum_storage_, d_sum_storage_bytes_, d_in_tmp, d_out_tmp, N_);
    gpuErrchk(cudaPeekAtLastError());
    cudaSafeMalloc(&d_sum_storage_, d_sum_storage_bytes_);
};

Context::~Context() {
    gpuErrchk(cudaFree(d_x_t_));
    gpuErrchk(cudaFree(d_v_t_));
    gpuErrchk(cudaFree(d_box_t_));
    gpuErrchk(cudaFree(d_u_buffer_));
    gpuErrchk(cudaFree(d_sum_storage_));
};

double Context::_get_temperature() {
    if (std::shared_ptr<LangevinIntegrator> langevin = std::dynamic_pointer_cast<LangevinIntegrator>(intg_);
        langevin != nullptr) {
        return langevin->get_temperature();
    } else {
        throw std::runtime_error("integrator must be LangevinIntegrator.");
    }
}

void Context::ensure_local_md_intialized() {
    if (this->local_md_pots_ == nullptr) {
        this->local_md_pots_.reset(new LocalMDPotentials(N_, bps_));
    }
}

std::array<std::vector<double>, 2> Context::multiple_steps_local(
    const int n_steps,
    const std::vector<int> &local_idxs,
    const int burn_in,
    const int store_x_interval,
    const double radius,
    const double k,
    const int seed) {
    if (store_x_interval <= 0) {
        throw std::runtime_error("store_x_interval <= 0");
    }

    const int x_buffer_size = n_steps / store_x_interval;

    const int box_buffer_size = x_buffer_size * 3 * 3;

    // Store coordinates in host memory as it can be very large
    std::vector<double> h_x_buffer(x_buffer_size * N_ * 3);
    // Store boxes on GPU as boxes are a constant size and relatively small
    std::unique_ptr<DeviceBuffer<double>> d_box_traj(nullptr);
    if (box_buffer_size > 0) {
        d_box_traj.reset(new DeviceBuffer<double>(box_buffer_size));
    }

    this->ensure_local_md_intialized();

    cudaStream_t stream;

    // Create stream that doesn't sync with the default stream
    gpuErrchk(cudaStreamCreateWithFlags(&stream, cudaStreamNonBlocking));
    try {

        local_md_pots_->setup_from_idxs(
            d_x_t_, d_box_t_, local_idxs, this->_get_temperature(), seed, radius, k, stream);

        unsigned int *d_free_idxs = local_md_pots_->get_free_idxs();

        std::vector<std::shared_ptr<BoundPotential>> local_pots = local_md_pots_->get_potentials();

        intg_->initialize(local_pots, d_x_t_, d_v_t_, d_box_t_, d_free_idxs, stream);
        for (int i = 0; i < burn_in; i++) {
            this->_step(local_pots, d_free_idxs, stream);
        }
        for (int i = 1; i <= n_steps; i++) {
            this->_step(local_pots, d_free_idxs, stream);
            if (i % store_x_interval == 0) {
                gpuErrchk(cudaMemcpyAsync(
                    &h_x_buffer[0] + ((i / store_x_interval) - 1) * N_ * 3,
                    d_x_t_,
                    N_ * 3 * sizeof(double),
                    cudaMemcpyDeviceToHost,
                    stream));
                gpuErrchk(cudaMemcpyAsync(
                    &d_box_traj->data[0] + ((i / store_x_interval) - 1) * 3 * 3,
                    d_box_t_,
                    3 * 3 * sizeof(*d_box_traj->data),
                    cudaMemcpyDeviceToDevice,
                    stream));
            }
        }
        intg_->finalize(local_pots, d_x_t_, d_v_t_, d_box_t_, d_free_idxs, stream);
        local_md_pots_->reset_potentials(stream);
    } catch (...) {
        gpuErrchk(cudaStreamSynchronize(stream));
        gpuErrchk(cudaStreamDestroy(stream));
        throw;
    }
    gpuErrchk(cudaStreamSynchronize(stream));
    gpuErrchk(cudaStreamDestroy(stream));

    std::vector<double> h_box_buffer(box_buffer_size);

    if (box_buffer_size > 0) {
        d_box_traj->copy_to(&h_box_buffer[0]);
    }
    return std::array<std::vector<double>, 2>({h_x_buffer, h_box_buffer});
}

std::array<std::vector<double>, 2> Context::multiple_steps_local_selection(
    const int n_steps,
    const int reference_idx,
    const std::vector<int> &selection_idxs,
    const int burn_in,
    const int store_x_interval,
    const double radius,
    const double k) {
    if (store_x_interval <= 0) {
        throw std::runtime_error("store_x_interval <= 0");
    }

    const int x_buffer_size = n_steps / store_x_interval;

    const int box_buffer_size = x_buffer_size * 3 * 3;

    // Store coordinates in host memory as it can be very large
    std::vector<double> h_x_buffer(x_buffer_size * N_ * 3);
    // Store boxes on GPU as boxes are a constant size and relatively small
    std::unique_ptr<DeviceBuffer<double>> d_box_traj(nullptr);
    if (box_buffer_size > 0) {
        d_box_traj.reset(new DeviceBuffer<double>(box_buffer_size));
    }

    this->ensure_local_md_intialized();

    cudaStream_t stream;

    // Create stream that doesn't sync with the default stream
    gpuErrchk(cudaStreamCreateWithFlags(&stream, cudaStreamNonBlocking));
    try {

        local_md_pots_->setup_from_idxs(reference_idx, selection_idxs, radius, k, stream);

        unsigned int *d_free_idxs = local_md_pots_->get_free_idxs();

        std::vector<std::shared_ptr<BoundPotential>> local_pots = local_md_pots_->get_potentials();

        intg_->initialize(local_pots, d_x_t_, d_v_t_, d_box_t_, d_free_idxs, stream);
        for (int i = 0; i < burn_in; i++) {
            this->_step(local_pots, d_free_idxs, stream);
        }
        for (int i = 1; i <= n_steps; i++) {
            this->_step(local_pots, d_free_idxs, stream);
            if (i % store_x_interval == 0) {
                gpuErrchk(cudaMemcpyAsync(
                    &h_x_buffer[0] + ((i / store_x_interval) - 1) * N_ * 3,
                    d_x_t_,
                    N_ * 3 * sizeof(double),
                    cudaMemcpyDeviceToHost,
                    stream));
                gpuErrchk(cudaMemcpyAsync(
                    &d_box_traj->data[0] + ((i / store_x_interval) - 1) * 3 * 3,
                    d_box_t_,
                    3 * 3 * sizeof(*d_box_traj->data),
                    cudaMemcpyDeviceToDevice,
                    stream));
            }
        }
        intg_->finalize(local_pots, d_x_t_, d_v_t_, d_box_t_, d_free_idxs, stream);
        local_md_pots_->reset_potentials(stream);
    } catch (...) {
        gpuErrchk(cudaStreamSynchronize(stream));
        gpuErrchk(cudaStreamDestroy(stream));
        throw;
    }
    gpuErrchk(cudaStreamSynchronize(stream));
    gpuErrchk(cudaStreamDestroy(stream));

    std::vector<double> h_box_buffer(box_buffer_size);

    if (box_buffer_size > 0) {
        d_box_traj->copy_to(&h_box_buffer[0]);
    }
    return std::array<std::vector<double>, 2>({h_x_buffer, h_box_buffer});
}

std::array<std::vector<double>, 2> Context::multiple_steps(const int n_steps, int store_x_interval) {
    if (store_x_interval <= 0) {
        throw std::runtime_error("store_x_interval <= 0");
    }
    if (n_steps % store_x_interval != 0) {
        std::cout << "warning:: n_steps modulo store_x_interval does not equal zero" << std::endl;
    }

    int x_buffer_size = n_steps / store_x_interval;
    int box_buffer_size = x_buffer_size * 3 * 3;

    std::vector<double> h_x_buffer(x_buffer_size * N_ * 3);

    cudaStream_t stream = static_cast<cudaStream_t>(0);

    std::unique_ptr<DeviceBuffer<double>> d_box_buffer(nullptr);
    if (box_buffer_size > 0) {
        d_box_buffer.reset(new DeviceBuffer<double>(box_buffer_size));
    }

    intg_->initialize(bps_, d_x_t_, d_v_t_, d_box_t_, nullptr, stream);
    for (int i = 1; i <= n_steps; i++) {
        this->_step(bps_, nullptr, stream);

        if (i % store_x_interval == 0) {
            gpuErrchk(cudaMemcpyAsync(
                &h_x_buffer[0] + ((i / store_x_interval) - 1) * N_ * 3,
                d_x_t_,
                N_ * 3 * sizeof(double),
                cudaMemcpyDeviceToHost,
                stream));
            gpuErrchk(cudaMemcpyAsync(
                &d_box_buffer->data[0] + ((i / store_x_interval) - 1) * 3 * 3,
                d_box_t_,
                3 * 3 * sizeof(*d_box_buffer->data),
                cudaMemcpyDeviceToDevice,
                stream));
        }
    }
    intg_->finalize(bps_, d_x_t_, d_v_t_, d_box_t_, nullptr, stream);

    gpuErrchk(cudaStreamSynchronize(stream));

    std::vector<double> h_box_buffer(box_buffer_size);
    if (box_buffer_size > 0) {
        d_box_buffer->copy_to(&h_box_buffer[0]);
    }

    return std::array<std::vector<double>, 2>({h_x_buffer, h_box_buffer});
}

std::array<std::vector<double>, 3>
Context::multiple_steps_U(const int n_steps, int store_u_interval, int store_x_interval) {

    if (store_u_interval <= 0) {
        throw std::runtime_error("store_u_interval <= 0");
    }

    if (store_x_interval <= 0) {
        throw std::runtime_error("store_x_interval <= 0");
    }

    if (n_steps % store_x_interval != 0) {
        std::cout << "warning:: n_steps modulo store_x_interval does not equal zero" << std::endl;
    }

    if (n_steps % store_u_interval != 0) {
        std::cout << "warning:: n_steps modulo store_u_interval does not equal zero" << std::endl;
    }

    int u_traj_size = n_steps / store_u_interval;
    int x_traj_size = n_steps / store_x_interval;

    std::vector<double> h_x_traj(x_traj_size * N_ * 3);

    cudaStream_t stream = static_cast<cudaStream_t>(0);

    std::unique_ptr<DeviceBuffer<double>> d_box_traj(nullptr);
    if (x_traj_size > 0) {
        d_box_traj.reset(new DeviceBuffer<double>(x_traj_size * 3 * 3));
    }
    std::unique_ptr<DeviceBuffer<unsigned long long>> d_u_traj(nullptr);
    if (u_traj_size > 0) {
        d_u_traj.reset(new DeviceBuffer<unsigned long long>(u_traj_size));
        gpuErrchk(cudaMemsetAsync(d_u_traj->data, 0, d_u_traj->size, stream));
    }

    intg_->initialize(bps_, d_x_t_, d_v_t_, d_box_t_, nullptr, stream);
    for (int step = 1; step <= n_steps; step++) {

        this->_step(bps_, nullptr, stream);

        if (step % store_x_interval == 0) {
            gpuErrchk(cudaMemcpyAsync(
                &h_x_traj[0] + ((step / store_x_interval) - 1) * N_ * 3,
                d_x_t_,
                N_ * 3 * sizeof(double),
                cudaMemcpyDeviceToHost,
                stream));
            gpuErrchk(cudaMemcpyAsync(
                &d_box_traj->data[0] + ((step / store_x_interval) - 1) * 3 * 3,
                d_box_t_,
                3 * 3 * sizeof(*d_box_traj->data),
                cudaMemcpyDeviceToDevice,
                stream));
        }

        // we need to compute aggregate energies
        if (u_traj_size > 0 && step % store_u_interval == 0) {
            // reset buffers on each pass.
            gpuErrchk(cudaMemsetAsync(d_u_buffer_, 0, N_ * sizeof(*d_u_buffer_), stream));
            unsigned long long *u_ptr = d_u_traj->data + (step / store_u_interval) - 1;
            for (int i = 0; i < bps_.size(); i++) {
                bps_[i]->execute_device(N_, d_x_t_, d_box_t_, nullptr, nullptr, d_u_buffer_, stream);
            }
            cub::DeviceReduce::Sum(d_sum_storage_, d_sum_storage_bytes_, d_u_buffer_, u_ptr, N_, stream);
            gpuErrchk(cudaPeekAtLastError());
        }
    }
    intg_->finalize(bps_, d_x_t_, d_v_t_, d_box_t_, nullptr, stream);

    gpuErrchk(cudaStreamSynchronize(stream));

    std::vector<unsigned long long> h_u_traj_ull(u_traj_size);
    if (u_traj_size > 0) {
        d_u_traj->copy_to(&h_u_traj_ull[0]);
    }

    std::vector<double> h_u_traj_double(u_traj_size);
    for (int i = 0; i < h_u_traj_ull.size(); i++) {
        h_u_traj_double[i] = FIXED_TO_FLOAT<double>(h_u_traj_ull[i]);
    }
    std::vector<double> h_box_traj(x_traj_size * 3 * 3);
    if (x_traj_size > 0) {
        d_box_traj->copy_to(&h_box_traj[0]);
    }

    return std::array<std::vector<double>, 3>({h_u_traj_double, h_x_traj, h_box_traj});
}

void Context::step() {
    cudaStream_t stream = static_cast<cudaStream_t>(0);
    this->_step(bps_, nullptr, stream);
    gpuErrchk(cudaStreamSynchronize(stream));
}

void Context::finalize() {
    cudaStream_t stream = static_cast<cudaStream_t>(0);
    intg_->finalize(bps_, d_x_t_, d_v_t_, d_box_t_, nullptr, stream);
    gpuErrchk(cudaStreamSynchronize(stream));
}

void Context::initialize() {
    cudaStream_t stream = static_cast<cudaStream_t>(0);
    intg_->initialize(bps_, d_x_t_, d_v_t_, d_box_t_, nullptr, stream);
    gpuErrchk(cudaStreamSynchronize(stream));
}

void Context::_step(
    std::vector<std::shared_ptr<BoundPotential>> &bps, unsigned int *d_atom_idxs, const cudaStream_t stream) {
    intg_->step_fwd(bps, d_x_t_, d_v_t_, d_box_t_, d_atom_idxs, stream);

    // If atom idxs are passed, indicates that only a subset of the system should move. Don't
    // run the barostat in this situation.
    if (d_atom_idxs == nullptr && barostat_) {
        // May modify coords, du_dx and box size
        barostat_->inplace_move(d_x_t_, d_box_t_, stream);
    }

    step_ += 1;
};

int Context::num_atoms() const { return N_; }

void Context::set_x_t(const double *in_buffer) {
    gpuErrchk(cudaMemcpy(d_x_t_, in_buffer, N_ * 3 * sizeof(*in_buffer), cudaMemcpyHostToDevice));
}

void Context::set_v_t(const double *in_buffer) {
    gpuErrchk(cudaMemcpy(d_v_t_, in_buffer, N_ * 3 * sizeof(*in_buffer), cudaMemcpyHostToDevice));
}

void Context::set_box(const double *in_buffer) {
    gpuErrchk(cudaMemcpy(d_box_t_, in_buffer, 3 * 3 * sizeof(*in_buffer), cudaMemcpyHostToDevice));
}

void Context::get_x_t(double *out_buffer) const {
    gpuErrchk(cudaMemcpy(out_buffer, d_x_t_, N_ * 3 * sizeof(*out_buffer), cudaMemcpyDeviceToHost));
}

void Context::get_v_t(double *out_buffer) const {
    gpuErrchk(cudaMemcpy(out_buffer, d_v_t_, N_ * 3 * sizeof(*out_buffer), cudaMemcpyDeviceToHost));
}

void Context::get_box(double *out_buffer) const {
    gpuErrchk(cudaMemcpy(out_buffer, d_box_t_, 3 * 3 * sizeof(*out_buffer), cudaMemcpyDeviceToHost));
}

} // namespace timemachine
