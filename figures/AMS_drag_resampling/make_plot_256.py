import numpy as np
import matplotlib.pyplot as plt

plt.style.use('ggplot')
color_list = plt.rcParams['axes.prop_cycle'].by_key()['color']
# This scripts produces a figure that illustrates how the maximum over the resamplied trajectories
# saturates. It shows that that the TAMS does not lead to higher fluctuations, with respect to the
# initial ensemble of trajectories.
#
# Original data can be found in
# transition_hdd/thibault/These/AMS/libTAMS/tests/experience_lbm/courbe_efficacite_instant
# Original MATLAB script is make_plot_256.m

prefix = '/home/tlestang/transition_hdd/thibault/These/AMS/libTAMS/tests/experience_lbm/' \
        +'data/instant_256_20/'

# Defines average and std of drag process, compute over the control run
m = 0.0252
sig = 0.0412

# Defines relevant parameters of the TAMS experiment
Nc = 256;
Ta = 20;

# Opens file and read maxima on resampled trajectories
amax = (np.fromfile(prefix+'amax.dat')-m)/sig
Nresamp = len(amax)

# Creates a 1D array that contains the computational cost for each resamp. traj.
# It is over-evaluated as the formula below considers that each resamp. traj. was simulated
# over the full duration Ta
Cvec = Nc*Ta*np.ones(Nresamp) + Ta*np.arange(1,Nresamp+1)

# Init. figure
fig,ax = plt.subplots(figsize=(8,5), constrained_layout=True)

# Gathers the maxima over the initial ensemble
maxArray = np.zeros(Nc)
for j in range(0,Nc):
    f = np.fromfile(prefix+'traj_{:d}_costFunc_iter_0.dat'.format(j))
    maxArray[j]=(np.amax(f)-m)/sig
# Plots a line that represents the level of the highest fluctuation in
# the initial ensemble
M = np.amax(maxArray)
line, = ax.plot([Cvec[40], Cvec[Nresamp-1]], [M, M], '--', color=color_list[1])
# Plots the maxima for Cvec = Nc*Ta (initial computational cost)
init, = ax.plot(Nc*Ta*np.ones(Nc), maxArray, '+', linestyle='None')
init.set_markersize(5)
init.set_color(line.get_color())
init.set_label('Maxima over initial trajectories')

# Plots maxima over resampled trajectories
resamp, = ax.plot(Cvec, amax, linestyle='None')
resamp.set_marker('o')
resamp.set_markersize(3)
resamp.set_markerfacecolor(color_list[0]);
resamp.set_markeredgecolor(resamp.get_markerfacecolor())
resamp.set_label('Maxima over resampled trajectories')

ax.set_xscale('log')
ax.set_xlabel(r'$C_{TAMS} / \tau_c$',fontsize=22)
ax.set_ylabel(r'$f_d / \sigma$',fontsize=22)
ax.tick_params(axis="x", labelsize=18)
ax.tick_params(axis="y", labelsize=18)

ax.legend(loc='best', fontsize=18)

fname = 'AMS_drag_resampling.png'
plt.savefig(fname)

plt.show()
