import numpy as np
import matplotlib.style
import matplotlib.pyplot as plt

plt.style.use('ggplot')

path_to_file = "/home/thibault/transition_hdd/thibault/These/lbm_code/seq/draft/scripts/" \
               + "courbe_temps_de_retour_drag_instant/return_times_drag_instant.dat"

buf = np.fromfile(path_to_file, float, -1, "");
n=len(buf)/2
r = buf[0:n]
avec = buf[n:]

r = r / 2000;
mu = 0.0252;
sig = 0.0412;
avec = (avec-mu)/sig;

fig,ax = plt.subplots(1,1,figsize=(6,4),constrained_layout=True)
ax.set_xlim(10, 1e5)
ax.set_ylim(2.7, 9)
line, = ax.plot(r, avec)
ax.set_xscale('log')
#line.set_linewidth(.7)

ax.set_xlabel(r'$r(f_d \geq a) / \tau_c$',fontsize=16)
ax.set_ylabel('$a$',fontsize=16)
ax.set_yticks([3,5,7,9])
ax.set_yticklabels((r'$3\sigma$',r'$5\sigma$',r'$7\sigma$',r'$9\sigma$'))

fname = 'return_time.png'
plt.savefig(fname)

plt.show()
