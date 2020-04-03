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

prefix = "./data/"
print(prefix)

fig = plt.figure(figsize=(16,7), constrained_layout=True)
# Declares a 2x5 grid.

grid = plt.GridSpec(2, 5, figure=fig)
# the first row is divided into five snapshots
for i in range(0,5):
    plt.subplot(grid[0,i])
#the second row is for the drag signal
plt.subplot(grid[1,:])

ax_list = fig.axes
nplots = len(ax_list)

path_to_file_ux = prefix+'ux.dat'
path_to_file_uy = prefix+'uy.dat'
fx = open(path_to_file_ux, "rb")  # reopen the file
fy = open(path_to_file_uy, "rb")  # reopen the file
bbox = dict(boxstyle="round", fc="0.9")

for i in range(0,nplots-1):
        # trick to advance in time with row major ordering
        
        fx.seek(i*N*8, 0)  
        fy.seek(i*N*8, 0)  

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

        # Print time as title
        timeFromBeg=0.1+i*0.2
        tit='$t={:2.1f}\\tau_c$'.format(timeFromBeg)

        ax_list[i].set_title(tit,fontsize=20,bbox=bbox)
        # Print vorticity field
        im=ax_list[i].imshow(vort, interpolation='spline36', cmap='BrBG', vmin=-0.09, vmax=0.09)
        # Adds a filled Rectangle to mark the square obstacle
        rect = ax_list[i].add_artist(Rectangle((21,25), 14, 14))
        rect.set_color('#545454')

        # Write ticks and labels
        xticks = ax_list[i].get_xticks()
        xticks[:] = [(x+xmin) / 17 for x in xticks]
        xticklabels = ['{:2.1f}'.format(x) for x in xticks]
        ax_list[i].set_xticklabels(xticklabels, fontsize=16)
        yticks = ax_list[i].get_yticks()
        yticks[:] = [(x+ymin) / 17 for x in yticks]
        yticklabels = ['{:2.1f}'.format(x) for x in yticks]
        ax_list[i].set_yticklabels(yticklabels[::-1], fontsize=16)
        
        ax_list[i].set_xlabel(r'$x/R$',fontsize=22)
        ax_list[i].set_ylabel(r'$y/R$',fontsize=22)
        
cbar=fig.colorbar(im, ax=ax_list,location='top')
cbar.ax.tick_params(labelsize=16)

# Now plot the drag signal
sig=0.0412
m=0.0252
Nt = 2000;
fd = (np.fromfile(prefix+'data_force.datout',float,Nt,"")-m)/sig
tspan = np.linspace(0,4,Nt)
ax_list[-1].plot(tspan,fd)
# And plots nplots-1 dots for the nplots-1 snapshots
for t in range(0,2000,400):
        ax_list[-1].plot(tspan[t+200],fd[t+200],marker='o',markersize=10,linestyle='None',color='k')
ax_list[-1].set_xlim((0,4))
# ax_list[-1].set_xticklabels(['$0$','$0.2\\tau_c$','$0.4\\tau_c$','$0.6\\tau_c$','$0.8\\tau_c$','$1.0\\tau_c$'], fontsize=22)
ax_list[-1].set_ylim((-1,2))
ax_list[-1].set_yticks(range(-1,3,1))
ax_list[-1].set_yticklabels(['$-\\sigma$','$0$','$\\sigma$','$2\\sigma$'], fontsize=22)
ax_list[-1].set_ylabel('$f_d(t)$',fontsize=22)
ax_list[-1].set_xlabel('$t/T_0$',fontsize=22)


fname = 'ecoulement_typique.eps'
plt.savefig(fname)

plt.show()
            
