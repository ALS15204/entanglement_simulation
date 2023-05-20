import json
from dataclasses import dataclass
import numpy as np
from qiskit_nature.algorithms import (
    GroundStateEigensolver,
    NumPyMinimumEigensolverFactory,
)
from qiskit_nature.converters.second_quantization import QubitConverter
from qiskit_nature.drivers import Molecule
from qiskit_nature.drivers.second_quantization import PySCFDriver
from qiskit_nature.mappers.second_quantization import JordanWignerMapper
from qiskit_nature.problems.second_quantization import ElectronicStructureProblem

R_1 = 0.958  # position for the first H atom
R_2 = 0.958  # position for the second H atom
THETAS_IN_DEG = 104.478  # bond angles.


def water_molecule(
    radius_1: float = R_1, radius_2: float = R_2, thetas_in_deg: float = THETAS_IN_DEG
) -> Molecule:
    H1_x = radius_1
    H2_x = radius_2 * np.cos(np.pi / 180 * thetas_in_deg)
    H2_y = radius_2 * np.sin(np.pi / 180 * thetas_in_deg)

    return Molecule(
        geometry=[
            ["O", [0.0, 0.0, 0.0]],
            ["H", [H1_x, 0.0, 0.0]],
            ["H", [H2_x, H2_y, 0.0]],
        ],
        charge=0,
        multiplicity=1,
    )


def radii(n_points: int = 50) -> np.ndarray:
    return np.linspace(0.5, 2.5, n_points)


@dataclass
class WaterMoleculeData:
    radius: float
    hartree_fock_energy: float
    classical_energy: float


if __name__ == "__main__":
    water_data = []
    for radius in radii(50):
        molecule = water_molecule(radius_2=radius)
        driver = PySCFDriver.from_molecule(molecule=molecule, basis="sto6g")
        problem = ElectronicStructureProblem(driver)

        converter = QubitConverter(JordanWignerMapper())

        solver = GroundStateEigensolver(
            converter,
            NumPyMinimumEigensolverFactory(use_default_filter_criterion=False),
        )

        result = solver.solve(problem)
        classical_energy = result.total_energies[0]
        print("Classical energy = ", classical_energy)
        water_data.append(
            WaterMoleculeData(
                radius=radius,
                hartree_fock_energy=result.hartree_fock_energy,
                classical_energy=classical_energy,
            )
        )

    with open("water_data.json", "w") as f:
        json.dump([d.__dict__ for d in water_data], f, indent=4, sort_keys=True)
