# Produces a figure illustrating the vorticity field at the moment of peak drag for 7 events.
# The figure consists of 7 axes. One axes is four times bigger as the others, and contains 
# annotations
import numpy as np
import csv
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

Dx = 513
Dy = 129
N = Dx*Dy
F = np.zeros(104)
idx = np.zeros(104)

prefix = "/home/tlestang/transition_hdd/thibault/These/lbm_code/seq/draft/etude_dynamique/instant_events/"
# Files extremes.csv contains the index of the events and the corresponding
# peak drag amplitude, in units of sigma
# First row is lowest fluctuation
with open(prefix+'extremes.csv', mode='r') as extremes_file:
        extremes_reader = csv.reader(extremes_file, delimiter=',')
        line_count=0
        for row in extremes_reader:
            idx[line_count]=row[0]
            F[line_count]=row[1]
            line_count += 1

fig = plt.figure(figsize=(16,7), constrained_layout=True)
# Declares a 2x5 grid.

grid = plt.GridSpec(2, 5, figure=fig)
for i in range(0,5):
    plt.subplot(grid[0,i])
    plt.subplot(grid[1,i])

ax_list = fig.axes
nplots = len(ax_list)

path_to_file_ux = prefix+'event_{:d}_feb/ux.dat'.format(int(idx[1]+1))
path_to_file_uy = prefix+'event_{:d}_feb/uy.dat'.format(int(idx[1]+1))
fx = open(path_to_file_ux, "rb")  # reopen the file
fy = open(path_to_file_uy, "rb")  # reopen the file
bbox = dict(boxstyle="round", fc="0.9")
for i in range(0,nplots):
        # trick to advance in time with row major ordering
        I = 2*(i%5) + i//5
        
        offset=(40+2*i)-1
        fx.seek(offset*N*8, 0)  
        fy.seek(offset*N*8, 0)  

        # Get velocity fields
        ux = np.fromfile(fx, float, N, "")
        ux = np.reshape(ux, (129,513), 'F')
        uy = np.fromfile(fy, float, N, "")
        uy = np.reshape(uy, (129,513), 'F')
    
        ymin=32;ymax=96
        xmin=236;xmax=310
        # Compute vorticity using finite-differences
        dxy = (uy[ymin:ymax, xmin+1:xmax+1] - uy[ymin:ymax, xmin-1:xmax-1])*0.5
        dyx = (ux[ymin+1:ymax+1, xmin:xmax] - ux[ymin-1:ymax-1, xmin:xmax])*0.5
        vort = dxy - dyx
        # The sign of the vorticity is wrong if using a right-handed coord. system.
        # The velocity field should probably be flipped upside-down
        vort = - vort

        # Print fluctuation amplitude as title
        timeFromPeak=(offset+1-50)*0.04
        if timeFromPeak<0:
                tit=r'$t=t^{\star}-'+'{:2.2f}\\tau_c$'.format(-timeFromPeak)
        elif timeFromPeak>0:
                tit=r'$t=t^{\star}+'+'{:2.2f}\\tau_c$'.format(timeFromPeak)
        else:
                tit=r'$t=t^{\star}$'
        ax_list[I].set_title(tit,fontsize=20,bbox=bbox)
        # Print vorticity field
        im=ax_list[I].imshow(vort, interpolation='spline36', cmap='BrBG', vmin=-0.15, vmax=0.15)
        # Adds a filled Rectangle to mark the square obstacle
        rect = ax_list[I].add_artist(Rectangle((21,25), 14, 14))
        rect.set_color('#545454')

        # Write ticks and labels
        xticks = ax_list[I].get_xticks()
        xticks[:] = [(x+xmin) / 17 for x in xticks]
        xticklabels = ['{:2.1f}'.format(x) for x in xticks]
        ax_list[I].set_xticklabels(xticklabels, fontsize=16)
        yticks = ax_list[I].get_yticks()
        yticks[:] = [(x+ymin) / 17 for x in yticks]
        yticklabels = ['{:2.1f}'.format(x) for x in yticks]
        ax_list[I].set_yticklabels(yticklabels[::-1], fontsize=16)
        
        ax_list[i].set_xlabel(r'$x/R$',fontsize=22)
        ax_list[i].set_ylabel(r'$y/R$',fontsize=22)
        
#cbar=fig.colorbar(im, ax=ax_list)
#cbar.ax.tick_params(labelsize=16)



fname = 'dynamics_extremes.png'
plt.savefig(fname)

plt.show()
            
