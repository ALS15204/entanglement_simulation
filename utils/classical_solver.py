from qiskit_nature.algorithms import GroundStateEigensolver, NumPyMinimumEigensolverFactory
from qiskit_nature.converters.second_quantization import QubitConverter
from qiskit_nature.mappers.second_quantization import JordanWignerMapper

CONVERTER = QubitConverter(JordanWignerMapper())
CLASSICAL_SOLVER = GroundStateEigensolver(
    CONVERTER,
    NumPyMinimumEigensolverFactory(use_default_filter_criterion=False),
)
