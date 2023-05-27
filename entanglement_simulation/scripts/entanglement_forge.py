"""
This script runs the entanglement forging experiment.
"""
from pathlib import Path
from typing import Union, Dict

import numpy as np

from qiskit import Aer, QuantumCircuit
from qiskit.circuit import Parameter

from entanglement_forging import EntanglementForgedGroundStateSolver
from entanglement_forging import EntanglementForgedConfig

from entanglement_simulation import EXPERIMENT_DIR
from entanglement_simulation.circuits import hop_gate_2, ansatz_circuit_1
from entanglement_simulation.data.constants import BITSTRINGS
from entanglement_simulation.utils.classical_solver import CONVERTER
from entanglement_simulation.utils.experiment_data import DataPoint, ExperimentDataSet, HyperParameters
from entanglement_simulation.water_molecule import radii, WaterMolecule, thetas


def reduce_bitstrings(bitstrings, orbitals_to_reduce) -> list:
    """Returns reduced bitstrings."""
    return np.delete(bitstrings, orbitals_to_reduce, axis=-1).tolist()


def collect_exisiting_hyperparams_to_results(
        experiment_path: Union[Path, str]
) -> Dict[HyperParameters, ExperimentDataSet]:
    """Collects all existing results from a given experiment path."""
    experiment_path = Path(experiment_path)
    exisiting_results = [ExperimentDataSet.from_json(f) for f in list(experiment_path.glob("*.json"))]
    return {result.hyperparameters: result for result in exisiting_results}


def run_one_entangled_forging_experiment(
        ansatz: QuantumCircuit, hyperparameters: HyperParameters, reduced_bitstrings: list, target_dir: Path,
        case: str = "b"
) -> ExperimentDataSet:
    """Runs one entangled forging experiment with one set of hyperparameters."""

    if case not in ["a", "b", "c"]:
        raise ValueError("Case must be 'a', 'b', or 'c'.")
    if case in {"a", "b"}:
        params = radii(50)
    elif case == "c":
        params = thetas(50)

    print(hyperparameters)
    # Check if the experiment has already been run.
    hyperparam_to_exisiting_results = collect_exisiting_hyperparams_to_results(target_dir)
    if hyperparameters in hyperparam_to_exisiting_results:
        exisiting_result = hyperparam_to_exisiting_results[hyperparameters]
        for data_point in exisiting_result.data_points:
            print(f"Radius: {data_point.radius: .3f}; Ground State Energy: {data_point.forged_vqe_energy: .5f}")
        return exisiting_result

    # Run the experiment.
    experiment_data_set = ExperimentDataSet(hyperparameters=hyperparameters)
    for p in params:
        # Prepare the water molecule.
        if case == "a":
            water = WaterMolecule(radius_1=p, radius_2=p)
        elif case == "b":
            water = WaterMolecule(radius_2=p)
        elif case == "c":
            water = WaterMolecule(radius_1=p)
        water.solve_classical_result()

        # Run the entangled forging experiment.
        backend = Aer.get_backend("statevector_simulator")
        config = EntanglementForgedConfig(
            backend=backend,
            maxiter=100,
            spsa_c0=hyperparameters.spsa_c0,
            spsa_c1=hyperparameters.spsa_c1,
            initial_params=hyperparameters.initial_thetas,
        )
        calc = EntanglementForgedGroundStateSolver(
            qubit_converter=CONVERTER,
            ansatz=ansatz,
            bitstrings_u=reduced_bitstrings[:hyperparameters.k],
            config=config,
            orbitals_to_reduce=hyperparameters.orbitals_to_reduce
        )
        res = calc.solve(water.problem)
        print(f"Radius: {p: .3f}; Ground State Energy: {res.ground_state_energy: .5f}")

        # Prepare data point and add it to the experiment data set.
        data_point = DataPoint(
            radius=p,
            hartree_fock_energy=water.hartree_fock_energy,
            classical_energy=water.classical_energy,
            forged_vqe_energy=res.ground_state_energy,
            schmidts_coefficients=res.schmidts_value.tolist()
        )
        experiment_data_set.add_data_point(data_point)
    # Save the experiment data set.
    output_file_name = target_dir / f"{experiment_data_set.mean_square_error_to_classical: .5f}_result.json"
    experiment_data_set.to_json(output_file_name)
    return experiment_data_set


if __name__ == "__main__":

    # Experiment constants
    orbitals_to_reduce = [0, 3]
    k = 3
    case = "b"  # simulate case (b) in the paper
    experiment_dir = EXPERIMENT_DIR / f"case_{case}_reduced_orbitals_{orbitals_to_reduce[0]}_{orbitals_to_reduce[1]}_k{k}"
    experiment_dir.mkdir(exist_ok=True, parents=True)

    # Hyperparameters settings
    spsa_c0s = np.arange(1, 11, 1) * np.pi  # [1, 2, ..., 10] * pi
    spsa_c1s = np.arange(1, 6, 1) * 0.1  # [0.1, 0.2, ..., 0.5]
    initial_thetas_sets = [[np.pi / 4, np.pi / 2, 3 * np.pi / 4, np.pi]]

    # Prepare hyperparameters
    hyperparameters_sets = []
    for spsa_c0 in spsa_c0s:
        for spsa_c1 in spsa_c1s:
            hyperparameters_sets.extend(
                HyperParameters(
                    k=k,
                    spsa_c0=spsa_c0,
                    spsa_c1=spsa_c1,
                    orbitals_to_reduce=orbitals_to_reduce,
                    initial_thetas=initial_thetas,
                )
                for initial_thetas in initial_thetas_sets
            )

    # Prepare ansatz with frozen orbitals
    reduced_bitstrings = reduce_bitstrings(BITSTRINGS, orbitals_to_reduce)
    print(f"Bitstrings after orbital reduction: {reduced_bitstrings}")
    theta = Parameter("θ")
    hop_gate_1 = hop_gate_2(theta)
    ansatz = ansatz_circuit_1(hop_gate_1, theta)

    # Run experiments
    experiment_results = []
    for idx, hyperparameters in enumerate(hyperparameters_sets):
        print(f"Experiment {idx + 1}/{len(hyperparameters_sets)}")
        experiment_result = run_one_entangled_forging_experiment(
            ansatz, hyperparameters, reduced_bitstrings=reduced_bitstrings, target_dir=experiment_dir
        )
        experiment_results.append(experiment_result)

    # Save the best results
    final_result_dir = experiment_dir / "best_fit/"
    final_result_dir.mkdir(exist_ok=True, parents=True)
    # Search for the best k=3 experiment.
    best_experiment = min(experiment_results, key=lambda x: x.mean_square_error_to_classical)
    best_experiment.to_json(final_result_dir / "k3.json")
    best_hyperparameters = best_experiment.hyperparameters
    # Prepare hyperparameters and run the best experiment with k=6.
    best_hyperparameters_dict = best_hyperparameters.to_dict()
    best_hyperparameters_dict.pop("k")
    best_k6_hyperparameters = HyperParameters(k=6, **best_hyperparameters_dict)
    best_k6_result = run_one_entangled_forging_experiment(
        ansatz, best_k6_hyperparameters, reduced_bitstrings=reduced_bitstrings, target_dir=final_result_dir
    )
    best_k6_result.to_json(final_result_dir / "k6.json")
