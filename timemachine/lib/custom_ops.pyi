import numpy

FIXED_EXPONENT: int

class BDExchangeMove_f32(Mover):
    def __init__(self, N: int, target_mols: list[list[int]], params: numpy.typing.NDArray[numpy.float64], temperature: float, nb_beta: float, cutoff: float, seed: int, num_proposals_per_move: int, interval: int, batch_size: int = ...) -> None: ...
    def acceptance_fraction(self) -> float: ...
    def batch_size(self) -> int: ...
    def compute_incremental_log_weights(self, coords: numpy.typing.NDArray[numpy.float64], box: numpy.typing.NDArray[numpy.float64], mol_idxs: numpy.typing.NDArray[numpy.int32], quaternions: numpy.typing.NDArray[numpy.float64], translation: numpy.typing.NDArray[numpy.float64]) -> list[list[float]]: ...
    def compute_initial_log_weights(self, coords: numpy.typing.NDArray[numpy.float64], box: numpy.typing.NDArray[numpy.float64]) -> list[float]: ...
    def get_after_log_weights(self) -> list[float]: ...
    def get_before_log_weights(self) -> list[float]: ...
    def get_params(self) -> numpy.typing.NDArray[numpy.float64]: ...
    def last_log_probability(self) -> float: ...
    def last_raw_log_probability(self) -> float: ...
    def move(self, coords: numpy.typing.NDArray[numpy.float64], box: numpy.typing.NDArray[numpy.float64]) -> tuple: ...
    def n_accepted(self) -> int: ...
    def n_proposed(self) -> int: ...
    def set_params(self, params: numpy.typing.NDArray[numpy.float64]) -> None: ...
    def __buffer__(self, *args, **kwargs): ...
    def __release_buffer__(self, *args, **kwargs): ...

class BDExchangeMove_f64(Mover):
    def __init__(self, N: int, target_mols: list[list[int]], params: numpy.typing.NDArray[numpy.float64], temperature: float, nb_beta: float, cutoff: float, seed: int, num_proposals_per_move: int, interval: int, batch_size: int = ...) -> None: ...
    def acceptance_fraction(self) -> float: ...
    def batch_size(self) -> int: ...
    def compute_incremental_log_weights(self, coords: numpy.typing.NDArray[numpy.float64], box: numpy.typing.NDArray[numpy.float64], mol_idxs: numpy.typing.NDArray[numpy.int32], quaternions: numpy.typing.NDArray[numpy.float64], translation: numpy.typing.NDArray[numpy.float64]) -> list[list[float]]: ...
    def compute_initial_log_weights(self, coords: numpy.typing.NDArray[numpy.float64], box: numpy.typing.NDArray[numpy.float64]) -> list[float]: ...
    def get_after_log_weights(self) -> list[float]: ...
    def get_before_log_weights(self) -> list[float]: ...
    def get_params(self) -> numpy.typing.NDArray[numpy.float64]: ...
    def last_log_probability(self) -> float: ...
    def last_raw_log_probability(self) -> float: ...
    def move(self, coords: numpy.typing.NDArray[numpy.float64], box: numpy.typing.NDArray[numpy.float64]) -> tuple: ...
    def n_accepted(self) -> int: ...
    def n_proposed(self) -> int: ...
    def set_params(self, params: numpy.typing.NDArray[numpy.float64]) -> None: ...
    def __buffer__(self, *args, **kwargs): ...
    def __release_buffer__(self, *args, **kwargs): ...

class BoundPotential:
    def __init__(self, potential: Potential, params: numpy.typing.NDArray[numpy.float64]) -> None: ...
    def execute(self, coords: numpy.typing.NDArray[numpy.float64], box: numpy.typing.NDArray[numpy.float64], compute_du_dx: bool = ..., compute_u: bool = ...) -> tuple: ...
    def execute_batch(self, coords: numpy.typing.NDArray[numpy.float64], boxes: numpy.typing.NDArray[numpy.float64], compute_du_dx: bool, compute_u: bool) -> tuple: ...
    def execute_fixed(self, coords: numpy.typing.NDArray[numpy.float64], box: numpy.typing.NDArray[numpy.float64]) -> numpy.typing.NDArray[numpy.uint64]: ...
    def get_potential(self) -> Potential: ...
    def set_params(self, params: numpy.typing.NDArray[numpy.float64]) -> None: ...
    def size(self) -> int: ...
    def __buffer__(self, *args, **kwargs): ...
    def __release_buffer__(self, *args, **kwargs): ...

class CentroidRestraint_f32(Potential):
    def __init__(self, group_a_idxs: numpy.typing.NDArray[numpy.int32], group_b_idxs: numpy.typing.NDArray[numpy.int32], kb: float, b0: float) -> None: ...
    def __buffer__(self, *args, **kwargs): ...
    def __release_buffer__(self, *args, **kwargs): ...

class CentroidRestraint_f64(Potential):
    def __init__(self, group_a_idxs: numpy.typing.NDArray[numpy.int32], group_b_idxs: numpy.typing.NDArray[numpy.int32], kb: float, b0: float) -> None: ...
    def __buffer__(self, *args, **kwargs): ...
    def __release_buffer__(self, *args, **kwargs): ...

class ChiralAtomRestraint_f32(Potential):
    def __init__(self, idxs: numpy.typing.NDArray[numpy.int32]) -> None: ...
    def __buffer__(self, *args, **kwargs): ...
    def __release_buffer__(self, *args, **kwargs): ...

class ChiralAtomRestraint_f64(Potential):
    def __init__(self, idxs: numpy.typing.NDArray[numpy.int32]) -> None: ...
    def __buffer__(self, *args, **kwargs): ...
    def __release_buffer__(self, *args, **kwargs): ...

class ChiralBondRestraint_f32(Potential):
    def __init__(self, idxs: numpy.typing.NDArray[numpy.int32], signs: numpy.typing.NDArray[numpy.int32]) -> None: ...
    def __buffer__(self, *args, **kwargs): ...
    def __release_buffer__(self, *args, **kwargs): ...

class ChiralBondRestraint_f64(Potential):
    def __init__(self, idxs: numpy.typing.NDArray[numpy.int32], signs: numpy.typing.NDArray[numpy.int32]) -> None: ...
    def __buffer__(self, *args, **kwargs): ...
    def __release_buffer__(self, *args, **kwargs): ...

class Context:
    def __init__(self, x0: numpy.typing.NDArray[numpy.float64], v0: numpy.typing.NDArray[numpy.float64], box: numpy.typing.NDArray[numpy.float64], integrator: Integrator, bps: list[BoundPotential], movers: list[Mover] | None = ...) -> None: ...
    def finalize(self) -> None: ...
    def get_barostat(self) -> MonteCarloBarostat: ...
    def get_box(self) -> numpy.typing.NDArray[numpy.float64]: ...
    def get_integrator(self) -> Integrator: ...
    def get_movers(self) -> list[Mover]: ...
    def get_potentials(self) -> list[BoundPotential]: ...
    def get_v_t(self) -> numpy.typing.NDArray[numpy.float64]: ...
    def get_x_t(self) -> numpy.typing.NDArray[numpy.float64]: ...
    def initialize(self) -> None: ...
    def multiple_steps(self, n_steps: int, store_x_interval: int = ...) -> tuple: ...
    def multiple_steps_local(self, n_steps: int, local_idxs: numpy.typing.NDArray[numpy.int32], store_x_interval: int = ..., radius: float = ..., k: float = ..., seed: int = ...) -> tuple: ...
    def multiple_steps_local_selection(self, n_steps: int, reference_idx: int, selection_idxs: numpy.typing.NDArray[numpy.int32], store_x_interval: int = ..., radius: float = ..., k: float = ...) -> tuple: ...
    def set_box(self, box: numpy.typing.NDArray[numpy.float64]) -> None: ...
    def set_v_t(self, velocities: numpy.typing.NDArray[numpy.float64]) -> None: ...
    def set_x_t(self, coords: numpy.typing.NDArray[numpy.float64]) -> None: ...
    def setup_local_md(self, temperature: float, freeze_reference: bool) -> None: ...
    def step(self) -> None: ...
    def __buffer__(self, *args, **kwargs): ...
    def __release_buffer__(self, *args, **kwargs): ...

class FanoutSummedPotential(Potential):
    def __init__(self, potentials: list[Potential], parallel: bool = ...) -> None: ...
    def get_potentials(self) -> list[Potential]: ...
    def __buffer__(self, *args, **kwargs): ...
    def __release_buffer__(self, *args, **kwargs): ...

class FlatBottomBond_f32(Potential):
    def __init__(self, bond_idxs: numpy.typing.NDArray[numpy.int32]) -> None: ...
    def __buffer__(self, *args, **kwargs): ...
    def __release_buffer__(self, *args, **kwargs): ...

class FlatBottomBond_f64(Potential):
    def __init__(self, bond_idxs: numpy.typing.NDArray[numpy.int32]) -> None: ...
    def __buffer__(self, *args, **kwargs): ...
    def __release_buffer__(self, *args, **kwargs): ...

class HarmonicAngle_f32(Potential):
    def __init__(self, angle_idxs: numpy.typing.NDArray[numpy.int32]) -> None: ...
    def __buffer__(self, *args, **kwargs): ...
    def __release_buffer__(self, *args, **kwargs): ...

class HarmonicAngle_f64(Potential):
    def __init__(self, angle_idxs: numpy.typing.NDArray[numpy.int32]) -> None: ...
    def __buffer__(self, *args, **kwargs): ...
    def __release_buffer__(self, *args, **kwargs): ...

class HarmonicBond_f32(Potential):
    def __init__(self, bond_idxs: numpy.typing.NDArray[numpy.int32]) -> None: ...
    def __buffer__(self, *args, **kwargs): ...
    def __release_buffer__(self, *args, **kwargs): ...

class HarmonicBond_f64(Potential):
    def __init__(self, bond_idxs: numpy.typing.NDArray[numpy.int32]) -> None: ...
    def __buffer__(self, *args, **kwargs): ...
    def __release_buffer__(self, *args, **kwargs): ...

class HilbertSort:
    def __init__(self, size: int) -> None: ...
    def sort(self, coords: numpy.typing.NDArray[numpy.float64], box: numpy.typing.NDArray[numpy.float64]) -> numpy.typing.NDArray[numpy.uint32]: ...
    def __buffer__(self, *args, **kwargs): ...
    def __release_buffer__(self, *args, **kwargs): ...

class Integrator:
    def __init__(self, *args, **kwargs) -> None: ...
    def __buffer__(self, *args, **kwargs): ...
    def __release_buffer__(self, *args, **kwargs): ...

class InvalidHardware(Exception): ...

class LangevinIntegrator(Integrator):
    def __init__(self, masses: numpy.typing.NDArray[numpy.float64], temperature: float, dt: float, friction: float, seed: int) -> None: ...
    def __buffer__(self, *args, **kwargs): ...
    def __release_buffer__(self, *args, **kwargs): ...

class LogFlatBottomBond_f32(Potential):
    def __init__(self, bond_idxs: numpy.typing.NDArray[numpy.int32], beta: float) -> None: ...
    def __buffer__(self, *args, **kwargs): ...
    def __release_buffer__(self, *args, **kwargs): ...

class LogFlatBottomBond_f64(Potential):
    def __init__(self, bond_idxs: numpy.typing.NDArray[numpy.int32], beta: float) -> None: ...
    def __buffer__(self, *args, **kwargs): ...
    def __release_buffer__(self, *args, **kwargs): ...

class MonteCarloBarostat(Mover):
    def __init__(self, N: int, pressure: float, temperature: float, group_idxs: list[list[int]], interval: int, bps, seed: int, adaptive_scaling_enabled: bool, initial_volume_scale_factor: float) -> None: ...
    def get_adaptive_scaling(self) -> bool: ...
    def get_volume_scale_factor(self) -> float: ...
    def set_adaptive_scaling(self, adaptive_scaling_enabled: bool) -> None: ...
    def set_pressure(self, pressure: float) -> None: ...
    def set_volume_scale_factor(self, volume_scale_factor: float) -> None: ...
    def __buffer__(self, *args, **kwargs): ...
    def __release_buffer__(self, *args, **kwargs): ...

class Mover:
    def __init__(self, *args, **kwargs) -> None: ...
    def get_interval(self) -> int: ...
    def move(self, coords: numpy.typing.NDArray[numpy.float64], box: numpy.typing.NDArray[numpy.float64]) -> tuple: ...
    def set_interval(self, interval: int) -> None: ...
    def set_step(self, step: int) -> None: ...
    def __buffer__(self, *args, **kwargs): ...
    def __release_buffer__(self, *args, **kwargs): ...

class Neighborlist_f32:
    def __init__(self, N: int) -> None: ...
    def compute_block_bounds(self, coords: numpy.typing.NDArray[numpy.float64], box: numpy.typing.NDArray[numpy.float64], block_size: int) -> tuple: ...
    def get_max_ixn_count(self) -> int: ...
    def get_nblist(self, coords: numpy.typing.NDArray[numpy.float64], box: numpy.typing.NDArray[numpy.float64], cutoff: float) -> list[list[int]]: ...
    def get_num_row_idxs(self) -> int: ...
    def get_tile_ixn_count(self) -> int: ...
    def reset_row_idxs(self) -> None: ...
    def resize(self, size: int) -> None: ...
    def set_row_idxs(self, idxs: numpy.typing.NDArray[numpy.uint32]) -> None: ...
    def __buffer__(self, *args, **kwargs): ...
    def __release_buffer__(self, *args, **kwargs): ...

class Neighborlist_f64:
    def __init__(self, N: int) -> None: ...
    def compute_block_bounds(self, coords: numpy.typing.NDArray[numpy.float64], box: numpy.typing.NDArray[numpy.float64], block_size: int) -> tuple: ...
    def get_max_ixn_count(self) -> int: ...
    def get_nblist(self, coords: numpy.typing.NDArray[numpy.float64], box: numpy.typing.NDArray[numpy.float64], cutoff: float) -> list[list[int]]: ...
    def get_num_row_idxs(self) -> int: ...
    def get_tile_ixn_count(self) -> int: ...
    def reset_row_idxs(self) -> None: ...
    def resize(self, size: int) -> None: ...
    def set_row_idxs(self, idxs: numpy.typing.NDArray[numpy.uint32]) -> None: ...
    def __buffer__(self, *args, **kwargs): ...
    def __release_buffer__(self, *args, **kwargs): ...

class NonbondedAllPairs_f32(Potential):
    def __init__(self, num_atoms: int, beta: float, cutoff: float, atom_idxs_i: numpy.typing.NDArray[numpy.int32] | None = ..., disable_hilbert_sort: bool = ..., nblist_padding: float = ...) -> None: ...
    def get_atom_idxs(self) -> list[int]: ...
    def get_num_atom_idxs(self) -> int: ...
    def set_atom_idxs(self, atom_idxs: list[int]) -> None: ...
    def __buffer__(self, *args, **kwargs): ...
    def __release_buffer__(self, *args, **kwargs): ...

class NonbondedAllPairs_f64(Potential):
    def __init__(self, num_atoms: int, beta: float, cutoff: float, atom_idxs_i: numpy.typing.NDArray[numpy.int32] | None = ..., disable_hilbert_sort: bool = ..., nblist_padding: float = ...) -> None: ...
    def get_atom_idxs(self) -> list[int]: ...
    def get_num_atom_idxs(self) -> int: ...
    def set_atom_idxs(self, atom_idxs: list[int]) -> None: ...
    def __buffer__(self, *args, **kwargs): ...
    def __release_buffer__(self, *args, **kwargs): ...

class NonbondedExclusions_f32(Potential):
    def __init__(self, pair_idxs_i: numpy.typing.NDArray[numpy.int32], scales_i: numpy.typing.NDArray[numpy.float64], beta: float, cutoff: float) -> None: ...
    def __buffer__(self, *args, **kwargs): ...
    def __release_buffer__(self, *args, **kwargs): ...

class NonbondedExclusions_f64(Potential):
    def __init__(self, pair_idxs_i: numpy.typing.NDArray[numpy.int32], scales_i: numpy.typing.NDArray[numpy.float64], beta: float, cutoff: float) -> None: ...
    def __buffer__(self, *args, **kwargs): ...
    def __release_buffer__(self, *args, **kwargs): ...

class NonbondedInteractionGroup_f32(Potential):
    def __init__(self, num_atoms: int, row_atom_idxs_i: numpy.typing.NDArray[numpy.int32], beta: float, cutoff: float, col_atom_idxs_i: numpy.typing.NDArray[numpy.int32] | None = ..., disable_hilbert_sort: bool = ..., nblist_padding: float = ...) -> None: ...
    def set_atom_idxs(self, row_atom_idxs: list[int], col_atom_idxs: list[int]) -> None: ...
    def __buffer__(self, *args, **kwargs): ...
    def __release_buffer__(self, *args, **kwargs): ...

class NonbondedInteractionGroup_f64(Potential):
    def __init__(self, num_atoms: int, row_atom_idxs_i: numpy.typing.NDArray[numpy.int32], beta: float, cutoff: float, col_atom_idxs_i: numpy.typing.NDArray[numpy.int32] | None = ..., disable_hilbert_sort: bool = ..., nblist_padding: float = ...) -> None: ...
    def set_atom_idxs(self, row_atom_idxs: list[int], col_atom_idxs: list[int]) -> None: ...
    def __buffer__(self, *args, **kwargs): ...
    def __release_buffer__(self, *args, **kwargs): ...

class NonbondedMolEnergyPotential_f32:
    def __init__(self, N: int, target_mols: list[list[int]], beta: float, cutoff: float) -> None: ...
    def execute(self, coords: numpy.typing.NDArray[numpy.float64], params: numpy.typing.NDArray[numpy.float64], box: numpy.typing.NDArray[numpy.float64]) -> numpy.typing.NDArray[numpy.float64]: ...
    def __buffer__(self, *args, **kwargs): ...
    def __release_buffer__(self, *args, **kwargs): ...

class NonbondedMolEnergyPotential_f64:
    def __init__(self, N: int, target_mols: list[list[int]], beta: float, cutoff: float) -> None: ...
    def execute(self, coords: numpy.typing.NDArray[numpy.float64], params: numpy.typing.NDArray[numpy.float64], box: numpy.typing.NDArray[numpy.float64]) -> numpy.typing.NDArray[numpy.float64]: ...
    def __buffer__(self, *args, **kwargs): ...
    def __release_buffer__(self, *args, **kwargs): ...

class NonbondedPairListPrecomputed_f32(Potential):
    def __init__(self, pair_idxs: numpy.typing.NDArray[numpy.int32], beta: float, cutoff: float) -> None: ...
    def __buffer__(self, *args, **kwargs): ...
    def __release_buffer__(self, *args, **kwargs): ...

class NonbondedPairListPrecomputed_f64(Potential):
    def __init__(self, pair_idxs: numpy.typing.NDArray[numpy.int32], beta: float, cutoff: float) -> None: ...
    def __buffer__(self, *args, **kwargs): ...
    def __release_buffer__(self, *args, **kwargs): ...

class NonbondedPairList_f32(Potential):
    def __init__(self, pair_idxs_i: numpy.typing.NDArray[numpy.int32], scales_i: numpy.typing.NDArray[numpy.float64], beta: float, cutoff: float) -> None: ...
    def __buffer__(self, *args, **kwargs): ...
    def __release_buffer__(self, *args, **kwargs): ...

class NonbondedPairList_f64(Potential):
    def __init__(self, pair_idxs_i: numpy.typing.NDArray[numpy.int32], scales_i: numpy.typing.NDArray[numpy.float64], beta: float, cutoff: float) -> None: ...
    def __buffer__(self, *args, **kwargs): ...
    def __release_buffer__(self, *args, **kwargs): ...

class PeriodicTorsion_f32(Potential):
    def __init__(self, angle_idxs: numpy.typing.NDArray[numpy.int32]) -> None: ...
    def __buffer__(self, *args, **kwargs): ...
    def __release_buffer__(self, *args, **kwargs): ...

class PeriodicTorsion_f64(Potential):
    def __init__(self, angle_idxs: numpy.typing.NDArray[numpy.int32]) -> None: ...
    def __buffer__(self, *args, **kwargs): ...
    def __release_buffer__(self, *args, **kwargs): ...

class Potential:
    def __init__(self, *args, **kwargs) -> None: ...
    def execute(self, coords: numpy.typing.NDArray[numpy.float64], params: numpy.typing.NDArray[numpy.float64], box: numpy.typing.NDArray[numpy.float64], compute_du_dx: bool = ..., compute_du_dp: bool = ..., compute_u: bool = ...) -> tuple: ...
    def execute_batch(self, coords: numpy.typing.NDArray[numpy.float64], params: numpy.typing.NDArray[numpy.float64], boxes: numpy.typing.NDArray[numpy.float64], compute_du_dx: bool, compute_du_dp: bool, compute_u: bool) -> tuple: ...
    def execute_batch_sparse(self, coords: numpy.typing.NDArray[numpy.float64], params: numpy.typing.NDArray[numpy.float64], boxes: numpy.typing.NDArray[numpy.float64], coords_batch_idxs: numpy.typing.NDArray[numpy.uint32], params_batch_idxs: numpy.typing.NDArray[numpy.uint32], compute_du_dx: bool, compute_du_dp: bool, compute_u: bool) -> tuple: ...
    def execute_du_dx(self, coords: numpy.typing.NDArray[numpy.float64], params: numpy.typing.NDArray[numpy.float64], box: numpy.typing.NDArray[numpy.float64]) -> numpy.typing.NDArray[numpy.float64]: ...
    def __buffer__(self, *args, **kwargs): ...
    def __release_buffer__(self, *args, **kwargs): ...

class SegmentedSumExp_f32:
    def __init__(self, max_vals_per_segment: int, num_segments: int) -> None: ...
    def logsumexp(self, values: list[list[float]]) -> list[float]: ...
    def __buffer__(self, *args, **kwargs): ...
    def __release_buffer__(self, *args, **kwargs): ...

class SegmentedSumExp_f64:
    def __init__(self, max_vals_per_segment: int, num_segments: int) -> None: ...
    def logsumexp(self, values: list[list[float]]) -> list[float]: ...
    def __buffer__(self, *args, **kwargs): ...
    def __release_buffer__(self, *args, **kwargs): ...

class SegmentedWeightedRandomSampler_f32:
    def __init__(self, max_vals_per_segment: int, segments: int, seed: int) -> None: ...
    def sample(self, weights: list[list[float]]) -> list[int]: ...
    def __buffer__(self, *args, **kwargs): ...
    def __release_buffer__(self, *args, **kwargs): ...

class SegmentedWeightedRandomSampler_f64:
    def __init__(self, max_vals_per_segment: int, segments: int, seed: int) -> None: ...
    def sample(self, weights: list[list[float]]) -> list[int]: ...
    def __buffer__(self, *args, **kwargs): ...
    def __release_buffer__(self, *args, **kwargs): ...

class SummedPotential(Potential):
    def __init__(self, potentials: list[Potential], params_sizes: list[int], parallel: bool = ...) -> None: ...
    def get_potentials(self) -> list[Potential]: ...
    def __buffer__(self, *args, **kwargs): ...
    def __release_buffer__(self, *args, **kwargs): ...

class TIBDExchangeMove_f32(BDExchangeMove_f32):
    def __init__(self, N: int, ligand_idxs: list[int], target_mols: list[list[int]], params: numpy.typing.NDArray[numpy.float64], temperature: float, nb_beta: float, cutoff: float, radius: float, seed: int, num_proposals_per_move: int, interval: int, batch_size: int = ...) -> None: ...
    def __buffer__(self, *args, **kwargs): ...
    def __release_buffer__(self, *args, **kwargs): ...

class TIBDExchangeMove_f64(BDExchangeMove_f64):
    def __init__(self, N: int, ligand_idxs: list[int], target_mols: list[list[int]], params: numpy.typing.NDArray[numpy.float64], temperature: float, nb_beta: float, cutoff: float, radius: float, seed: int, num_proposals_per_move: int, interval: int, batch_size: int = ...) -> None: ...
    def __buffer__(self, *args, **kwargs): ...
    def __release_buffer__(self, *args, **kwargs): ...

class VelocityVerletIntegrator(Integrator):
    def __init__(self, dt: float, cbs: numpy.typing.NDArray[numpy.float64]) -> None: ...
    def __buffer__(self, *args, **kwargs): ...
    def __release_buffer__(self, *args, **kwargs): ...

def atom_by_atom_energies_f32(target_atoms: numpy.typing.NDArray[numpy.int32], coords: numpy.typing.NDArray[numpy.float64], params: numpy.typing.NDArray[numpy.float64], box: numpy.typing.NDArray[numpy.float64], nb_beta: float, nb_cutoff: float) -> numpy.typing.NDArray[numpy.float32]: ...
def atom_by_atom_energies_f64(target_atoms: numpy.typing.NDArray[numpy.int32], coords: numpy.typing.NDArray[numpy.float64], params: numpy.typing.NDArray[numpy.float64], box: numpy.typing.NDArray[numpy.float64], nb_beta: float, nb_cutoff: float) -> numpy.typing.NDArray[numpy.float64]: ...
def cuda_device_reset() -> None: ...
def inner_and_outer_mols_f32(center_atoms: numpy.typing.NDArray[numpy.int32], coords: numpy.typing.NDArray[numpy.float64], box: numpy.typing.NDArray[numpy.float64], group_idxs: list[list[int]], radius: float) -> tuple: ...
def inner_and_outer_mols_f64(center_atoms: numpy.typing.NDArray[numpy.int32], coords: numpy.typing.NDArray[numpy.float64], box: numpy.typing.NDArray[numpy.float64], group_idxs: list[list[int]], radius: float) -> tuple: ...
def rmsd_align(x1: numpy.typing.NDArray[numpy.float64], x2: numpy.typing.NDArray[numpy.float64]) -> numpy.typing.NDArray[numpy.float64]: ...
def rotate_and_translate_mol_f32(coords: numpy.typing.NDArray[numpy.float64], box: numpy.typing.NDArray[numpy.float64], quaternion: numpy.typing.NDArray[numpy.float64], translation: numpy.typing.NDArray[numpy.float64]) -> numpy.typing.NDArray[numpy.float64]: ...
def rotate_and_translate_mol_f64(coords: numpy.typing.NDArray[numpy.float64], box: numpy.typing.NDArray[numpy.float64], quaternion: numpy.typing.NDArray[numpy.float64], translation: numpy.typing.NDArray[numpy.float64]) -> numpy.typing.NDArray[numpy.float64]: ...
def rotate_coords_f32(coords: numpy.typing.NDArray[numpy.float64], quaternions: numpy.typing.NDArray[numpy.float64]) -> numpy.typing.NDArray[numpy.float64]: ...
def rotate_coords_f64(coords: numpy.typing.NDArray[numpy.float64], quaternions: numpy.typing.NDArray[numpy.float64]) -> numpy.typing.NDArray[numpy.float64]: ...
def translations_inside_and_outside_sphere_host_f32(num_translations: int, box: numpy.typing.NDArray[numpy.float64], center: numpy.typing.NDArray[numpy.float64], radius: float, seed: int) -> numpy.typing.NDArray[numpy.float32]: ...
def translations_inside_and_outside_sphere_host_f64(num_translations: int, box: numpy.typing.NDArray[numpy.float64], center: numpy.typing.NDArray[numpy.float64], radius: float, seed: int) -> numpy.typing.NDArray[numpy.float64]: ...
