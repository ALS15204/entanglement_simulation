import sys
import warnings
from dataclasses import dataclass, asdict
import numpy as np
import pickle

from qiskit import Aer
from qiskit.circuit import Parameter

from entanglement_forging import Log
from entanglement_forging import EntanglementForgedGroundStateSolver
from entanglement_forging import EntanglementForgedConfig
from entanglement_forging.core.wrappers.entanglement_forged_vqe_result import (
    EntanglementForgedVQEResult,
)

from utils.circuits import hop_gate_1, hop_gate_2, hop_gate_3, ansatz_circuit_1, ansatz_circuit_2
from utils.classical_solver import CLASSICAL_SOLVER, CONVERTER
from utils.water_molecule import radii, WaterMolecule

warnings.filterwarnings("ignore")
sys.path.append("../../")

# Experiment set up
k = 3
orbitals_to_reduce = [0, 3]
spsa_c0s = np.arange(1, 11, 2) * np.pi
spsa_c1s = np.arange(1, 6, 1) * 0.1
# spsa_c0 = 3 * np.pi
# spsa_c1 = 0.3
initial_params = [np.pi / 4, np.pi / 2, 3 * np.pi / 4, np.pi]
theta = Parameter("θ")
hop_gate_1 = hop_gate_2(theta)
ansatz = ansatz_circuit_1(hop_gate_1, theta)
ansatz.draw("text", justify="right", fold=-1)


@dataclass
class SimulationReport:
    radius: float
    forged_result: EntanglementForgedVQEResult
    hartree_fock_energy: float

    def to_dict(self):
        return asdict(self)


def reduce_bitstrings(bitstrings, orbitals_to_reduce) -> list:
    """Returns reduced bitstrings."""
    return np.delete(bitstrings, orbitals_to_reduce, axis=-1).tolist()


bitstrings = (
    [1, 1, 1, 1, 1, 0, 0],
    [1, 0, 1, 1, 1, 1, 0],
    [1, 0, 1, 1, 1, 0, 1],
    [1, 1, 0, 1, 1, 1, 0],
    [1, 1, 0, 1, 1, 0, 1],
    [1, 1, 1, 0, 1, 1, 0],
)
reduced_bitstrings = reduce_bitstrings(bitstrings, orbitals_to_reduce)
print(f"Bitstrings: {bitstrings}")
print(f"Bitstrings after orbital reduction: {reduced_bitstrings}")

for spsa_c0 in spsa_c0s:
    for spsa_c1 in spsa_c1s:
        reports = []
        for i, radius in enumerate(radii(10)):
            if radius > 1.7 or radius < 1.5:
                continue
            water = WaterMolecule(radius_2=radius)
            water.solve_classical_result()

            Log.VERBOSE = False

            backend = Aer.get_backend("statevector_simulator")

            config = EntanglementForgedConfig(
                backend=backend,
                maxiter=100,
                spsa_c0=spsa_c0,
                spsa_c1=spsa_c1,
                initial_params=initial_params,
            )

            calc = EntanglementForgedGroundStateSolver(
                qubit_converter=CONVERTER,
                ansatz=ansatz,
                bitstrings_u=reduced_bitstrings[:k],
                config=config,
                orbitals_to_reduce=orbitals_to_reduce,
            )
            res = calc.solve(water.problem)
            print(radius, res.ground_state_energy)
            report = SimulationReport(radius=radius, forged_result=res, hartree_fock_energy=water.hartree_fock_energy)
            print(f"create report {i}")
            reports.append(report)

                    # with open(f"c0_{int(spsa_c0/np.pi)}_c1_{spsa_c1}_reports_k{k}.pickle", "wb") as f:
                    #     pickle.dump([r.to_dict() for r in reports], f)

        print(
            f"{spsa_c0}, {spsa_c1}, {sum(r.hartree_fock_energy - r.forged_result.ground_state_energy for r in reports)}"
        )
