# test that we can run relative free energy simulations in complex and in solvent
# this doesn't test for accuracy, just that everything mechanically runs.
from importlib import resources
from typing import Sequence

import numpy as np
import pytest

from timemachine.constants import DEFAULT_FF
from timemachine.fe.free_energy import HostConfig, InitialState, PairBarResult, SimulationResult, image_frames, sample
from timemachine.fe.rbfe import estimate_relative_free_energy, run_solvent, run_vacuum
from timemachine.ff import Forcefield
from timemachine.md import builders
from timemachine.md.barostat.utils import compute_box_center
from timemachine.testsystems.relative import get_hif2a_ligand_pair_single_topology


def run_bitwise_reproducibility(mol_a, mol_b, core, forcefield, n_frames):
    # test that we can bitwise reproduce our trajectory using the initial state information

    lambda_schedule = [0.01, 0.02, 0.03]
    seed = 2023
    box_width = 4.0
    solvent_sys, solvent_conf, solvent_box, _ = builders.build_water_system(box_width, forcefield.water_ff)
    solvent_box += np.diag([0.1, 0.1, 0.1])  # remove any possible clashes
    solvent_host_config = HostConfig(solvent_sys, solvent_conf, solvent_box)
    keep_idxs = [0, 1, 2]
    solvent_res = estimate_relative_free_energy(
        mol_a,
        mol_b,
        core,
        forcefield,
        solvent_host_config,
        seed,
        n_frames=n_frames,
        prefix="solvent",
        lambda_schedule=lambda_schedule,
        keep_idxs=keep_idxs,
    )

    all_frames, all_boxes = [], []
    for state in solvent_res.initial_states:
        frames, boxes = sample(state, solvent_res.md_params)
        all_frames.append(frames)
        all_boxes.append(boxes)

    np.testing.assert_equal(solvent_res.frames, all_frames)
    np.testing.assert_equal(solvent_res.boxes, all_boxes)


def run_triple(mol_a, mol_b, core, forcefield, n_frames, protein_path, n_eq_steps):

    seed = 2023

    def check_sim_result(sim_res: SimulationResult):
        assert [x.lamb for x in sim_res.initial_states] == lambda_schedule

        assert sim_res.plots.dG_errs_png is not None
        assert sim_res.plots.overlap_summary_png is not None
        assert sim_res.plots.overlap_detail_png is not None

        assert len(sim_res.frames[0]) == n_frames
        assert len(sim_res.frames[-1]) == n_frames
        assert len(sim_res.boxes[0]) == n_frames
        assert len(sim_res.boxes[-1]) == n_frames
        assert sim_res.md_params.n_frames == n_frames
        assert sim_res.md_params.n_eq_steps == n_eq_steps

        def check_pair_bar_result(initial_states: Sequence[InitialState], bar_res: PairBarResult):
            n_pairs = len(initial_states) - 1
            assert len(bar_res.all_dGs) == n_pairs

            assert len(bar_res.all_errs) == n_pairs
            assert bar_res.dG_errs_by_lambda_by_component.shape[1] == n_pairs
            for dg_errs in [bar_res.all_errs, bar_res.dG_errs_by_lambda_by_component]:
                assert np.all(0.0 < np.asarray(dg_errs))
                assert np.linalg.norm(dg_errs) < 0.1

            assert len(bar_res.overlaps_by_lambda) == n_pairs
            assert bar_res.overlaps_by_lambda_by_component.shape[0] == bar_res.dG_errs_by_lambda_by_component.shape[0]
            assert bar_res.overlaps_by_lambda_by_component.shape[1] == n_pairs
            for overlaps in [bar_res.overlaps_by_lambda, bar_res.overlaps_by_lambda_by_component]:
                assert np.all(0.0 < np.asarray(overlaps))
                assert np.all(np.asarray(overlaps) < 1.0)

        check_pair_bar_result(sim_res.initial_states, sim_res.result)
        for initial_states, res in sim_res.intermediate_results:
            check_pair_bar_result(initial_states, res)

    lambda_schedule = [0.01, 0.02, 0.03]
    vacuum_host_config = None
    vacuum_res = estimate_relative_free_energy(
        mol_a,
        mol_b,
        core,
        forcefield,
        vacuum_host_config,
        seed,
        n_frames=n_frames,
        prefix="vacuum",
        lambda_schedule=lambda_schedule,
        n_eq_steps=n_eq_steps,
    )

    check_sim_result(vacuum_res)

    box_width = 4.0
    solvent_sys, solvent_conf, solvent_box, _ = builders.build_water_system(box_width, forcefield.water_ff)
    solvent_box += np.diag([0.1, 0.1, 0.1])  # remove any possible clashes
    solvent_host_config = HostConfig(solvent_sys, solvent_conf, solvent_box)
    solvent_res = estimate_relative_free_energy(
        mol_a,
        mol_b,
        core,
        forcefield,
        solvent_host_config,
        seed,
        n_frames=n_frames,
        prefix="solvent",
        lambda_schedule=lambda_schedule,
        n_eq_steps=n_eq_steps,
    )

    check_sim_result(solvent_res)

    seed = 2024
    complex_sys, complex_conf, _, _, complex_box, _ = builders.build_protein_system(
        protein_path, forcefield.protein_ff, forcefield.water_ff
    )
    complex_box += np.diag([0.1, 0.1, 0.1])  # remove any possible clashes
    complex_host_config = HostConfig(complex_sys, complex_conf, complex_box)
    complex_res = estimate_relative_free_energy(
        mol_a,
        mol_b,
        core,
        forcefield,
        complex_host_config,
        seed,
        n_frames=n_frames,
        prefix="complex",
        lambda_schedule=lambda_schedule,
        n_eq_steps=n_eq_steps,
    )

    check_sim_result(complex_res)


@pytest.mark.nightly(reason="Slow!")
def test_run_hif2a_test_system():

    mol_a, mol_b, core = get_hif2a_ligand_pair_single_topology()
    forcefield = Forcefield.load_from_file(DEFAULT_FF)

    with resources.path("timemachine.testsystems.data", "hif2a_nowater_min.pdb") as protein_path:
        run_triple(mol_a, mol_b, core, forcefield, n_frames=100, protein_path=str(protein_path), n_eq_steps=1000)
    run_bitwise_reproducibility(mol_a, mol_b, core, forcefield, n_frames=100)


def test_steps_per_frames():
    """Verifies that modifying steps per frames doesn't change result trajectory"""
    mol_a, mol_b, core = get_hif2a_ligand_pair_single_topology()
    forcefield = Forcefield.load_from_file(DEFAULT_FF)
    seed = 2022
    frames = 5
    res = run_vacuum(mol_a, mol_b, core, forcefield, None, frames, seed, n_eq_steps=10, steps_per_frame=2, n_windows=2)
    assert len(res.frames[0]) == frames

    frames = 2
    test_res = run_vacuum(
        mol_a, mol_b, core, forcefield, None, frames, seed, n_eq_steps=10, steps_per_frame=5, n_windows=2
    )
    assert len(test_res.frames[0]) == frames
    assert len(test_res.frames) == 2
    # The last frame from the trajectories should match as num_frames * steps_per_frame are equal
    for frame, test_frame in zip(res.frames, test_res.frames):
        np.testing.assert_array_equal(frame[-1], test_frame[-1])


def test_imaging_frames():
    """Verify that imaging frames places ligand at center and all coordinates are close to being within the box.

    Does not check precision, as it is known to be lossy. Only to be used for post-processing/visualization."""
    mol_a, mol_b, core = get_hif2a_ligand_pair_single_topology()
    forcefield = Forcefield.load_from_file(DEFAULT_FF)
    seed = 2022
    frames = 1
    steps_per_frame = 1
    equil_steps = 1
    windows = 2
    res, _, _ = run_solvent(
        mol_a,
        mol_b,
        core,
        forcefield,
        None,
        frames,
        seed,
        n_eq_steps=equil_steps,
        steps_per_frame=steps_per_frame,
        n_windows=windows,
    )
    keep_idxs = [0, len(res.initial_states) - 1]
    assert len(keep_idxs) == len(res.frames)

    # A buffer, as imaging doesn't ensure everything is perfectly in the box
    padding = 0.3
    for i, (frames, boxes) in enumerate(zip(res.frames, res.boxes)):
        initial_state = res.initial_states[keep_idxs[i]]
        box_center = compute_box_center(boxes[0])
        box_extents = np.max(boxes, axis=(0, 1))

        # Verify that coordinates are either outside of the box or below zero
        assert np.any(np.max(frames, axis=(0, 1)) > box_extents + padding) or np.any(
            np.min(frames, axis=(0, 1)) < -padding
        )
        # Ligand won't be near center of box
        assert not np.allclose(np.mean(frames[0][initial_state.ligand_idxs], axis=0), box_center)

        imaged = image_frames(initial_state, frames, boxes)

        # Verify that after imaged, coordinates are within padding of the box extents
        assert np.all(np.max(imaged, axis=(0, 1)) <= box_extents + padding) and np.all(
            np.min(imaged, axis=(0, 1)) >= -padding
        )
        # Verify that ligand was centered in the box
        np.testing.assert_allclose(np.mean(imaged[0][initial_state.ligand_idxs], axis=0), box_center)


def test_rbfe_with_1_window():
    """Should not be able to run a relative free energy calculation with a single window"""
    mol_a, mol_b, core = get_hif2a_ligand_pair_single_topology()
    forcefield = Forcefield.load_from_file(DEFAULT_FF)
    seed = 2022
    with pytest.raises(AssertionError):
        estimate_relative_free_energy(
            mol_a,
            mol_b,
            core,
            forcefield,
            None,
            seed,
            n_frames=1,
            prefix="failure",
            n_windows=1,
            steps_per_frame=1,
            n_eq_steps=10,
        )


if __name__ == "__main__":
    # convenience: so we can run this directly from python tests/test_relative_free_energy.py without
    # toggling the pytest marker
    test_run_hif2a_test_system()
