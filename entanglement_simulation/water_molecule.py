"""
This module contains the WaterMolecule class, which is used to create a water molecule with a given radius and bond angle.
This script is used to generate the file: entanglement_simulation/data/water_data.json
"""
import numpy as np
from qiskit_nature.drivers import Molecule
from qiskit_nature.drivers.second_quantization import PySCFDriver
from qiskit_nature.problems.second_quantization import ElectronicStructureProblem

from entanglement_simulation.utils.classical_solver import CLASSICAL_SOLVER
from entanglement_simulation.utils.experiment_data import DataPoint, ExperimentDataSet

from entanglement_simulation import DATA_DIR

R_1 = 0.958  # position for the first H atom
R_2 = 0.958  # position for the second H atom
THETAS_IN_DEG = 104.478  # bond angles.
WATER_DATA_FILE_PATH = DATA_DIR / "water_data.json"


def radii(n_points: int = 50) -> np.ndarray:
    return np.linspace(0.5, 2.5, n_points)


class WaterMolecule:
    def __init__(self, radius_1: float = R_1, radius_2: float = R_2, thetas_in_deg: float = THETAS_IN_DEG):
        self.radius_1 = radius_1
        self.radius_2 = radius_2
        self.thetas_in_deg = thetas_in_deg
        self.molecule = Molecule(
            geometry=[
                ("O", [0.0, 0.0, 0.0]),
                ("H", [self.h1_x, 0.0, 0.0]),
                ("H", [self.h2_x, self.h2_y, 0.0]),
            ],
            charge=0,
            multiplicity=1,
        )
        self._problem = None
        self._classical_result = None

    def __repr__(self):
        return f"WaterMolecule(radius_1={self.radius_1}, radius_2={self.radius_2}, thetas_in_deg={self.thetas_in_deg})"

    def __str__(self):
        return self.__repr__()

    def _to_problem(self) -> ElectronicStructureProblem:
        driver = PySCFDriver.from_molecule(molecule=self.molecule, basis="sto6g")
        return ElectronicStructureProblem(driver)

    def solve_classical_result(self):
        if not self._classical_result:
            self._classical_result = CLASSICAL_SOLVER.solve(self.problem)

    @property
    def h1_x(self):
        return self.radius_1

    @property
    def h2_x(self):
        return self.radius_2 * np.cos(np.pi / 180 * self.thetas_in_deg)

    @property
    def h2_y(self):
        return self.radius_2 * np.sin(np.pi / 180 * self.thetas_in_deg)

    @property
    def problem(self) -> ElectronicStructureProblem:
        if self._problem is None:
            self._problem = self._to_problem()
        return self._problem

    @property
    def classical_result(self):
        if not self._classical_result:
            self.solve_classical_result()
        return self._classical_result

    @property
    def hartree_fock_energy(self):
        return self.classical_result.hartree_fock_energy

    @property
    def classical_energy(self):
        return self.classical_result.total_energies[0]


def create_water_data() -> ExperimentDataSet:
    water_data = ExperimentDataSet()
    for radius in radii(50):
        water = WaterMolecule(radius_2=radius)
        classical_energy = water.classical_energy
        print("Classical energy = ", classical_energy)
        water_data.add_data_point(
            DataPoint(
                radius=radius,
                hartree_fock_energy=water.hartree_fock_energy,
                classical_energy=classical_energy,
            )
        )
    return water_data


if __name__ == "__main__":
    water_data = create_water_data()
    water_data.to_json(WATER_DATA_FILE_PATH)
