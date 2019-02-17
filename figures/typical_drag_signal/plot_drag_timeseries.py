import numpy as np
import matplotlib.style
import matplotlib.pyplot as plt

plt.style.use('ggplot')

path_to_file = "/home/thibault/transition_hdd/thibault/These/lbm_code/seq/draft/control_run/control_1" \
               + "/data_force.datout"
tau_c = 1000;
f = np.fromfile(path_to_file, float, 250*tau_c, "");
tspan = np.linspace(0,1000,len(f))

fig,ax = plt.subplots(1,1,figsize=(8,3), constrained_layout=True)
ax.set_xlim(0, 1000)
line, = ax.plot(tspan, f)
line.set_linewidth(.7)

ax.set_xlabel(r'$t / \tau_c$',fontsize=22)
plt.ylabel('$f_d(t)$',fontsize=22)
ax.set_yticks(np.arange(-0.10,0.30,0.10))
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)


fname= 'typical_drag_signal.png'
plt.savefig(fname)

plt.show()
