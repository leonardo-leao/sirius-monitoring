# Author: Leonardo Rossi Leão
# E-mail: leonardo.leao@cnpem.br

import warnings                         # Filter warning messages
import numpy as np                      # Numerical computing tools
from scipy.stats import norm            # A normal continuous random variable
from actions.math import Math           # Mathematical functions
import matplotlib.pyplot as plt         # Plot options
import matplotlib.dates as mdates       # Matplotlib date formatter

# The savefig option generates warnings every time it is executed by a thread
warnings.filterwarnings("ignore")

class Plot():

    """ Plot templates """

    @staticmethod
    def telegram(x: list, y: list, options: dict) -> None:

        """
            Plot formatting template to forward on telegram

            x: x-axys values
            y: y-axys values
            options: {xIsDate: bool, savefig: bool}
        """

        fig = plt.figure(figsize=(10, 4))

        signal    = plt.subplot2grid(shape=(1,3), loc=(0,0), colspan=2)
        histogram = plt.subplot2grid(shape=(1,3), loc=(0,2), colspan=1)

        # Signal plot
        signal.plot(x, y, label=options["pv"])
        regression = Math.linearRegression(y, 10)
        signal.plot(x, regression)
        signal.grid(visible=True, linestyle='--', color='#D3D3D3')
        signal.set_ylabel("Temperature [°C]")
        signal.set_xlim(x[0], x[-1])
        signal.legend()

        # Histrogram plot
        mu, std = norm.fit(y)
        min_y, max_y = min(y), max(y)
        gaussian_x = np.linspace(min_y, max_y, 100)
        bins = np.arange(min_y, max_y, 0.01)
        histogram.hist(y, bins, weights=np.ones(len(y))/len(y), alpha=0.9)
        histogram.plot(gaussian_x, norm.pdf(gaussian_x, mu, std)/100)
        histogram.set_ylabel("Percentage [%]")

        if options['xIsDate']:
            signal.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

        
        plt.tight_layout()
        plt.savefig(options['savefig'])

