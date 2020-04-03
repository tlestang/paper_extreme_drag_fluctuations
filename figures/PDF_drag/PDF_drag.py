import sys
from os.path import splitext
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from os.path import abspath, dirname, join, basename, splitext

fig, ax = plt.subplots(constrained_layout=True)

prefix = join(
    abspath(dirname(__file__)), "data"
    )

series = pd.read_csv(join(prefix, "PDF_drag.csv"), comment="#", index_col=0)
series.plot(ax=ax, lw=2, legend=False)

series = pd.read_csv(join(prefix, "PDF_drag_nosq.csv"), comment="#", index_col=0)
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
plt.xlabel("$x=(f_d - \\mu)/\\sigma$", fontsize=20)
plt.ylabel("$P(x)$", fontsize=20)
plt.legend(["With obstacle", "Without obstacle", "Gaussian estimate"], fontsize=18)
plt.yscale("log")

fname = join(
    abspath(dirname(__file__)), basename(splitext(__file__)[0]) + ".eps"
    )

plt.savefig(fname)
