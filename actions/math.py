# Author: Leonardo Rossi Leão
# E-mail: leonardo.leao@cnpem.br

import numpy as np
from sklearn.linear_model import LinearRegression
from scipy.stats import pearsonr, spearmanr, kendalltau
from scipy.signal import correlate, correlation_lags, butter, filtfilt
from scipy.signal.windows import hamming

class Math():

    @staticmethod
    def avg(y: list) -> float:
        return sum(y)/len(y)

    @staticmethod
    def std(y: list) -> float:
        return np.std(y)

    @staticmethod
    def linearRegression(y: list, minutes: float) -> list:
        model = LinearRegression()
        step = minutes/len(y)
        x = np.array([i*step for i in range(len(y))]).reshape((-1, 1))
        model.fit(x, y)
        return model.predict(x)

    @staticmethod
    def fft(x: list, y: list) -> tuple:

        """
            Calculates the discrete fourier transform of a signal

            x: timeseries
            y: signal to apply fft
        """

        nsamp = len(y)
        fs = 1/(x[1]-x[0]).total_seconds()
        xf = np.fft.fftfreq(nsamp, 1/fs)[:nsamp//2]
        yf = abs(np.fft.fft(y)[:nsamp//2])*2/nsamp

        return xf, yf