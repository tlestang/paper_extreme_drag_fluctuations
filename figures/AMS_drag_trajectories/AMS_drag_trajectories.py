import numpy as np
import matplotlib.pyplot as plt
from os.path import abspath, dirname, join, basename, splitext

plt.style.use('ggplot')

# This scripts produces a figure that illustrates how the resampled trajectories eventually
# concentrate on a unique trajectory. 
#
# Original data can be found in
# It shows that that the TAMS does not lead to higher fluctuations, with respect to the
# initial ensemble of trajectories.
# /home/thibault/transition_hdd/thibault/These/AMS/libTAMS/tests/experience_lbm/plots_instant_32_5/
# Original MATLAB script is plot_pre_extinct.m

prefix = '/home/tlestang/transition_hdd/thibault/These/AMS/libTAMS/tests/experience_lbm/' \
        +'data/instant_32_5/'

# Defines average and std of drag process, compute over the control run
m = 0.0252
sig = 0.0412

# Defines relevant parameters of the TAMS experiment
Nc = 32;
Ta = 5;

tspan = np.linspace(0,5,5000)
maxArray=np.zeros(Nc)
# Init. figure
fig,ax = plt.subplots(figsize=(8,5), constrained_layout=True)

for i in range(0,Nc):
    x = np.fromfile(prefix+'traj_{:d}_costFunc_iter_0.dat'.format(i))
    x=(x-m)/sig
    ax.plot(tspan, x, color='#006699',zorder=i+1)
    maxArray[i] = np.amax(x)

maxIdx = np.argmax(maxArray)
ax.lines[maxIdx].set_color('#cc0000')
ax.lines[maxIdx].set_linewidth(1.5)
ax.lines[maxIdx].set_linestyle('--')
ax.lines[maxIdx].set_zorder(Nc+1)
ax.lines[maxIdx].set_label('Initial traj. with the highest maximum')
print(maxIdx)
nbKilledTraj = np.fromfile(prefix+'nbKilledTraj.dat', dtype='int32')
killedTraj = np.fromfile(prefix+'killedTraj.dat', dtype='int32')
for t in range(1,182):
    for i in range(0,nbKilledTraj[t-1]):
        ktIdx = killedTraj[t+i-1]
        x = np.fromfile(prefix+'traj_{:d}_costFunc_iter_{:d}.dat'.format(ktIdx,t))
        x=(x-m)/sig
        ax.lines[ktIdx].set_ydata(x)

ax.set_xlabel(r'$t / \tau_c$',fontsize=22)
ax.set_ylabel(r'$f_d(t) / \sigma$',fontsize=22)
ax.tick_params(axis="x", labelsize=18)
ax.tick_params(axis="y", labelsize=18)

ax.legend(loc='best', fontsize=18)
ax.set_xlim((0,5))

fname = join(
    abspath(dirname(__file__)), basename(splitext(__file__)[0]) + ".eps"
    )
plt.savefig(fname)

