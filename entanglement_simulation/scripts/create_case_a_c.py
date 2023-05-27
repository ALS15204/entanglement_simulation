from qiskit.circuit import Parameter

from entanglement_simulation import EXPERIMENT_DIR
from entanglement_simulation.circuits import hop_gate_2, ansatz_circuit_1
from entanglement_simulation.data.constants import BITSTRINGS
from entanglement_simulation.scripts.entanglement_forge import reduce_bitstrings, run_one_entangled_forging_experiment
from entanglement_simulation.utils.experiment_data import ExperimentDataSet, HyperParameters

if __name__ == "__main__":

    case_b_best_fit = EXPERIMENT_DIR / "case_b_reduced_orbitals_0_3_k3/best_fit/k3.json"

    for case in ["a", "c"]:
        # Experiment constants
        orbitals_to_reduce = [0, 3]
        k = 3
        experiment_dir = EXPERIMENT_DIR / f"case_{case}_reduced_orbitals" \
                                          f"_{orbitals_to_reduce[0]}_{orbitals_to_reduce[1]}_k{k}"
        experiment_dir.mkdir(exist_ok=True, parents=True)
        final_result_dir = experiment_dir / "best_fit/"
        final_result_dir.mkdir(exist_ok=True, parents=True)

        # Prepare ansatz with frozen orbitals
        reduced_bitstrings = reduce_bitstrings(BITSTRINGS, orbitals_to_reduce)
        print(f"Bitstrings after orbital reduction: {reduced_bitstrings}")
        theta = Parameter("θ")
        hop_gate_1 = hop_gate_2(theta)
        ansatz = ansatz_circuit_1(hop_gate_1, theta)

        best_case_b_experiment = ExperimentDataSet.from_json(case_b_best_fit)
        best_hyperparameters = best_case_b_experiment.hyperparameters
        case_a_result = run_one_entangled_forging_experiment(
            ansatz, best_hyperparameters,
            reduced_bitstrings=reduced_bitstrings,
            target_dir=final_result_dir,
            case=case
        )

        # Prepare hyperparameters and run the best experiment with k=6.
        best_hyperparameters_dict = best_hyperparameters.to_dict()
        best_hyperparameters_dict.pop("k")
        best_k6_hyperparameters = HyperParameters(k=6, **best_hyperparameters_dict)
        best_k6_result = run_one_entangled_forging_experiment(
            ansatz, best_k6_hyperparameters, reduced_bitstrings=reduced_bitstrings, target_dir=final_result_dir, case=case
        )
        best_k6_result.to_json(final_result_dir / "k6.json")
