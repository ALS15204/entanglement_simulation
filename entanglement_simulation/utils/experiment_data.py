"""
This module contains the data classes used to store the results of the experiments.
"""
import json
from dataclasses import dataclass, asdict, field
import numpy as np
from pathlib import Path
from typing import Optional, List, Union, Dict


@dataclass
class DataPoint:
    radius: float
    hartree_fock_energy: float
    classical_energy: float
    forged_vqe_energy: Optional[float] = None
    schmidts_coefficients: Optional[List[float]] = None

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data_dict: Dict):
        return cls(**data_dict)


@dataclass
class HyperParameters:
    k: int = 3
    spsa_c0: float = 3 * np.pi
    spsa_c1: float = 0.3
    orbitals_to_reduce: list = field(default_factory=lambda: [0, 3])
    initial_thetas: list = field(default_factory=lambda: [np.pi / 4, np.pi / 2, 3 * np.pi / 4, np.pi])

    def __repr__(self):
        return f"HyperParameters(k={self.k}, spsa_c0={self.spsa_c0: .3f}, spsa_c1={self.spsa_c1: .3f}, " \
               f"orbitals_to_reduce={self.orbitals_to_reduce}, initial_thetas={self.initial_thetas})"

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        if isinstance(other, HyperParameters):
            return self.__dict__ == other.__dict__
        return False

    def __hash__(self):
        return hash(self.__repr__())

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data_dict: Dict):
        return cls(**data_dict)


@dataclass
class ExperimentDataSet:
    data_points: list[DataPoint] = field(default_factory=list)
    hyperparameters: Optional[HyperParameters] = None

    def add_data_point(self, data_point: DataPoint):
        self.data_points.append(data_point)

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self, file_path: Union[Path, str]):
        with open(file_path, "w") as f:
            json.dump(self.to_dict(), f)

    @classmethod
    def from_json(cls, file_path: Union[Path, str]):
        with open(file_path, "r") as f:
            data_dict = json.load(f)
        return (
            cls(
                data_points=[
                    DataPoint.from_dict(dp) for dp in data_dict["data_points"]
                ],
                hyperparameters=HyperParameters.from_dict(
                    data_dict["hyperparameters"]
                ),
            )
            if "hyperparameters" in data_dict and data_dict["hyperparameters"] is not None
            else cls(
                data_points=[
                    DataPoint.from_dict(dp) for dp in data_dict["data_points"]
                ]
            )
        )

    @classmethod
    def from_dict(cls, data_dict: Dict):
        return cls(**data_dict)

    @property
    def number_data_points(self):
        return len(self.data_points)

    @property
    def radii(self):
        return [data_point.radius for data_point in self.data_points]

    @property
    def hartree_fock_energies(self):
        return [data_point.hartree_fock_energy for data_point in self.data_points]

    @property
    def classical_energies(self):
        return [data_point.classical_energy for data_point in self.data_points]

    @property
    def forged_vqe_energies(self):
        return [data_point.forged_vqe_energy for data_point in self.data_points]

    @property
    def schmidts_1(self):
        return [abs(data_point.schmidts_coefficients[0]) for data_point in self.data_points]

    @property
    def schmidts_larger(self):
        return [max(map(abs, data_point.schmidts_coefficients[1:])) for data_point in self.data_points]

    @property
    def schmidts_smaller(self):
        return [min(map(abs, data_point.schmidts_coefficients[1:])) for data_point in self.data_points]

    @property
    def mean_square_error_to_classical(self):
        return np.sqrt(
            sum((d.forged_vqe_energy - d.classical_energy)**2 for d in self.data_points) / self.number_data_points
        )

    @property
    def error_to_classical(self):
        return [
            abs(d.forged_vqe_energy - d.classical_energy) / 1e-3 for d in self.data_points
        ]
