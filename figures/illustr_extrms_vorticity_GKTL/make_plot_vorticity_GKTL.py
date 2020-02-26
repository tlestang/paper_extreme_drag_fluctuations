# Produces a figure illustrating the vorticity field at the moment of peak drag for 7 events.
# The figure consists of 7 axes. One axes is four times bigger as the others, and contains
# annotations
import os
import numpy as np
import csv
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

Dx = 513
Dy = 129
N = Dx * Dy
F = []
idx = []
gktl_dir = "../../er_lannic"
# Files extremes.csv contains the index of the events and the corresponding
# peak drag amplitude, in units of sigma
# First row is highest fluctuation
with open("extremes.csv", mode="r") as extremes_file:
    extremes_reader = csv.reader(extremes_file, delimiter=",")
    for _idx, _F, t_star in extremes_reader:
        idx.append(int(_idx))
        F.append(float(_F))

fig = plt.figure(figsize=(16, 6), constrained_layout=True)
# Declares a 2x5 grid.
# the last axes spans 4 cells
grid = plt.GridSpec(2, 5, figure=fig)
for i in range(0, 4):
    plt.subplot(grid[0, i])
    plt.subplot(grid[1, i])
plt.subplot(grid[0:, 3:])

fig = plt.gcf()
ax_list = fig.axes
Nevents = len(ax_list)

for i in range(0, Nevents):
    path_to_file_ux = os.path.join(gktl_dir, "event_{:d}/ux.dat".format(idx[i]))
    path_to_file_uy = os.path.join(gktl_dir, "event_{:d}/uy.dat".format(idx[i]))

    nb_snapshots = os.path.getsize(path_to_file_ux) // N // 8

    # Opens the files and jump to peak drag
    # (middle of timeseries)
    # Get velocity fields
    ux = np.fromfile(path_to_file_ux, float, N, "", offset=(nb_snapshots // 2 - 1) * N * 8)
    ux = np.reshape(ux, (129, 513), "F")
    uy = np.fromfile(path_to_file_uy, float, N, "", offset=(nb_snapshots // 2 - 1) * N * 8)
    uy = np.reshape(uy, (129, 513), "F")

    ymin = 32
    ymax = 96
    xmin = 236
    xmax = 310
    # Compute vorticity using finite-differences
    dxy = (
        uy[ymin:ymax, xmin + 1 : xmax + 1] - uy[ymin:ymax, xmin - 1 : xmax - 1]
    ) * 0.5
    dyx = (
        ux[ymin + 1 : ymax + 1, xmin:xmax] - ux[ymin - 1 : ymax - 1, xmin:xmax]
    ) * 0.5
    vort = dxy - dyx
    # The sign of the vorticity is wrong if using a right-handed coord. system.
    # The velocity field should probably be flipped upside-down
    vort = -vort

    # Print fluctuation amplitude as title
    tit = "{:2.1f}$\\sigma$".format(F[i])
    ax_list[i].set_title(tit, fontsize=22)
    # Print vorticity field
    im = ax_list[i].imshow(
        vort, interpolation="spline36", cmap="BrBG", vmin=-0.1, vmax=0.1
    )
    # Adds a filled Rectangle to mark the square obstacle
    rect = ax_list[i].add_artist(Rectangle((21, 25), 14, 14))
    rect.set_color("#545454")

    # Write ticks and labels
    xticks = ax_list[i].get_xticks()
    xticks[:] = [(x + xmin) / 17 for x in xticks]
    xticklabels = ["{:2.1f}".format(x) for x in xticks]
    ax_list[i].set_xticklabels(xticklabels, fontsize=16)
    yticks = ax_list[i].get_yticks()
    yticks[:] = [(x + ymin) / 17 for x in yticks]
    yticklabels = ["{:2.1f}".format(x) for x in yticks]
    ax_list[i].set_yticklabels(yticklabels[::-1], fontsize=16)

    ax_list[i].set_xlabel(r"$x/R$", fontsize=22)
    ax_list[i].set_ylabel(r"$y/R$", fontsize=22)

cbar = fig.colorbar(im, ax=ax_list)
cbar.ax.tick_params(labelsize=16)

fname = "illustr_extrms_vorticity.png"
plt.savefig(fname)

plt.show()
