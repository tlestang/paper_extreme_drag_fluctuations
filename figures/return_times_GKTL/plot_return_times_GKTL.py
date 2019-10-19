import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import interpolate
import returntimes_GKTL as rtt

def get_interpolated_return_times(directories, Ta, T, k, N, nb_points=10):
    nb_directories = len(directories)

    rmax = np.empty(nb_directories)
    rmin = np.empty(nb_directories)
    interpolants = []
    for i, dirname in enumerate(directories):
        a, ra = rtt.compute_return_times_no_dups(dirname, Ta,
                                                 T, k, N)
        rmax[i] = np.amax(ra); rmin[i] = np.amin(ra)
        interpolants.append(interpolate.interp1d(ra, a, kind='slinear', bounds_error=False))
    ra_interp = np.logspace(np.log(np.amin(rmin))/np.log(10),
                            np.log(np.amax(rmax))/np.log(10), nb_points)
    
    interpolated_a = np.empty((nb_points, nb_directories))
    for i, dirname in enumerate(directories):
        interpolated_a[:,i] = interpolants[i](ra_interp)

    return ra_interp, pd.DataFrame(data=interpolated_a)

N = 1024
Ta = 30
nbfiles = 10
tau_c = 2000
T = 10

mu_and_sigma_file = './data/musigma_AVG_10.dat'
musigma = np.fromfile(mu_and_sigma_file, float, -1, "")

fig, ax = plt.subplots(figsize=(8,5),constrained_layout=True)
ax.set_xscale('log')

for k in [0.005, 0.01]:
    GKTL_dir_template = './data/gktl_test_{}_k_{}_T_{}'.format(N,k,Ta)
    directories = ['{}_{}'.format(GKTL_dir_template, i) for i in range(0,nbfiles)]
    ra_interp, df = get_interpolated_return_times(directories, Ta, T,
                                                  k, N, nb_points=30)

    df=df.div(musigma[1])
    error = 1.96*df.std(axis=1).values
    mean = df.mean(axis=1).values
    line, = plt.plot(ra_interp, mean, label='$k={}$'.format(k))
    plt.fill_between(ra_interp, mean-error, mean+error, color=line.get_color(), alpha=0.2)
    

direct_sampling_file='./data/rt_Nc1024_Ta30_T10.csv'
# Direct sampling file contains M rows (blocks) and K columns (repetitions).
# Numbers are the block maxima
df = pd.read_csv(direct_sampling_file, comment='#', index_col=0)
df = (df-musigma[0])/musigma[1]

error = 1.96*df.std(axis=1).values[:-1]
mean = df.mean(axis=1).values[:-1]
M = df.shape[0]
# Compute return time for equiprobable blocks
DT = 100 #\Delta T = 10*T
ra = np.array([-DT/np.log(1-m/M) for m in range(1,M)])
line, = plt.plot(ra, mean, label='direct sampling')
plt.fill_between(ra, mean-error, mean+error, color=line.get_color(), alpha=0.2)

ax.set_yticks([1,3,5])
ax.tick_params(axis='both', which='major', labelsize=18)

ax.set_ylabel('$a/\sigma_T$', fontsize=22)
ax.set_xlabel('$r(\\tilde{F}_T \geq a)/\\tau_c$', fontsize=22)
ax.legend(loc='best', fontsize=16)

# Plot a vertical line indicating T_{tot} the lduration
# of the timeseries for direct estimations
ax.plot([np.amax(ra), np.amax(ra)], [0, 6], linestyle='--', linewidth=0.7, color='gray')
plt.text(np.amax(ra), 0.5, '$T_{tot}$', fontsize=20)
ax.set_ylim((0,6))
# Prints figure
fname = 'return_times_GKTL.png'
plt.savefig(fname)

plt.show()
