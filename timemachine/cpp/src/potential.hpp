#pragma once

#include <cuda_runtime.h>

namespace timemachine {

// *Not* guaranteed to be thread-safe.
class Potential {

public:
    virtual ~Potential() {};

    static const int D;

    void execute_batch_host(
        const int coord_batch_size,
        const int N,
        const int param_batch_size,
        const int P,
        const double *h_x,
        const double *h_p,
        const double *h_box,
        unsigned long long *h_du_dx,
        unsigned long long *h_du_dp,
        __int128 *h_u);

    void execute_batch_sparse_host(
        const int coords_size,
        const int N,
        const int params_size,
        const int P,
        const int batch_size,
        const unsigned int *coords_batch_idxs,
        const unsigned int *params_batch_idxs,
        const double *h_x,
        const double *h_p,
        const double *h_box,
        unsigned long long *h_du_dx,
        unsigned long long *h_du_dp,
        __int128 *h_u);

    void execute_host(
        const int N,
        const int P,
        const double *h_x,
        const double *h_p,
        const double *h_box,
        unsigned long long *h_du_dx,
        unsigned long long *h_du_dp,
        __int128 *h_u);

    void execute_host_du_dx(
        const int N,
        const int P,
        const double *h_x,
        const double *h_p,
        const double *h_box,
        unsigned long long *h_du_dx);

    void execute_batch_device(
        const int coord_batch_size,
        const int N,
        const int param_batch_size,
        const int P,
        const double *d_x,
        const double *d_p,
        const double *d_box,
        unsigned long long *d_du_dx,
        unsigned long long *d_du_dp,
        __int128 *d_u,
        cudaStream_t stream);

    void execute_batch_sparse_device(
        const int N,
        const int P,
        const int batch_size,
        const unsigned int *coords_batch_idxs,
        const unsigned int *params_batch_idxs,
        const double *d_x,
        const double *d_p,
        const double *d_box,
        unsigned long long *d_du_dx,
        unsigned long long *d_du_dp,
        __int128 *d_u,
        cudaStream_t stream);

    virtual void execute_device(
        const int N,
        const int P,
        const double *d_x,
        const double *d_p,
        const double *d_box,
        unsigned long long *d_du_dx,
        unsigned long long *d_du_dp,
        __int128 *h_u,
        cudaStream_t stream) = 0;

    virtual void du_dp_fixed_to_float(const int N, const int P, const unsigned long long *du_dp, double *du_dp_float);
};

} // namespace timemachine
