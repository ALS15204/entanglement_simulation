from openfermion.transforms import get_fermion_operator, jordan_wigner
from openfermion.linalg import get_sparse_operator
from openfermion.chem import MolecularData
from openfermionpyscf import run_pyscf
from scipy.optimize import minimize
from scipy.sparse.linalg import eigsh
from pyscf import fci
import numpy as np
import matplotlib.pyplot as plt

import qulacs
from qulacs import Observable, QuantumState
from qulacs.observable import (
    create_observable_from_openfermion_text,
    create_observable_from_openfermion_file,
)


def classical_ground_state(
    radius_1: float = 0.958, radius_2: float = 0.958, thetas_in_deg: float = 104.478
) -> float:
    # radius_1 = 0.958  # position for the first H atom
    # radius_2 = 0.958  # position for the second H atom
    # thetas_in_deg = 104.478  # bond angles.

    H1_x = radius_1
    H2_x = radius_2 * np.cos(np.pi / 180 * thetas_in_deg)
    H2_y = radius_2 * np.sin(np.pi / 180 * thetas_in_deg)

    basis = "sto-6g"
    multiplicity = 1
    charge = 0
    geometry = [["O", [0, 0, 0]], ["H", [H1_x, 0, 0]], ["H", [H2_x, H2_y, 0]]]
    description = "h2o"
    molecule = MolecularData(geometry, basis, multiplicity, charge, description)
    molecule = run_pyscf(molecule, run_scf=False, run_fci=True)
    n_qubit = molecule.n_qubits
    n_electron = molecule.n_electrons
    fermionic_hamiltonian = get_fermion_operator(molecule.get_molecular_hamiltonian())
    jw_hamiltonian = jordan_wigner(fermionic_hamiltonian)
    hamiltonian_matrix = get_sparse_operator(jw_hamiltonian)
    eigval, eigvec = eigsh(hamiltonian_matrix, k=2, which="SA")
    qulacs_hamiltonian = create_observable_from_openfermion_text(str(jw_hamiltonian))
    state = QuantumState(n_qubit)
    state.set_Haar_random_state()
    value = qulacs_hamiltonian.solve_ground_state_eigenvalue_by_power_method(state, 10)
    return molecule.hf_energy, molecule.fci_energy, value


radii = np.arange(0.5, 2.5, 0.5)
values = np.array([classical_ground_state(radius_1=r) for r in radii])
plt.plot(radii, [v[0] for v in values], label="HF")
plt.plot(radii, [v[1] for v in values], label="FCI")
plt.plot(radii, [v[2] for v in values], label="Classical")
plt.legend()
plt.show()

