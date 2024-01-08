from typing import List, Optional

import numpy
FIXED_EXPONENT: int

class BDExchangeMove_f32(Mover):
    def __init__(self, N: int, target_mols: List[List[int]], params: numpy.typing.NDArray[numpy.float64], temperature: float, nb_beta: float, cutoff: float, seed: int, proposals_per_move: int, interval: int) -> None: ...
    def acceptance_fraction(self) -> float: ...
    def get_params(self) -> numpy.typing.NDArray[numpy.float64]: ...
    def last_log_probability(self) -> float: ...
    def last_raw_log_probability(self) -> float: ...
    def move(self, coords: numpy.typing.NDArray[numpy.float64], box: numpy.typing.NDArray[numpy.float64]) -> tuple: ...
    def n_accepted(self) -> int: ...
    def n_proposed(self) -> int: ...
    def set_params(self, params: numpy.typing.NDArray[numpy.float64]) -> None: ...

class BDExchangeMove_f64(Mover):
    def __init__(self, N: int, target_mols: List[List[int]], params: numpy.typing.NDArray[numpy.float64], temperature: float, nb_beta: float, cutoff: float, seed: int, proposals_per_move: int, interval: int) -> None: ...
    def acceptance_fraction(self) -> float: ...
    def get_params(self) -> numpy.typing.NDArray[numpy.float64]: ...
    def last_log_probability(self) -> float: ...
    def last_raw_log_probability(self) -> float: ...
    def move(self, coords: numpy.typing.NDArray[numpy.float64], box: numpy.typing.NDArray[numpy.float64]) -> tuple: ...
    def n_accepted(self) -> int: ...
    def n_proposed(self) -> int: ...
    def set_params(self, params: numpy.typing.NDArray[numpy.float64]) -> None: ...

class BoundPotential:
    def __init__(self, potential: Potential, params: numpy.typing.NDArray[numpy.float64]) -> None: ...
    def execute(self, coords: numpy.typing.NDArray[numpy.float64], box: numpy.typing.NDArray[numpy.float64], compute_du_dx: bool = ..., compute_u: bool = ...) -> tuple: ...
    def execute_batch(self, coords: numpy.typing.NDArray[numpy.float64], boxes: numpy.typing.NDArray[numpy.float64], compute_du_dx: bool, compute_u: bool) -> tuple: ...
    def execute_fixed(self, coords: numpy.typing.NDArray[numpy.float64], box: numpy.typing.NDArray[numpy.float64]) -> numpy.typing.NDArray[numpy.uint64]: ...
    def get_potential(self) -> Potential: ...
    def set_params(self, params: numpy.typing.NDArray[numpy.float64]) -> None: ...
    def size(self) -> int: ...

class CentroidRestraint_f32(Potential):
    def __init__(self, group_a_idxs: numpy.typing.NDArray[numpy.int32], group_b_idxs: numpy.typing.NDArray[numpy.int32], kb: float, b0: float) -> None: ...

class CentroidRestraint_f64(Potential):
    def __init__(self, group_a_idxs: numpy.typing.NDArray[numpy.int32], group_b_idxs: numpy.typing.NDArray[numpy.int32], kb: float, b0: float) -> None: ...

class ChiralAtomRestraint_f32(Potential):
    def __init__(self, idxs: numpy.typing.NDArray[numpy.int32]) -> None: ...

class ChiralAtomRestraint_f64(Potential):
    def __init__(self, idxs: numpy.typing.NDArray[numpy.int32]) -> None: ...

class ChiralBondRestraint_f32(Potential):
    def __init__(self, idxs: numpy.typing.NDArray[numpy.int32], signs: numpy.typing.NDArray[numpy.int32]) -> None: ...

class ChiralBondRestraint_f64(Potential):
    def __init__(self, idxs: numpy.typing.NDArray[numpy.int32], signs: numpy.typing.NDArray[numpy.int32]) -> None: ...

class Context:
    def __init__(self, x0: numpy.typing.NDArray[numpy.float64], v0: numpy.typing.NDArray[numpy.float64], box: numpy.typing.NDArray[numpy.float64], integrator: Integrator, bps: List[BoundPotential], movers: Optional[List[Mover]] = ...) -> None: ...
    def finalize(self) -> None: ...
    def get_barostat(self) -> MonteCarloBarostat: ...
    def get_box(self) -> numpy.typing.NDArray[numpy.float64]: ...
    def get_integrator(self) -> Integrator: ...
    def get_movers(self) -> List[Mover]: ...
    def get_potentials(self) -> List[BoundPotential]: ...
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

class FanoutSummedPotential(Potential):
    def __init__(self, potentials: List[Potential], parallel: bool = ...) -> None: ...
    def get_potentials(self) -> List[Potential]: ...

class FlatBottomBond_f32(Potential):
    def __init__(self, bond_idxs: numpy.typing.NDArray[numpy.int32]) -> None: ...

class FlatBottomBond_f64(Potential):
    def __init__(self, bond_idxs: numpy.typing.NDArray[numpy.int32]) -> None: ...

class HarmonicAngleStable_f32(Potential):
    def __init__(self, angle_idxs: numpy.typing.NDArray[numpy.int32]) -> None: ...

class HarmonicAngleStable_f64(Potential):
    def __init__(self, angle_idxs: numpy.typing.NDArray[numpy.int32]) -> None: ...

class HarmonicAngle_f32(Potential):
    def __init__(self, angle_idxs: numpy.typing.NDArray[numpy.int32]) -> None: ...

class HarmonicAngle_f64(Potential):
    def __init__(self, angle_idxs: numpy.typing.NDArray[numpy.int32]) -> None: ...

class HarmonicBond_f32(Potential):
    def __init__(self, bond_idxs: numpy.typing.NDArray[numpy.int32]) -> None: ...

class HarmonicBond_f64(Potential):
    def __init__(self, bond_idxs: numpy.typing.NDArray[numpy.int32]) -> None: ...

class HilbertSort:
    def __init__(self, size: int) -> None: ...
    def sort(self, coords: numpy.typing.NDArray[numpy.float64], box: numpy.typing.NDArray[numpy.float64]) -> numpy.typing.NDArray[numpy.uint32]: ...

class Integrator:
    def __init__(self, *args, **kwargs) -> None: ...

class InvalidHardware(Exception): ...

class LangevinIntegrator(Integrator):
    def __init__(self, masses: numpy.typing.NDArray[numpy.float64], temperature: float, dt: float, friction: float, seed: int) -> None: ...

class LogFlatBottomBond_f32(Potential):
    def __init__(self, bond_idxs: numpy.typing.NDArray[numpy.int32], beta: float) -> None: ...

class LogFlatBottomBond_f64(Potential):
    def __init__(self, bond_idxs: numpy.typing.NDArray[numpy.int32], beta: float) -> None: ...

class LogSumExp_f32:
    def __init__(self, N: int) -> None: ...
    def sum(self, values: numpy.typing.NDArray[numpy.float64]) -> numpy.typing.NDArray[numpy.float32]: ...

class LogSumExp_f64:
    def __init__(self, N: int) -> None: ...
    def sum(self, values: numpy.typing.NDArray[numpy.float64]) -> numpy.typing.NDArray[numpy.float64]: ...

class MonteCarloBarostat(Mover):
    def __init__(self, N: int, pressure: float, temperature: float, group_idxs: List[List[int]], interval: int, bps, seed: int, adaptive_scaling_enabled: bool, initial_volume_scale_factor: float) -> None: ...
    def get_adaptive_scaling(self) -> bool: ...
    def get_volume_scale_factor(self) -> float: ...
    def set_adaptive_scaling(self, adaptive_scaling_enabled: bool) -> None: ...
    def set_pressure(self, pressure: float) -> None: ...
    def set_volume_scale_factor(self, volume_scale_factor: float) -> None: ...

class Mover:
    def __init__(self, *args, **kwargs) -> None: ...
    def get_interval(self) -> int: ...
    def move(self, coords: numpy.typing.NDArray[numpy.float64], box: numpy.typing.NDArray[numpy.float64]) -> tuple: ...
    def set_interval(self, interval: int) -> None: ...
    def set_step(self, step: int) -> None: ...

class Neighborlist_f32:
    def __init__(self, N: int) -> None: ...
    def compute_block_bounds(self, coords: numpy.typing.NDArray[numpy.float64], box: numpy.typing.NDArray[numpy.float64], block_size: int) -> tuple: ...
    def get_max_ixn_count(self) -> int: ...
    def get_nblist(self, coords: numpy.typing.NDArray[numpy.float64], box: numpy.typing.NDArray[numpy.float64], cutoff: float) -> List[List[int]]: ...
    def get_tile_ixn_count(self) -> int: ...
    def reset_row_idxs(self) -> None: ...
    def resize(self, size: int) -> None: ...
    def set_row_idxs(self, idxs: numpy.typing.NDArray[numpy.uint32]) -> None: ...

class Neighborlist_f64:
    def __init__(self, N: int) -> None: ...
    def compute_block_bounds(self, coords: numpy.typing.NDArray[numpy.float64], box: numpy.typing.NDArray[numpy.float64], block_size: int) -> tuple: ...
    def get_max_ixn_count(self) -> int: ...
    def get_nblist(self, coords: numpy.typing.NDArray[numpy.float64], box: numpy.typing.NDArray[numpy.float64], cutoff: float) -> List[List[int]]: ...
    def get_tile_ixn_count(self) -> int: ...
    def reset_row_idxs(self) -> None: ...
    def resize(self, size: int) -> None: ...
    def set_row_idxs(self, idxs: numpy.typing.NDArray[numpy.uint32]) -> None: ...

class NonbondedAllPairs_f32(Potential):
    def __init__(self, num_atoms: int, beta: float, cutoff: float, atom_idxs_i: Optional[numpy.typing.NDArray[numpy.int32]] = ..., disable_hilbert_sort: bool = ..., nblist_padding: float = ...) -> None: ...
    def get_atom_idxs(self) -> List[int]: ...
    def get_num_atom_idxs(self) -> int: ...
    def set_atom_idxs(self, atom_idxs: List[int]) -> None: ...

class NonbondedAllPairs_f64(Potential):
    def __init__(self, num_atoms: int, beta: float, cutoff: float, atom_idxs_i: Optional[numpy.typing.NDArray[numpy.int32]] = ..., disable_hilbert_sort: bool = ..., nblist_padding: float = ...) -> None: ...
    def get_atom_idxs(self) -> List[int]: ...
    def get_num_atom_idxs(self) -> int: ...
    def set_atom_idxs(self, atom_idxs: List[int]) -> None: ...

class NonbondedExclusions_f32(Potential):
    def __init__(self, pair_idxs_i: numpy.typing.NDArray[numpy.int32], scales_i: numpy.typing.NDArray[numpy.float64], beta: float, cutoff: float) -> None: ...

class NonbondedExclusions_f64(Potential):
    def __init__(self, pair_idxs_i: numpy.typing.NDArray[numpy.int32], scales_i: numpy.typing.NDArray[numpy.float64], beta: float, cutoff: float) -> None: ...

class NonbondedInteractionGroup_f32(Potential):
    def __init__(self, num_atoms: int, row_atom_idxs_i: numpy.typing.NDArray[numpy.int32], beta: float, cutoff: float, col_atom_idxs_i: Optional[numpy.typing.NDArray[numpy.int32]] = ..., disable_hilbert_sort: bool = ..., nblist_padding: float = ...) -> None: ...
    def set_atom_idxs(self, row_atom_idxs: List[int], col_atom_idxs: List[int]) -> None: ...

class NonbondedInteractionGroup_f64(Potential):
    def __init__(self, num_atoms: int, row_atom_idxs_i: numpy.typing.NDArray[numpy.int32], beta: float, cutoff: float, col_atom_idxs_i: Optional[numpy.typing.NDArray[numpy.int32]] = ..., disable_hilbert_sort: bool = ..., nblist_padding: float = ...) -> None: ...
    def set_atom_idxs(self, row_atom_idxs: List[int], col_atom_idxs: List[int]) -> None: ...

class NonbondedMolEnergyPotential_f32:
    def __init__(self, N: int, target_mols: List[List[int]], beta: float, cutoff: float) -> None: ...
    def execute(self, coords: numpy.typing.NDArray[numpy.float64], params: numpy.typing.NDArray[numpy.float64], box: numpy.typing.NDArray[numpy.float64]) -> numpy.typing.NDArray[numpy.float64]: ...

class NonbondedMolEnergyPotential_f64:
    def __init__(self, N: int, target_mols: List[List[int]], beta: float, cutoff: float) -> None: ...
    def execute(self, coords: numpy.typing.NDArray[numpy.float64], params: numpy.typing.NDArray[numpy.float64], box: numpy.typing.NDArray[numpy.float64]) -> numpy.typing.NDArray[numpy.float64]: ...

class NonbondedPairListPrecomputed_f32(Potential):
    def __init__(self, pair_idxs: numpy.typing.NDArray[numpy.int32], beta: float, cutoff: float) -> None: ...

class NonbondedPairListPrecomputed_f64(Potential):
    def __init__(self, pair_idxs: numpy.typing.NDArray[numpy.int32], beta: float, cutoff: float) -> None: ...

class NonbondedPairList_f32(Potential):
    def __init__(self, pair_idxs_i: numpy.typing.NDArray[numpy.int32], scales_i: numpy.typing.NDArray[numpy.float64], beta: float, cutoff: float) -> None: ...

class NonbondedPairList_f64(Potential):
    def __init__(self, pair_idxs_i: numpy.typing.NDArray[numpy.int32], scales_i: numpy.typing.NDArray[numpy.float64], beta: float, cutoff: float) -> None: ...

class PeriodicTorsion_f32(Potential):
    def __init__(self, angle_idxs: numpy.typing.NDArray[numpy.int32]) -> None: ...

class PeriodicTorsion_f64(Potential):
    def __init__(self, angle_idxs: numpy.typing.NDArray[numpy.int32]) -> None: ...

class Potential:
    def __init__(self, *args, **kwargs) -> None: ...
    def execute(self, coords: numpy.typing.NDArray[numpy.float64], params: numpy.typing.NDArray[numpy.float64], box: numpy.typing.NDArray[numpy.float64], compute_du_dx: bool = ..., compute_du_dp: bool = ..., compute_u: bool = ...) -> tuple: ...
    def execute_batch(self, coords: numpy.typing.NDArray[numpy.float64], params: numpy.typing.NDArray[numpy.float64], boxes: numpy.typing.NDArray[numpy.float64], compute_du_dx: bool, compute_du_dp: bool, compute_u: bool) -> tuple: ...
    def execute_du_dx(self, coords: numpy.typing.NDArray[numpy.float64], params: numpy.typing.NDArray[numpy.float64], box: numpy.typing.NDArray[numpy.float64]) -> numpy.typing.NDArray[numpy.float64]: ...

class SummedPotential(Potential):
    def __init__(self, potentials: List[Potential], params_sizes: List[int], parallel: bool = ...) -> None: ...
    def get_potentials(self) -> List[Potential]: ...

class TIBDExchangeMove_f32(BDExchangeMove_f32):
    def __init__(self, *args, **kwargs) -> None: ...
    def acceptance_fraction(self) -> float: ...
    def last_log_probability(self) -> float: ...
    def move(self, coords: numpy.typing.NDArray[numpy.float64], box: numpy.typing.NDArray[numpy.float64]) -> tuple: ...
    def n_accepted(self) -> int: ...
    def n_proposed(self) -> int: ...

class TIBDExchangeMove_f64(BDExchangeMove_f64):
    def __init__(self, *args, **kwargs) -> None: ...
    def acceptance_fraction(self) -> float: ...
    def last_log_probability(self) -> float: ...
    def move(self, coords: numpy.typing.NDArray[numpy.float64], box: numpy.typing.NDArray[numpy.float64]) -> tuple: ...
    def n_accepted(self) -> int: ...
    def n_proposed(self) -> int: ...

class VelocityVerletIntegrator(Integrator):
    def __init__(self, dt: float, cbs: numpy.typing.NDArray[numpy.float64]) -> None: ...

class WeightedRandomSampler_f32:
    def __init__(self, size: int, seed: int) -> None: ...
    def sample(self, num_samples: int, probabilities: numpy.typing.NDArray[numpy.float64]) -> List[int]: ...

class WeightedRandomSampler_f64:
    def __init__(self, size: int, seed: int) -> None: ...
    def sample(self, num_samples: int, probabilities: numpy.typing.NDArray[numpy.float64]) -> List[int]: ...

def _accumulate_energy(x: numpy.typing.NDArray[numpy.int64]) -> float: ...
def atom_by_atom_energies_f32(target_atoms: numpy.typing.NDArray[numpy.int32], coords: numpy.typing.NDArray[numpy.float64], params: numpy.typing.NDArray[numpy.float64], box: numpy.typing.NDArray[numpy.float64], nb_beta: float, nb_cutoff: float) -> numpy.typing.NDArray[numpy.float32]: ...
def atom_by_atom_energies_f64(target_atoms: numpy.typing.NDArray[numpy.int32], coords: numpy.typing.NDArray[numpy.float64], params: numpy.typing.NDArray[numpy.float64], box: numpy.typing.NDArray[numpy.float64], nb_beta: float, nb_cutoff: float) -> numpy.typing.NDArray[numpy.float64]: ...
def cuda_device_reset() -> None: ...
def inner_and_outer_mols_f32(center_atoms: numpy.typing.NDArray[numpy.int32], coords: numpy.typing.NDArray[numpy.float64], box: numpy.typing.NDArray[numpy.float64], group_idxs: List[List[int]], radius: float) -> tuple: ...
def inner_and_outer_mols_f64(center_atoms: numpy.typing.NDArray[numpy.int32], coords: numpy.typing.NDArray[numpy.float64], box: numpy.typing.NDArray[numpy.float64], group_idxs: List[List[int]], radius: float) -> tuple: ...
def rmsd_align(x1: numpy.typing.NDArray[numpy.float64], x2: numpy.typing.NDArray[numpy.float64]) -> numpy.typing.NDArray[numpy.float64]: ...
def rotate_and_translate_mol_f32(coords: numpy.typing.NDArray[numpy.float64], box: numpy.typing.NDArray[numpy.float64], quaternion: numpy.typing.NDArray[numpy.float64], translation: numpy.typing.NDArray[numpy.float64]) -> numpy.typing.NDArray[numpy.float64]: ...
def rotate_and_translate_mol_f64(coords: numpy.typing.NDArray[numpy.float64], box: numpy.typing.NDArray[numpy.float64], quaternion: numpy.typing.NDArray[numpy.float64], translation: numpy.typing.NDArray[numpy.float64]) -> numpy.typing.NDArray[numpy.float64]: ...
def rotate_coords_f32(coords: numpy.typing.NDArray[numpy.float64], quaternions: numpy.typing.NDArray[numpy.float64]) -> numpy.typing.NDArray[numpy.float64]: ...
def rotate_coords_f64(coords: numpy.typing.NDArray[numpy.float64], quaternions: numpy.typing.NDArray[numpy.float64]) -> numpy.typing.NDArray[numpy.float64]: ...
def translation_outside_sphere_f32(num_translations: int, center: numpy.typing.NDArray[numpy.float64], box: numpy.typing.NDArray[numpy.float64], radius: float, seed: int) -> numpy.typing.NDArray[numpy.float32]: ...
def translation_outside_sphere_f64(num_translations: int, center: numpy.typing.NDArray[numpy.float64], box: numpy.typing.NDArray[numpy.float64], radius: float, seed: int) -> numpy.typing.NDArray[numpy.float64]: ...
def translation_within_sphere_f32(num_translations: int, center: numpy.typing.NDArray[numpy.float64], radius: float, seed: int) -> numpy.typing.NDArray[numpy.float32]: ...
def translation_within_sphere_f64(num_translations: int, center: numpy.typing.NDArray[numpy.float64], radius: float, seed: int) -> numpy.typing.NDArray[numpy.float64]: ...
