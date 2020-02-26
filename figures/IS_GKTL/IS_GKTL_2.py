import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import erf

from jfm_paper import utils


def ret_gaussian(x):
    """ Returns zero-mean, unit variance at point
    """
    return (1.0 / (np.sqrt(2.0 * np.pi))) * np.exp(-0.5 * x * x)


musimga = np.fromfile("../..//data/musigma_AVG_10.dat", float, -1, "")

prefix = "../../data/"
gktl_dirs = ["er_lannic_1", "er_lannic_0", "er_lannic"]
gktl_dirs = [os.path.join(prefix, gktl_dir) for gktl_dir in gktl_dirs]

fig, ax = plt.subplots(figsize=(8, 5), constrained_layout=True)

for gktl_dir in gktl_dirs:
    gktl_params = utils.get_gktl_parameters(gktl_dir)
    df = utils.get_gktl_drag_trajectories(gktl_dir)
    traj = df.values
    gktl_params = utils.get_gktl_parameters(gktl_dir)
    A = [np.mean(traj[:, i]) for i in range(gktl_params["nc"])]

    k = gktl_params["k"]
    label = "$k = {:1.2f}$".format(k)
    n, bins, patches = plt.hist(A / musimga[1], 50, alpha=0.5, label=label)

binsize = bins[1] - bins[0]
nc = utils.get_gktl_parameters(gktl_dirs[0])["nc"]
A = np.sqrt(np.pi) * 0.5
mesh = np.arange(-5, 5, binsize)
hist = A * nc * (erf(mesh[1:]) - erf(mesh[:-1]))
midpoints = [0.5 * (b + a) for a, b in zip(mesh[:-1], mesh[1:])]
plt.bar(
    x=midpoints, height=hist, width=binsize, alpha=0.5, color="#808080", label="$k=0$"
)

plt.xlabel("$F_{T_a} / \\sigma_{T_a}$", fontsize=22)
plt.ylabel("#trajectories", fontsize=22)
ax.tick_params(axis="both", which="major", labelsize=16)
ax.legend(loc="best", fontsize=16)
plt.xlim((-2, 6))

fname = os.path.splitext(__file__)[0] + ".png"
plt.savefig(fname)

plt.show()
