import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def ret_gaussian(x):
    """ Returns zero-mean, unit variance at point
    """
    return (1./(np.sqrt(2.*np.pi)))*np.exp(-0.5*x*x)

prefix = '/home/tlestang/transition_hdd/thibault/These/tailleur_lecomte/lbm/2_sq/' \
         + 'grid/illustration_IS/'

directories = ['k_0.02_2018_03_26_10_01_46/', 'k_0.025_2018_03_25_20_13_40/',
           'k_0.03_2018_03_25_20_13_40/'];
k_value = [0.02, 0.015, 0.03]

sig = 0.0087714;

fig, ax = plt.subplots(figsize=(8,5),constrained_layout=True)

i=0
for directory in directories:
    A = np.fromfile(prefix+directory+'A.datout', float, -1, "")
    A = A/sig # A is already zero-mean

    # https://seaborn.pydata.org/generated/seaborn.kdeplot.html
    sns.kdeplot(A, shade=True, ax=ax, label='$k={:1.2f}$'.format(k_value[i]))
    i=i+1
    
xvec = np.linspace(-2,5,100)
# Plot the origina PDF estimate (gaussian approx)
ax.plot(xvec,ret_gaussian(xvec),linestyle='--', label='$k=0$')
ax.set_xlim((-2,7))
ax.set_ylim((0,0.7))

ax.set_xticks([-2,0,2,4,6])
ax.set_yticks(ax.get_yticks()[::2]) # Plot only half of ticks
ax.set_xticklabels(['$-2\\sigma_T$','$0$','$2\\sigma_T$','$4\\sigma_T$','$6\\sigma_T$'])
ax.tick_params(axis='both', which='major', labelsize=16)

ax.set_xlabel('$F$', fontsize=22)
ax.set_ylabel('$\\rho_{k}(F_T = F)$', fontsize=22)
ax.legend(loc='best', fontsize=16)

# Prints figure
fname = 'IS_GKTL.png'
plt.savefig(fname)

plt.show()
