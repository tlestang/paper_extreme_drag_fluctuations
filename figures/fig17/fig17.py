from os.path import join
import numpy as np
import matplotlib.pyplot as plt
from os.path import abspath, dirname, join, basename, splitext
from pathlib import PurePath

plt.style.use('ggplot')

main_data_path = PurePath(abspath(dirname(__file__))).parent.parent / "data"
prefix = join(
    abspath(dirname(__file__)), "data"
    )

gktl_dir = join(str(main_data_path), "er_lannic")

# list.txt is generated with ./sort_extremes.py
# contains the sorted list of extremes according to the
# time-averaged drag (highest value first)
sortedI = np.loadtxt(join(prefix, "list.txt"), dtype=int)

sig=0.0412
m=0.0252
# Gets the value of mu and sigma for time-averaged drag
musigma = np.fromfile(join(str(main_data_path), "musigma_AVG_10.dat"), float, -1, "");

T = 10 # Physical duration of instant. trajectories

Nsubplots = 6
minArray=np.zeros(Nsubplots) # containers for max and min over instant. drag
maxArray=np.zeros(Nsubplots) # timeseries
fig, axes = plt.subplots(nrows=2,ncols=3, figsize=(18,6), constrained_layout=True)
for i in range(0,Nsubplots):
    fileName=join(gktl_dir, "recon_rep_0_clone_{}.traj".format(sortedI[i]))
    f = np.fromfile(fileName, float, -1, "")
    # amplitude of fluctuation for time-average
    F_avg = np.sum(f)/(len(f)-1)
    F_avg = F_avg/musigma[1]
    # Compute centered and reduced drag
    # important to do this *after* computing F_avg
    f = f/sig
    N = len(f)
    # row and col are computed so that plots go from left
    # to right, in descending order of F_avg
    row = i // 3
    col = i % 3
    drag_signal, = axes[row,col].plot(np.linspace(0,T,N),f)
    axes[row,col].set_xlim((0, T))
    axes[row,col].set_title(r"$F_T = {:2.1f}\sigma _T$".format(F_avg), fontsize=26)
    # Compute min and max for instant drag signal to
    # impose common ylim to all subplots (see below)
    maxArray[i]=np.amax(f)
    minArray[i]=np.amin(f)
    # Plot a dashed line to mark average value (f=0)
    avg_marker_line, = axes[row,col].plot([0,T],[0,0], '--')
    avg_marker_line.set_color(drag_signal.get_color())
    if(i==0):
        avg_marker_line.set_label(r'$\langle f_d \rangle$')
        axes[row,col].legend(loc='upper left', fontsize=22)
globalDragMinimum = np.amin(minArray)
globalDragMaximum = np.amax(maxArray)
for i in range(0,6):
    row = i // 3
    col = i % 3
    axes[row,col].set_ylim((globalDragMinimum,globalDragMaximum))
    axes[row,col].set_xlabel(r'$t/ \tau_c$',fontsize=28)
    axes[row,col].set_ylabel(r'$f_d(t)$',fontsize=28)
    axes[row,col].set_yticks([0,2,4,6])
    axes[row,col].set_yticklabels(['${:2.0f}\\sigma$'.format(x) \
                                   for x in axes[row,col].get_xticks()])
    axes[row,col].tick_params(axis='both', which='major', labelsize=22)

fname = join(
    abspath(dirname(__file__)), basename(splitext(__file__)[0]) + ".eps"
    )
plt.savefig(fname)
