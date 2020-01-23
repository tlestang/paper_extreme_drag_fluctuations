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
import argparse
import simulate
from jfm_paper import utils


def resimulate(gktl_dir, traj_index):
    tau_c = 2000
    vis_window = 4 * tau_c

    # Read the drag signal
    filename = os.path.join(gktl_dir, "recon_rep_0_clone_{}.traj".format(traj_index))
    drag_signal = np.fromfile(filename, float, -1, "")

    gktl_params = utils.get_gktl_parameters(gktl_dir)
    DT = gktl_params["DT"]

    # Pressure, velocities and drag will be recorded for tvismin <= t <= tvismax
    t_star = np.argmax(drag_signal)
    tvismin = t_star - vis_window // 2  # Min visualisation boundary window
    tvismax = t_star + vis_window // 2  # Max visualisation boundary window
    if tvismin < 0:
        msg = "Warning, minimum visualisation boundary is < 0. Its value is: {}".format(
            tvismin
        )
        print(msg)
        print("Resimulating from t = 0")
        tvismin = 0
    if tvismax > len(drag_signal) - 1:
        msg = "Warning, maximum visualisation boundary is beyond endpoint of trajectory. Its value is: {}".format(
            tvismax
        )
        print(msg)
        tvismax = len(drag_signal) - 1
        print("Resimulating until tvismax = {}".format(tvismax))

    # Compute starting and end GKTL states
    step_min = tvismin // DT
    step_max = tvismax // DT

    # Compute history for trajectory
    history = utils.gktl_reconstruct_trajectories(
        gktl_dir, br_end=29, br_start=10, rep=0
    )

    # Now do resimulation
    # Dimensions of the lattice, required to compute the size of a state.
    Dx = 513
    Dy = 129
    for step in range(step_min, step_max + 1):
        ancestor_idx = history[traj_index][step]
        filename = "rep_0_clone_{}.bin".format(ancestor_idx)
        # Get initial populations from GKTL ouput file
        # and write it back to disk in a separate file.
        # This is necessary to feed it into the simulate module
        with open(os.path.join(gktl_dir, filename), "rb") as f:
            np.fromfile(
                f,
                float,
                Dx * Dy * 9,
                "",
                offset=(step + 10) * Dx * Dy * 9 * np.dtype(float).itemsize,
            ).tofile("init_state.bin")
            # Simulate flow for this GKTL step
            tmin = step * DT
            tmax = (step + 1) * DT - 1
            simulate.simulate("init_state.bin", tmin, tmax, tvismin, tvismax)


if __name__ == "__main__":
    description = "(re)Simulate the flow locally around maximum of trajectory sampled in a GKTL run."
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        "directory",
        type=str,
        help="GKTL directory location relative to current directory.",
    )
    parser.add_argument(
        "traj_index",
        metavar="j",
        type=int,
        help="The index of the trajectory to simulate.",
    )
    args = parser.parse_args()

    resimulate(args.directory, args.traj_index)
