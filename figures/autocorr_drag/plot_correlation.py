import numpy as np
import matplotlib.style
import matplotlib.pyplot as plt

plt.style.use('ggplot')

prefix = '/home/tlestang/transition_hdd/thibault/These/lbm_code/seq/' \
         + 'draft/scripts/plot_correlation/'

buf = np.fromfile(prefix+'correlationData.dat', float, -1, "");
n=int(len(buf)/2)
tDomain = buf[0:n]
c = buf[n:]

fig,ax = plt.subplots(1,1, figsize=(12,8), constrained_layout=True)
ax.set_xlim(0, 10)
line0, =ax.plot(np.array([0, 10]), np.array([0, 0]))
lineC, = ax.plot(tDomain/500,c,color=line0.get_color())
line0.set_linestyle('--')
line0.set_linewidth(1.5)

ax.set_xlabel(r'$\tau / \tau_0$',fontsize=26)
plt.ylabel(r'$C(\tau)$',fontsize=26)
plt.xticks(fontsize=22)
plt.yticks(fontsize=22)

fname = 'autocorr_drag.png'
plt.savefig(fname)

plt.show()
