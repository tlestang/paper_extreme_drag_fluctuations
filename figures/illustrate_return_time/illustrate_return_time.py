import numpy as np
import matplotlib.style
import matplotlib.pyplot as plt

def bundle_nearest_points(I, dist):
    """
       Given a list of number I (int or floats), return a list of lists, each sublist containing
       subsequent elements distant from less than dist of the next one.

       Parameters
       -----------
       I: list
       dist: int or float

       Returns
       --------
       list of lists
    """
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

path_to_file = "/home/tlestang/articles/jfm_paper/data/control_2_2017_10_31_14_07_55" \
               + "/data_force.datout"
tau_0 = 500 # Turnover time in units of LBM timesteps
             # The correlation time tau_c is 2000 timesteps, and the
             # tau_c is 4tau_0
T = 1000
f = np.fromfile(path_to_file, float, T*tau_0, "");
tspan = np.linspace(0,T,len(f))

a = 0.17 # threshold
I = np.argwhere(f>a) # find all indices where f>a

tau_c = 4*tau_0
list_of_bundles = bundle_nearest_points(I, tau_c)

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

y0 = 0.22 # height of the arrows
dy0 = 0.017 # How higher is the tau letters wrt arrows
dx0 = 10 # Shift tau letters to the left
eps = 1 # Shorten the arrows on both sides
props=dict(arrowstyle="<->", color=line2.get_color(), linewidth=1.5)

# Plot the arrows and text
for i, tup in enumerate(zip(point_array, point_array[1:])):
    x_point, x_point_fwd = tup
    plt.annotate('', xy=(x_point+eps, y0), xytext=(x_point_fwd-eps, y0),
                 arrowprops=props)
    plt.text((x_point+x_point_fwd)/2-dx0, y0+dy0, '$\\tau_{}$'.format(i+1), fontsize=14)

# Plot the letter a at the left hand side of the plot slightly above
# the threshold line
plt.text(15, a+0.005, '$a$', color=line2.get_color(), fontsize=18)    

ax.set_xlabel(r'$t / T_0$',fontsize=22)
plt.ylabel('$f_d(t)$',fontsize=22)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)


fname= 'illustrate_return_time.eps'
plt.savefig(fname)

plt.show()
