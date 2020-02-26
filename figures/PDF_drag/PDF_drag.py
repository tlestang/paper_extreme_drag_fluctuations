import sys
from os.path import splitext

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


fig, ax = plt.subplots()

series = pd.read_csv("../../data/PDF_drag.csv", comment="#", index_col=0)
series.plot(ax=ax, lw=2, legend=False)

series = pd.read_csv("../../data/PDF_drag_nosq.csv", comment="#", index_col=0)
series.plot(ax=ax, lw=2, legend=False)

# Plot gaussian distribution
xx = np.linspace(-4, 4, 50)
plt.plot(
    xx,
    (lambda x: np.exp(-x * x * 0.5) / np.sqrt(2 * np.pi))(xx),
    linestyle="--",
    color="k",
    linewidth=1.5,
)
plt.xlabel("$(f_d - \\mu)/\\sigma$", fontsize=18)
plt.ylabel("$\\mathcal{P}$", fontsize=18)
plt.legend(["With obstacle", "Without obstacle", "Gaussian estimate"], fontsize=18)
plt.yscale("log")
fname = splitext(__file__)[0] + ".png"
plt.savefig(fname)

plt.show()