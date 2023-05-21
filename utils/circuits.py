from typing import Annotated, Iterable

from qiskit.circuit import Parameter, QuantumCircuit

HOPE_GATE = QuantumCircuit(2, name="Hop gate")
PHIS = (
    Parameter("θ1"),
    Parameter("θ2"),
    Parameter("θ3"),
    Parameter("θ4"),
)


def hop_gate_1(theta: Parameter) -> QuantumCircuit:
    hop_gate = HOPE_GATE.copy()
    hop_gate.h(0)
    hop_gate.cx(1, 0)
    hop_gate.cx(0, 1)
    hop_gate.ry(-theta, 0)
    hop_gate.ry(-theta, 1)
    hop_gate.cx(0, 1)
    hop_gate.h(0)
    return hop_gate


def hop_gate_2(theta: Parameter) -> QuantumCircuit:
    hop_gate = HOPE_GATE.copy()
    hop_gate.swap(0, 1)
    hop_gate.h(1)
    hop_gate.cx(1, 0)
    hop_gate.ry(theta, 0)
    hop_gate.ry(theta, 1)
    hop_gate.cx(0, 1)
    hop_gate.h(0)
    return hop_gate


def hop_gate_3(theta: Parameter) -> QuantumCircuit:
    hop_gate = HOPE_GATE.copy()
    hop_gate.h(1)
    hop_gate.cx(1, 0)
    hop_gate.ry(theta, 0)
    hop_gate.ry(theta, 1)
    hop_gate.cx(0, 1)
    hop_gate.h(0)
    return hop_gate


def ansatz_circuit_1(
    hop_gate: QuantumCircuit,
    theta: Parameter,
    phis: Annotated[Iterable[Parameter], 4] = PHIS,
) -> QuantumCircuit:
    phi_1, phi_2, phi_3, phi_4 = phis
    ansatz = QuantumCircuit(5)
    ansatz.append(hop_gate.to_gate({theta: phi_1}), [0, 1])
    ansatz.append(hop_gate.to_gate({theta: phi_2}), [3, 4])
    ansatz.append(hop_gate.to_gate({theta: 0}), [1, 4])
    ansatz.append(hop_gate.to_gate({theta: phi_3}), [0, 2])
    ansatz.append(hop_gate.to_gate({theta: phi_4}), [3, 4])
    return ansatz


def ansatz_circuit_2(hop_gate_1, hop_gate_2, theta: Parameter):
    phi_1, phi_2, phi_3, phi_4 = PHIS
    ansatz = QuantumCircuit(5)
    ansatz.swap(0, 1)
    ansatz.append(hop_gate_1.to_gate({theta: phi_2}), [3, 4])
    ansatz.append(hop_gate_2.to_gate({theta: phi_1}), [0, 1])
    ansatz.append(hop_gate_1.to_gate({theta: 0}), [1, 4])
    ansatz.swap(0, 2)
    ansatz.swap(3, 4)
    ansatz.append(hop_gate_2.to_gate({theta: phi_3}), [0, 2])
    ansatz.append(hop_gate_2.to_gate({theta: phi_4}), [3, 4])
    return ansatz