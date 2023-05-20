import warnings
from dataclasses import dataclass
from typing import Optional

from entanglement_forging.core.wrappers.entanglement_forged_vqe_result import (
    EntanglementForgedVQEResult,
)

import numpy as np
import pickle

from qiskit_nature.drivers.second_quantization import PySCFDriver
from qiskit_nature.problems.second_quantization import ElectronicStructureProblem
from qiskit_nature.mappers.second_quantization import JordanWignerMapper
from qiskit_nature.converters.second_quantization import QubitConverter
from qiskit import Aer
from qiskit_nature.algorithms.ground_state_solvers import (
    GroundStateEigensolver,
    NumPyMinimumEigensolverFactory,
)
from qiskit.circuit import Parameter

import sys
from entanglement_forging import Log
from entanglement_forging import EntanglementForgedGroundStateSolver
from entanglement_forging import EntanglementForgedConfig

from circuits import hop_gate_1, hop_gate_2, ansatz_circuit
from water_molecule import water_molecule, radii

warnings.filterwarnings("ignore")
sys.path.append("../../")

k = 6


@dataclass
class SimulationReport:
    radius: float
    forged_result: Optional[EntanglementForgedVQEResult] = None


def reduce_bitstrings(bitstrings, orbitals_to_reduce) -> list:
    """Returns reduced bitstrings."""
    return np.delete(bitstrings, orbitals_to_reduce, axis=-1).tolist()


orbitals_to_reduce = [0, 3]
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

theta = Parameter("θ")

reports = []
for i, radius in enumerate(radii(10)):
    molecule = water_molecule(radius_2=radius)
    driver = PySCFDriver.from_molecule(molecule=molecule, basis="sto6g")
    problem = ElectronicStructureProblem(driver)

    converter = QubitConverter(JordanWignerMapper())

    solver = GroundStateEigensolver(
        converter, NumPyMinimumEigensolverFactory(use_default_filter_criterion=False)
    )

    hop_gate = hop_gate_2(theta)
    hop_gate.draw()
    ansatz = ansatz_circuit(hop_gate, theta)
    ansatz.draw("text", justify="right", fold=-1)

    Log.VERBOSE = False

    backend = Aer.get_backend("statevector_simulator")

    config = EntanglementForgedConfig(
        backend=backend,
        maxiter=350,
        spsa_c0=20 * np.pi,
        initial_params=[0, 0, 0, 0],
    )

    calc = EntanglementForgedGroundStateSolver(
        qubit_converter=converter,
        ansatz=ansatz,
        bitstrings_u=reduced_bitstrings[:k],
        config=config,
        orbitals_to_reduce=orbitals_to_reduce,
    )
    res = calc.solve(problem)
    print(res.ground_state_energy)
    report = SimulationReport(radius=radius, forged_result=res)
    print(f"create report {i}")
    reports.append(report)

with open(f"reports_k{k}.pickle", "wb") as f:
    pickle.dump([r.__dict__ for r in reports], f)
