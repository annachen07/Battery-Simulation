import numpy as np

from model.ecm import ECM


t = np.arange(1000)
I = np.ones(len(t))
R_0 = 2e-6
R_1 = 2e-9
C_1 = 100
z_0 = 0.5
Q = 1.5
file_path = "/Users/annachen/PycharmProjects/batterysimulation/data/OCV_discharge.csv"
i_r1 = 0

sim1 = ECM(t, I, R_0, R_1, C_1, z_0, file_path, Q, i_r1)
print(sim1.t)
print(sim1.I)
print(sim1.R_0)
print(sim1.R_1)
print(sim1.C_1)
print(sim1.z_0)
print(sim1.file_path)
print(sim1.calc_ocv(0.5))
print(sim1.calc_SOC(1, 0, 0.5, 1))
print(sim1.solve())
print(np.exp(1))
print(sim1.solve())