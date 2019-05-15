import numpy as np
import matplotlib.style
import matplotlib.pyplot as plt

def bundle_nearest_points(I, dist):
    bundle = []
    list_of_bundles = []
    bundle.append(I[0])
    for tup in zip(I,I[1:]):     
        if (tup[1]-tup[0]) < dist:
            bundle.append(tup[1])
        else:
            list_of_bundles.append(bundle.copy())
            bundle.clear()
            bundle.append(tup[1])
            
    list_of_bundles.append(bundle.copy())
    return list_of_bundles


plt.style.use('ggplot')

path_to_file = "/home/tlestang/transition_hdd/thibault/These/lbm_code/seq/draft/control_run/control_1" \
               + "/data_force.datout"
tau_0 = 500 # Turnover time in units of LBM timesteps
             # The correlation time tau_c is 2000 timesteps, and the
             # tau_c is 4tau_0
T = 1000
f = np.fromfile(path_to_file, float, T*tau_0, "");
tspan = np.linspace(0,T,len(f))

a = 0.15
I = np.argwhere(f>a)

list_of_bundles = bundle_nearest_points(I, 2000)

point_array = np.zeros(len(list_of_bundles))
value_array = np.zeros(len(list_of_bundles))                    
for i, bundle in enumerate(list_of_bundles):
    # argmax return the index relative to f[bundle]
    # must add offset bundle[0]
    point_array[i] = tspan[np.argmax(f[bundle])+bundle[0]]
    value_array[i] = np.amax(f[bundle])

fig,ax = plt.subplots(1,1,figsize=(12,4), constrained_layout=True)
ax.set_xlim(0, T)
line, = ax.plot(tspan, f)
line2, = ax.plot(point_array, value_array, 'o', linestyle='None', markersize=4)
line3, = ax.plot([tspan[0], tspan[-1]], [a, a], linestyle='--', linewidth=.7)
line3.set_color(line2.get_color())
line.set_linewidth(.8)

y0 = 0.20
eps = 10
props=dict(arrowstyle="->", color=line2.get_color(),
                length_includes_head=True, width=0.002,
                head_width=0.01, head_length=5)

for x_point, x_point_fwd in zip(point_array, point_array[1:]):
    plt.annotate('', xy=(x_point+eps, y0), xytext=(x_point_fwd-eps, y0),
                 arrowprops=props)

ax.set_xlabel(r'$t / \tau_0$',fontsize=22)
plt.ylabel('$f_d(t)$',fontsize=22)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)


# fname= 'typical_drag_signal.png'
# plt.savefig(fname)

plt.show()
