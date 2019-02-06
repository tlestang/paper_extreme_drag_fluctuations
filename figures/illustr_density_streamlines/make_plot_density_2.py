# Produces a figure illustrating the vorticity field at the moment of peak drag for 7 events.
# The figure consists of 7 axes. One axes is four times bigger as the others, and contains 
# annotations
import numpy as np
import csv
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

Dx = 513
Dy = 129
x = np.asarray(range(0,74))
y = np.asarray(range(0,64))
N = Dx*Dy
F = np.zeros(104)
idx = np.zeros(104)
prefix = '/home/thibault/transition_hdd/thibault/These/lbm_code/seq/draft/etude_dynamique/instant_events/'
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

fig, ax_list = plt.subplots(figsize=(9,7),constrained_layout=True)

fig = plt.gcf()
#ax_list = fig.axes
#Nevents = len(ax_list)

path_to_file_ux = prefix+'event_{:d}_feb/ux.dat'.format(int(idx[0]+1))
path_to_file_uy = prefix+'event_{:d}_feb/uy.dat'.format(int(idx[0]+1))
path_to_file_rho = prefix+'event_{:d}_feb/rho.dat'.format(int(idx[0]+1))

# Opens the files and jump to peak drag
# (middle of timeseries)
fx = open(path_to_file_ux, "rb")  # reopen the file
fy = open(path_to_file_uy, "rb")  # reopen the file
frho = open(path_to_file_rho, "rb")  # reopen the file
fx.seek(49*N*8, 0)  # seek
fy.seek(49*N*8, 0)  # seek
frho.seek(49*N*8, 0)  # seek
    
# Get vorticity fields
# Needed to compute streamlines
ux = np.fromfile(fx, float, N, "")
ux = np.reshape(ux, (129,513), 'F')
uy = np.fromfile(fy, float, N, "")
uy = np.reshape(uy, (129,513), 'F')
# Zoom on the square obstacle
ymin=32;ymax=96
xmin=236;xmax=310
uxCropped = ux[ymin:ymax,xmin:xmax]
uyCropped = uy[ymin:ymax,xmin:xmax]

# Get density field
rho = np.fromfile(frho, float, N, "")
rho = np.reshape(rho, (129,513), 'F')
# Zoom on the square obstacle
rhoCropped = rho[ymin:ymax,xmin:xmax]

# ---- Actual Plotting part ----------
# Print density field
im = ax_list.imshow(rhoCropped, interpolation='spline36', cmap='RdBu', vmin=0.85, vmax=1.15)
    
# Print fluctuation amplitude as title
tit='$f_d = {:2.1f}\\sigma$'.format(F[0])
ax_list.set_title(tit,fontsize=22)

# Adds a filled Rectangle to mark the square obstacle
rect = ax_list.add_artist(Rectangle((21,25), 14, 14))
rect.set_color('#545454')

cbar = fig.colorbar(im, ax=ax_list)
cbar.ax.tick_params(labelsize=16)
# Print streamlines for last axes
ax_list.streamplot(x,y,uxCropped,uyCropped, linewidth=1, density=3)

# Annotate the plot to point to interesting flow regions
# -----
# Write the annotation in a box
# Taken from:
# https://matplotlib.org/gallery/pyplots/annotate_transform.html#sphx-glr-gallery-pyplots-annotate-transform-py
bbox = dict(boxstyle="round", fc="0.9")
# Annotate trapped vorticity
ax_list.annotate('Trapped vorticity', xy=(40, 35), xytext=(50, 15),
                     arrowprops=dict(facecolor='black', shrink=0.05),bbox=bbox,fontsize=16)
# Annotate blocking vortex
ax_list.annotate('Blocking vortex', xy=(60, 35), xytext=(35, 50),
                     arrowprops=dict(facecolor='black', shrink=0.05),bbox=bbox,fontsize=16)
# Annotate blocking vortex
ax_list.annotate('Production of vorticity', xy=(28, 25), xytext=(5, 12),
                     arrowprops=dict(facecolor='black', shrink=0.05),bbox=bbox,fontsize=16)

# Write ticks and labels
xticks = ax_list.get_xticks()
xticks[:] = [(x+xmin) / 17 for x in xticks]
xticklabels = ['{:2.1f}'.format(x) for x in xticks]
ax_list.set_xticklabels(xticklabels, fontsize=16)
yticks = ax_list.get_yticks()
yticks[:] = [(x+ymin) / 17 for x in yticks]
yticklabels = ['{:2.1f}'.format(x) for x in yticks]
ax_list.set_yticklabels(yticklabels[::-1], fontsize=16)

ax_list.set_xlabel(r'$x/R$',fontsize=22)
ax_list.set_ylabel(r'$y/R$',fontsize=22)


fname = 'illustr_density_streamlines.png'
plt.savefig(fname)

plt.show()
            
