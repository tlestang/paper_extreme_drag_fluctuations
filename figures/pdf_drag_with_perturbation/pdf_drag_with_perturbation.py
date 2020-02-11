import sys
from os.path import splitext

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


fig, ax = plt.subplots(constrained_layout=True, figsize=(8, 5))

series = pd.read_csv("../../data/PDF_drag_one_file.csv", comment="#", index_col=0)
series.plot(ax=ax, lw=2, legend=False)
series_perturb = pd.read_csv("../../data/PDF_drag_with_perturbation.csv", comment="#", index_col=0)
series_perturb.plot(ax=ax, lw=2, legend=False)

ax.set_xlabel("$(f_d - \\mu)/\\sigma$", fontsize=18)
ax.set_ylabel("$\\mathcal{P}$", fontsize=18)
ax.legend(["No perturbation", "$\\epsilon = 0.002$"], fontsize=18)

ax.set_yscale("log")
fname = splitext(__file__)[0] + ".png"
plt.savefig(fname)

plt.show()
