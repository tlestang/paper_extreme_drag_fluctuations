import os
import numpy as np
import argparse
import matplotlib.pyplot as plt

from jfm_paper import utils
from jfm_paper.resimulate_extreme_GKTL import resimulate

description = "Sort trajectories sampled by the GKTL algorithm according to the value of the maximum drag."
parser = argparse.ArgumentParser(description=description)
parser.add_argument(
    "directory",
    type=str,
    help="Location of GKTL directory relative to the current directory.",
)
parser.add_argument(
    "--resimulate",
    action="store_true",
    help="Whether or not to carry on resimulation of trajectories.",
)

args = parser.parse_args()

musimga = np.fromfile(
    "/home/tlestang/articles/jstat_paper/data/musigma_AVG_10.dat", float, -1, ""
)
sig = 0.0412  # Standard deviation of instant. drag computed over CR
m = 0.0252  # Average instant. drag computed over CR

# Now group together trajectories that overlap over more than 50% of their
# total duration.
# In this example the GKTL run consists in 30 steps and the actual trajectories
# studied are the last 20 steps.
# So we want to group together the trajectories that share a common ancestor at step 30 - 20/2 = 20
dict_of_parents = utils.gktl_group_trajectories(args.directory, br_end=29, br_start=20)
# dict_of_parents is a dict which entries are a list of overlapping trajs.
# Loops on group of trajectories

traj_idx = []  # Indices of trajectories sorted
drag_maxima = []  # Container for the average drag
for counter, common_ancestor_idx in enumerate(dict_of_parents):
    # for each group, get index of traj with the highest average
    drag_maxima_ingroup = []
    group_of_trajs = dict_of_parents[common_ancestor_idx]
    for jj in group_of_trajs:
        fileName = os.path.join(args.directory, "recon_rep_0_clone_{}.traj".format(jj))
        # Reads instant. drag
        drag_maxima_ingroup.append(np.amax(np.fromfile(fileName, float, -1, "")))

    j = group_of_trajs[
        np.argmax(drag_maxima_ingroup)
    ]  # Pick traj with the largst maximum in group
    traj_idx.append(j)
    drag_maxima.append(np.amax(drag_maxima_ingroup))

with open("extremes.csv", "w") as f:
    for i, idx in enumerate(np.argsort(-np.array(drag_maxima))):
        f.write("{},{}\n".format(traj_idx[idx], drag_maxima[idx] / sig))
if args.resimulate:
    for i, idx in enumerate(np.argsort(-np.array(drag_maxima))):
        print(
            "Resimulating trajectory {} ({}/{})".format(
                traj_idx[idx], i, len(drag_maxima)
            )
        )
        resimulate(args.directory, traj_idx[idx])
        event_dir = os.path.join(args.directory, "event_{}".format(traj_idx[idx]))
        if not os.path.isdir(event_dir):
            os.mkdir(event_dir)
        for filename in ["ux.dat", "uy.dat", "rho.dat", "dragFile.dat"]:
            os.rename(filename, os.path.join(event_dir, filename))
            print("Moved {} to {}".format(filename, os.path.join(event_dir, filename)))
