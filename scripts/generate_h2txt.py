from openfermion.ops import FermionOperator
from openfermion.transforms import bravyi_kitaev

h_00 = h_11 = -1.252477
h_22 = h_33 = -0.475934
h_0110 = h_1001 = 0.674493
h_2332 = h_3323 = 0.697397
h_0220 = h_0330 = h_1221 = h_1331 = h_2002 = h_3003 = h_2112 = h_3113 = 0.663472
h_0202 = h_1313 = h_2130 = h_2310 = h_0312 = h_0132 = 0.181287

fermion_operator = FermionOperator("0^ 0", h_00)
fermion_operator += FermionOperator("1^ 1", h_11)
fermion_operator += FermionOperator("2^ 2", h_22)
fermion_operator += FermionOperator("3^ 3", h_33)

fermion_operator += FermionOperator("0^ 1^ 1 0", h_0110)
fermion_operator += FermionOperator("2^ 3^ 3 2", h_2332)
fermion_operator += FermionOperator("0^ 3^ 3 0", h_0330)
fermion_operator += FermionOperator("1^ 2^ 2 1", h_1221)

fermion_operator += FermionOperator("0^ 2^ 2 0", h_0220 - h_0202)
fermion_operator += FermionOperator("1^ 3^ 3 1", h_1331 - h_1313)

fermion_operator += FermionOperator("0^ 1^ 3 2", h_0132)
fermion_operator += FermionOperator("2^ 3^ 1 0", h_0132)

fermion_operator += FermionOperator("0^ 3^ 1 2", h_0312)
fermion_operator += FermionOperator("2^ 1^ 3 0", h_0312)

## Bravyi-Kitaev transformation
bk_operator = bravyi_kitaev(fermion_operator)

## output
fp = open("H2.txt", "w")
fp.write(str(bk_operator))
fp.close()
