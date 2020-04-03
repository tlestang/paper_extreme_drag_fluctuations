import sys
from os.path import splitext

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


fig, ax = plt.subplots(constrained_layout=True, figsize=(8, 5))

series = pd.read_csv("../../data/PDF_drag.csv", comment="#", index_col=0)
trunc_series = series.iloc[np.where((series.index.values > -6.5) & (series.index.values < 8.5))] 
trunc_series.plot(ax=ax, lw=2, legend=False)
series_perturb = pd.read_csv("../../data/PDF_drag_with_perturbation.csv", comment="#", index_col=0)
series_perturb.plot(ax=ax, lw=2, legend=False)

ax.set_xlabel("$x=(f_d - \\mu)/\\sigma$", fontsize=22)
ax.set_ylabel("$P(x)$", fontsize=22)
ax.legend(["No perturbation", "$\\epsilon = 0.002$"], fontsize=18)
ax.tick_params(axis='both', which='major', labelsize=18)

ax.set_yscale("log")
fname = splitext(__file__)[0] + ".eps"
plt.savefig(fname)

plt.show()
