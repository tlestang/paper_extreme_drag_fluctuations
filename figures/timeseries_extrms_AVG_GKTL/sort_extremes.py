# Reads the N = 85 drag signals corresponding the the extreme fluctuations
# of the average drag.
# + It sorts the events according to the fluctuations amplitude (AVG drag)
# + It computes the upper and lower bounds of the instant drag over all events.

# Outputs a formatted text file consiting of N lines.
# Next N lines are index of event sorted in descending order
# (most extreme event first)
# Prints max and min over instant timeseries to stdout

from os.path import join
import numpy as np
import matplotlib.pyplot as plt

from jfm_paper import utils

gktl_dir = "../../data/er_lannic"

musimga = np.fromfile(
    "../../data/musigma_AVG_10.dat", float, -1, ""
)
sig=0.0412 # Standard deviation of instant. drag computed over CR
m=0.0252 # Average instant. drag computed over CR

# Now group together trajectories that overlap over more than 50% of their
# total duration.
# In this example the GKTL run consists in 30 steps and the actual trajectories
# studied are the last 20 steps.
# So we want to group together the trajectories that share a common ancestor at step 30 - 20/2 = 20
dict_of_parents = utils.gktl_group_trajectories(gktl_dir, br_end=29, br_start=15)
# dict_of_parents is a dict which entries are a list of overlapping trajs.
# Loops on group of trajectories

traj_idx = [] # Indices of trajectories sorted
F = [] # Container for the average drag
for counter, common_ancestor_idx in enumerate(dict_of_parents):
    # for each group, get index of traj with the highest average
    FF = []
    group_of_trajs = dict_of_parents[common_ancestor_idx]
    for jj in group_of_trajs:
        fileName=join(gktl_dir,"recon_rep_0_clone_{}.traj".format(jj))
        # Reads instant. drag
        f = np.fromfile(fileName, float, -1, "")
        FF.append(np.mean(f))
    
    j = group_of_trajs[np.argmax(FF)] # Pick first traj in the list
    traj_idx.append(j)
    fileName=join(gktl_dir,"recon_rep_0_clone_{}.traj".format(j))
    # Reads instant. drag
    f = np.fromfile(fileName, float, -1, "")
    F.append(np.mean(f))

np.savetxt('list.txt', [traj_idx[ii] for ii in np.argsort(-np.array(F))], '%0.2d')

