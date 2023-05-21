import json
import pickle
import matplotlib.pyplot as plt
import numpy as np

radii_1 = np.linspace(0.5, 2.5, 50)
with open("water_data.json", "r") as f:
    water_data = json.load(f)
with open("../experiment_results/experiment_11/reports_k6.pickle", "rb") as f:
    reports_6k = pickle.load(f)
with open("../experiment_results/experiment_11/reports_k3.pickle", "rb") as f:
    reports_3k = pickle.load(f)

plt.plot(
    [data["radius"] for data in water_data],
    [data["hartree_fock_energy"] for data in water_data],
    label="HF",
)
plt.plot(
    [data["radius"] for data in water_data],
    [data["classical_energy"] for data in water_data],
    label="FCI",
)
plt.scatter(
    [r["radius"] for r in reports_6k],
    [r["forged_result"].ground_state_energy for r in reports_6k],
    label="k=6",
)
plt.scatter(
    [r["radius"] for r in reports_3k],
    [r["forged_result"].ground_state_energy for r in reports_3k],
    label="k=3",
)
plt.xlabel("radius of H1")
plt.ylabel("energy")
plt.xlim((0.5, 2.5))
plt.ylim((-75.75, -75.3))
plt.legend()
plt.show()

# plt.plot(
#     [r for r, rep in zip(radii_1, reports_3k) if rep["forged_result"]],
#     [-r["forged_result"].schmidts_value[0] for r in reports_3k if r["forged_result"]],
#     label="lambda_1",
#     marker=".",
# )
# plt.plot(
#     [r for r, rep in zip(radii_1, reports_3k) if rep["forged_result"]],
#     [r["forged_result"].schmidts_value[1] for r in reports_3k if r["forged_result"]],
#     label="lambda_2",
#     marker=".",
# )
# plt.plot(
#     [r for r, rep in zip(radii_1, reports_3k) if rep["forged_result"]],
#     [r["forged_result"].schmidts_value[2] for r in reports_3k if r["forged_result"]],
#     label="lambda_3",
#     marker=".",
# )
# # plt.plot(
# #     [r for r, rep in zip(radii_1, reports) if rep["forged_result"]],
# #     [-r["forged_result"].schmidts_value[3] for r in reports if r["forged_result"]],
# #     label="lambda_4",
# #     marker=".",
# # )
# # plt.plot(
# #     [r for r, rep in zip(radii_1, reports) if rep["forged_result"]],
# #     [r["forged_result"].schmidts_value[4] for r in reports if r["forged_result"]],
# #     label="lambda_5",
# #     marker=".",
# # )
# plt.xlabel("radius of H1")
# plt.ylabel("Schmidt coefficients")
# plt.xlim((0.5, 2.5))
# plt.ylim((1e-3, 2))
# plt.yscale("log")
# plt.legend()
# plt.show()
