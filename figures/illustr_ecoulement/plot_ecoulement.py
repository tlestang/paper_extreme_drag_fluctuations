# Produces a figure illustrating the vorticity field in the whole comp. domain
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

Dx = 513
Dy = 129
N = Dx*Dy
F = np.zeros(104)
idx = np.zeros(104)

# Make use of flow data generated for figure ecoulement typique
prefix = '/home/tlestang/transition_hdd/thibault/These/' \
         + 'articles/data/ecoulement_typique/'

fig, ax = plt.subplots(figsize=(16,7), constrained_layout=True)
# Declares a 2x5 grid.

path_to_file_ux = prefix+'ux.dat'
path_to_file_uy = prefix+'uy.dat'
fx = open(path_to_file_ux, "rb")  # reopen the file
fy = open(path_to_file_uy, "rb")  # reopen the file
bbox = dict(boxstyle="round", fc="0.9")

# Get velocity fields
ux = np.fromfile(fx, float, N, "")
ux = np.reshape(ux, (129,513), 'F')
uy = np.fromfile(fy, float, N, "")
uy = np.reshape(uy, (129,513), 'F')
    
ymin=1;ymax=128
xmin=1;xmax=512
# Compute vorticity using finite-differences
dxy = (uy[ymin:ymax, xmin+1:xmax+1] - uy[ymin:ymax, xmin-1:xmax-1])*0.5
dyx = (ux[ymin+1:ymax+1, xmin:xmax] - ux[ymin-1:ymax-1, xmin:xmax])*0.5
vort = dxy - dyx

im=ax.imshow(vort, interpolation='spline36', cmap='BrBG', vmin=-0.07, vmax=0.07)

# Adds a filled Rectangle to mark the square obstacle
rect = ax.add_artist(Rectangle((256,55), 14, 14))
rect.set_color('#545454')
# Show the grid
R = 8
ny,nx  = ux.shape
n_lamina = ((ny-1)/R)/2
x0 = (nx-1)/16
for i in range(0,int(n_lamina)):
    y_start = 2*i*R + R/2
    y_end = y_start + R
    grid = ax.add_artist(Rectangle((x0-1,y_start-1), 1, R-1))
    grid.set_color('#545454')

# Write ticks and labels
xticks = ax.get_xticks()
xticks[:] = [x / 17 for x in xticks]
xticklabels = ['{:2.1f}'.format(x) for x in xticks]
ax.set_xticklabels(xticklabels, fontsize=16)
yticks = ax.get_yticks()
yticks[:] = [x / 17 for x in yticks]
yticklabels = ['{:2.1f}'.format(x) for x in yticks]
ax.set_yticklabels(yticklabels[::-1], fontsize=16)

ax.tick_params(axis='both', which='major', labelsize=22)
ax.set_xlabel(r'$x/R$',fontsize=24)
ax.set_ylabel(r'$y/R$',fontsize=24)
        
#cbar=fig.colorbar(im, ax=ax,location='top')
#cbar.ax.tick_params(labelsize=16)

fname = 'illustr_ecoulement.png'
plt.savefig(fname)

plt.show()
            
