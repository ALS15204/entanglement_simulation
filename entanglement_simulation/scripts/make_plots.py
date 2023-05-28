"""
This script is used to generate plots Fig 3B and Fig 4B for the paper.
"""
from pathlib import Path
import matplotlib.pyplot as plt

from entanglement_simulation.utils.experiment_data import ExperimentDataSet
from entanglement_simulation import (
    EXPERIMENT_DIR, WATER_DATA_FILE_PATH_A, WATER_DATA_FILE_PATH_B, WATER_DATA_FILE_PATH_C
)
from entanglement_simulation.water_molecule import create_water_data

PLOT_CONFIG = {
    "case_a": {
        "water_data": WATER_DATA_FILE_PATH_A,
        "x_label": "R ($\\AA$)",
        "x_lim": (0.5, 2.5),
        "y_lim": [(-75.75, -75.0), (0.1, 500), (1e-2, 2)],
    },
    "case_b": {
        "water_data": WATER_DATA_FILE_PATH_B,
        "x_label": "$R_2$ ($\\AA$)",
        "x_lim": (0.5, 2.5),
        "y_lim": [(-75.75, -75.30), (1, 100), (1e-3, 2)],
    },
    "case_c":
        {
        "water_data": WATER_DATA_FILE_PATH_C,
        "x_label": "$\\theta$ (deg)",
        "x_lim": (40, 180),
        "y_lim": [(-75.80, -75.45), (0.1, 500), (1e-2, 2)],
    }
}


def plot_directory(experiment_dir: Path):
    case, config = [(k, config) for k, config in PLOT_CONFIG.items() if k in experiment_dir.name][0]
    water_data = (
        ExperimentDataSet.from_json(PLOT_CONFIG[case]["water_data"])
        if PLOT_CONFIG[case]["water_data"].exists()
        else create_water_data()
    )
    plot_dir = experiment_dir / "plots/"
    plot_dir.mkdir(exist_ok=True)
    k3_data = ExperimentDataSet.from_json(experiment_dir / "best_fit/k3.json")
    k6_data = ExperimentDataSet.from_json(experiment_dir / "best_fit/k6.json")
    fig_3 = plt.figure(0, figsize=(6, 7))
    fig_3.suptitle(
        f"VQE energies [c0: {k3_data.hyperparameters.spsa_c0: .3f}; c1: {k3_data.hyperparameters.spsa_c1: .3f}]"
    )
    fig_3_subplots = fig_3.subplots(nrows=2, ncols=1, sharex=True, gridspec_kw={'height_ratios': [2, 1]})
    fig_3_subplots[0].plot(water_data.radii, water_data.hartree_fock_energies, label="HF")
    fig_3_subplots[0].plot(water_data.radii, water_data.classical_energies, label="FCI")
    fig_3_subplots[0].scatter(k3_data.radii, k3_data.forged_vqe_energies, label="k=3")
    fig_3_subplots[0].scatter(k6_data.radii, k6_data.forged_vqe_energies, label="k=6")
    fig_3_subplots[0].set_ylabel("energy (Ha)")
    fig_3_subplots[0].set_xlim(PLOT_CONFIG[case]["x_lim"])
    fig_3_subplots[0].set_ylim((PLOT_CONFIG[case]["y_lim"][0]))
    fig_3_subplots[0].legend()
    fig_3_subplots[1].scatter(k3_data.radii, k3_data.error_to_classical, label="k=3")
    fig_3_subplots[1].scatter(k6_data.radii, k6_data.error_to_classical, label="k=6")
    fig_3_subplots[1].set_xlabel(PLOT_CONFIG[case]["x_label"])
    fig_3_subplots[1].set_ylabel("|error| (mHa)")
    fig_3_subplots[1].set_ylim((PLOT_CONFIG[case]["y_lim"][1]))
    fig_3_subplots[1].set_yscale("log")
    fig_3.tight_layout()

    fig_4 = plt.figure(1, figsize=(6, 4))
    fig_4.suptitle(
        f"Schmidt coefficients [c0: {k3_data.hyperparameters.spsa_c0: .3f}; c1: {k3_data.hyperparameters.spsa_c1: .3f}]"
    )
    fig_4_subplots = fig_4.subplots(nrows=1, ncols=1)
    fig_4_subplots.plot(k3_data.radii, k3_data.schmidts_1, marker="o", label="$\lambda_1$")
    fig_4_subplots.plot(k3_data.radii, k3_data.schmidts_larger, marker="o", label="$\lambda_{>}$")
    fig_4_subplots.plot(k3_data.radii, k3_data.schmidts_smaller, marker="o", label="$\lambda_{<}$")
    fig_4_subplots.set_xlabel(PLOT_CONFIG[case]["x_label"])
    fig_4_subplots.set_ylabel("Schmidt coefficients")
    fig_4_subplots.set_xlim(PLOT_CONFIG[case]["x_lim"])
    fig_4_subplots.set_ylim((PLOT_CONFIG[case]["y_lim"][2]))
    fig_4_subplots.set_yscale("log")
    fig_4_subplots.legend()
    fig_4.tight_layout()
    return {f"fig_3{case[-1]}": fig_3, f"fig_4{case[-1]}": fig_4}


if __name__ == "__main__":
    experiment_dir = EXPERIMENT_DIR / "case_c_reduced_orbitals_0_3_k3"
    figures = plot_directory(experiment_dir)
    for key, fig in figures.items():
        figures[key].show()
        figures[key].savefig(experiment_dir / f"plots/{key}.png")
