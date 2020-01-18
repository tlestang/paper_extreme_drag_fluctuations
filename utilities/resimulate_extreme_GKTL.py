# This script simulates the flow around the point of maximum drag for a given
# trajectory sampled by the GKTL algorithm.
# Usage:
# python resimulate_extreme_GKTL.py <gktl_dir> <index_of_trajectory>
# where <gktl_dir> is the path to the GKTL experiemt directory relative
# to the current working dir and <index_of_trajectory> is an integer.
# If non existent, will create a directory extreme_traj_x
# in current working dir.

import os
import numpy as np
import simulate
from jfm_paper import utils


tau_c = 2000
Dx = 513
Dy = 129
traj_index = 0
gktl_dir = "../resimul_test"
vis_window = 4 * tau_c

# Read the drag signal
filename = os.path.join(gktl_dir, "recon_rep_0_clone_{}.traj".format(traj_index))
drag_signal = np.fromfile(filename, float, -1, "")

gktl_params = utils.get_gktl_parameters(gktl_dir)
DT = gktl_params["DT"]

# Compute time points
t_star = np.argmax(drag_signal)
tvismin = t_star-vis_window//2
tvismax = t_star+vis_window//2
if tvismin<0:
    print("ERROR: tvismin<0")
if tvismax>gktl_params["Ta"]-1:
    print("ERROR: tvismax > Ta")

step_min = tvismin // DT
step_max = tvismax // DT

# Get population file
history = utils.gktl_reconstruct_trajectories(gktl_dir, br_end=29, br_start=0, rep=0)

for step in range(step_min, step_max + 1):
    print(step)
    ancestor_idx = history[traj_index][step]
    filename = "rep_0_clone_{}.bin".format(ancestor_idx) 
    with open(os.path.join(gktl_dir, filename), "rb") as f:
        np.fromfile(
            f,
            float,
            Dx * Dy * 9,
            "",
            offset=step * Dx * Dy * 9 * np.dtype(float).itemsize,
        ).tofile("init_state.bin")
    tmin = step * DT
    tmax = (step + 1) * DT - 1
    simulate.simulate("init_state.bin", tmin, tmax, tvismin, tvismax)
