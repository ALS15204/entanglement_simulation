"""
This script is used to generate plots Fig 3B and Fig 4B for the paper.
"""
from pathlib import Path
import matplotlib.pyplot as plt

from entanglement_simulation.utils.experiment_data import ExperimentDataSet
from entanglement_simulation import EXPERIMENT_DIR, WATER_DATA_FILE_PATH
from entanglement_simulation.water_molecule import create_water_data


def plot_directory(experiment_dir: Path):
    water_data = (
        ExperimentDataSet.from_json(WATER_DATA_FILE_PATH)
        if WATER_DATA_FILE_PATH.exists()
        else create_water_data()
    )
    plot_dir = experiment_dir / "plots/"
    plot_dir.mkdir(exist_ok=True)
    k3_data = ExperimentDataSet.from_json(experiment_dir / "best_fit/k3.json")
    k6_data = ExperimentDataSet.from_json(experiment_dir / "best_fit/k6.json")
    fig_3b = plt.figure(0, figsize=(6, 7))
    fig_3b.suptitle(
        f"VQE energies [c0: {k3_data.hyperparameters.spsa_c0: .3f}; c1: {k3_data.hyperparameters.spsa_c1: .3f}]"
    )
    fig_3b_subplots = fig_3b.subplots(nrows=2, ncols=1, sharex=True, gridspec_kw={'height_ratios': [2, 1]})
    fig_3b_subplots[0].plot(water_data.radii, water_data.hartree_fock_energies, label="HF")
    fig_3b_subplots[0].plot(water_data.radii, water_data.classical_energies, label="FCI")
    fig_3b_subplots[0].scatter(k3_data.radii, k3_data.forged_vqe_energies, label="k=3")
    fig_3b_subplots[0].scatter(k6_data.radii, k6_data.forged_vqe_energies, label="k=6")
    fig_3b_subplots[0].set_ylabel("energy (Ha)")
    fig_3b_subplots[0].set_xlim((0.5, 2.5))
    fig_3b_subplots[0].set_ylim((-75.75, -75.30))
    fig_3b_subplots[0].legend()
    fig_3b_subplots[1].scatter(k3_data.radii, k3_data.error_to_classical, label="k=3")
    fig_3b_subplots[1].scatter(k6_data.radii, k6_data.error_to_classical, label="k=6")
    fig_3b_subplots[1].set_xlabel("$R_2$ ($\\AA$)")
    fig_3b_subplots[1].set_ylabel("|error| (mHa)")
    fig_3b_subplots[1].set_ylim((1., 100))
    fig_3b_subplots[1].set_yscale("log")
    fig_3b.tight_layout()

    fig_4b = plt.figure(1, figsize=(6, 4))
    fig_4b.suptitle(
        f"Schmidt coefficients [c0: {k3_data.hyperparameters.spsa_c0: .3f}; c1: {k3_data.hyperparameters.spsa_c1: .3f}]"
    )
    fig_4b_subplots = fig_4b.subplots(nrows=1, ncols=1)
    fig_4b_subplots.plot(k3_data.radii, k3_data.schmidts_1, marker="o", label="$\lambda_1$")
    fig_4b_subplots.plot(k3_data.radii, k3_data.schmidts_larger, marker="o", label="$\lambda_{>}$")
    fig_4b_subplots.plot(k3_data.radii, k3_data.schmidts_smaller, marker="o", label="$\lambda_{<}$")
    fig_4b_subplots.set_xlabel("$R_2$ ($\\AA$)")
    fig_4b_subplots.set_ylabel("Schmidt coefficients")
    fig_4b_subplots.set_xlim((0.5, 2.5))
    fig_4b_subplots.set_ylim((1e-3, 2))
    fig_4b_subplots.set_yscale("log")
    fig_4b_subplots.legend()
    fig_4b.tight_layout()
    return {"fig_3b": fig_3b, "fig_4b": fig_4b}


if __name__ == "__main__":
    experiment_dir = EXPERIMENT_DIR / "case_b_reduced_orbitals_0_3_k3"
    figures = plot_directory(experiment_dir)
    figures["fig_3b"].show()
    figures["fig_4b"].show()
    for fig_name, fig in figures.items():
        fig.savefig(experiment_dir / f"plots/{fig_name}.png")