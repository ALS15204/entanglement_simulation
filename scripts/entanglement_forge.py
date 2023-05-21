import sys
import warnings
from dataclasses import dataclass
import numpy as np
import pickle

from qiskit_nature.algorithms import (
    GroundStateEigensolver,
    NumPyMinimumEigensolverFactory,
)
from qiskit_nature.drivers.second_quantization import PySCFDriver
from qiskit_nature.problems.second_quantization import ElectronicStructureProblem
from qiskit_nature.mappers.second_quantization import JordanWignerMapper
from qiskit_nature.converters.second_quantization import QubitConverter
from qiskit import Aer
from qiskit.circuit import Parameter

from entanglement_forging import Log
from entanglement_forging import EntanglementForgedGroundStateSolver
from entanglement_forging import EntanglementForgedConfig
from entanglement_forging.core.wrappers.entanglement_forged_vqe_result import (
    EntanglementForgedVQEResult,
)

from utils.circuits import hop_gate_1, hop_gate_2, hop_gate_3, ansatz_circuit_1, ansatz_circuit_2
from utils.water_molecule import water_molecule, radii

warnings.filterwarnings("ignore")
sys.path.append("../../")

# Experiment set up
k = 6
orbitals_to_reduce = [0, 3]
spsa_c0 = 10 * np.pi
spsa_c1 = 0.5
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

reports = []
for i, radius in enumerate(radii(10)):
    # if radius < 2.0:
    #     continue
    molecule = water_molecule(radius_2=radius)
    driver = PySCFDriver.from_molecule(molecule=molecule, basis="sto6g")
    problem = ElectronicStructureProblem(driver)

    converter = QubitConverter(JordanWignerMapper())
    solver = GroundStateEigensolver(
        converter,
        NumPyMinimumEigensolverFactory(use_default_filter_criterion=False),
    )

    result = solver.solve(problem)

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
        qubit_converter=converter,
        ansatz=ansatz,
        bitstrings_u=reduced_bitstrings[:k],
        config=config,
        orbitals_to_reduce=orbitals_to_reduce,
    )
    res = calc.solve(problem)
    print(radius, res.ground_state_energy)
    report = SimulationReport(radius=radius, forged_result=res, hartree_fock_energy=result.hartree_fock_energy)
    print(f"create report {i}")
    reports.append(report)

with open(f"reports_k{k}.pickle", "wb") as f:
    pickle.dump([r.__dict__ for r in reports], f)
