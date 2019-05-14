import numpy as np
import matplotlib.style
import matplotlib.pyplot as plt

plt.style.use('ggplot')

path_to_file = "/home/tlestang/transition_hdd/thibault/These/lbm_code/seq/draft/control_run/control_1" \
               + "/data_force.datout"
tau_0 = 500 # Turnover time in units of LBM timesteps
             # The correlation time tau_c is 2000 timesteps, and the
             # tau_c is 4tau_0
T = 1000
f = np.fromfile(path_to_file, float, T*tau_0, "");
tspan = np.linspace(0,T,len(f))

fig,ax = plt.subplots(1,1,figsize=(12,3), constrained_layout=True)
ax.set_xlim(0, T)
line, = ax.plot(tspan, f)
line.set_linewidth(.7)

ax.set_xlabel(r'$t / \tau_0$',fontsize=22)
plt.ylabel('$f_d(t)$',fontsize=22)
#ax.set_yticks(np.arange(-0.10,0.30,0.10))
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)


fname= 'typical_drag_signal.png'
plt.savefig(fname)

plt.show()
