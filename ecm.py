import numpy as np
import pandas as pd
import scipy as sci


class ECM:
    def __init__(self, t, I, R_0, R_1, C_1, z_0, file_path, Q, i_r1):
        '''
        initialzation function
        :param t: time array
        :param I: current array
        :param R_0: internal resistance
        :param R_1: RC resistance
        :param C_1: capacitor resistance
        :param z_0: initial SOC
        :param file_path: filepath for SOC_OCV data
        '''
        self.t = t
        self.I = I
        self.R_0 = R_0
        self.R_1 = R_1
        self.C_1 = C_1
        self.z_0 = z_0
        self.file_path = file_path
        self.Q = Q
        self.i_r1 = i_r1

    def calc_ocv(self, soc):
        df = pd.read_csv(self.file_path)
        ocv = df['V']
        soc_array = df['cap_discharge']

        return sci.interpolate.interp1d(soc_array, ocv)(soc)

    def calc_SOC(self, t_curr, t_prev, soc_prev, curr):
        # calc delta_t
        delta_t = t_curr - t_prev
        return soc_prev - delta_t * curr / (self.Q * 3600)

    def solve(self):
        # soc
        soc_array = np.zeros(len(self.t))
        soc_array[0] = self.z_0
        v_array = np.zeros(len(self.t))
        for i, t in enumerate(self.t):
            if i > 0:
                soc_array[i] = self.calc_SOC(t, self.t[i-1], soc_array[i-1], self.I[i])
                delta_t = t - self.t[i-1]
                self.i_r1 = np.exp(-delta_t/(self.R_1 * self.C_1))*self.i_r1 + (1-np.exp(-delta_t/ (self.R_1 * self.C_1))) * self.I[i-1]
                v_array[i] = self.calc_ocv(soc_array[i]) - self.R_1 * self.i_r1 - self.R_0 * self.I[i-1]
        return v_array

        #soc_array = np.zeros(len(self.t))
         #soc_array[0] = self.z_0
        #for i, t in enumerate(self.t):
            #if i > 0:
                #soc_array[i] = self.calc_SOC(t, self.t[i-1], soc_array[i-1], self.I[i])
        # solve i_R1

        # solve for v
        return soc_array

