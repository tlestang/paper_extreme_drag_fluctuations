import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys
from  scipy import integrate
from os.path import splitext
from os.path import abspath, dirname, join, basename

R = 16 # Size of the obstable in lattice unit
U = 0.036 # Mean flow velocity in lattice unit 
dt = U/R

prefix = join(
    abspath(dirname(__file__)), "data"
    )

# -------* Autocorrelation function for drag process *---------
path_autocorr_drag = join(prefix, 'autocorr_drag.csv')
try:
    series = pd.read_csv(path_autocorr_drag, comment='#', index_col=0)
except FileNotFoundError:
    sys.exit('Error: Could not find find file {}'.format(path_autocorr_drag))

# Compute integral of autocorrelation to estimate
# autocorrelation time
# Note that the autocorrelation is already normalized
# by variance.
I = integrate.trapz(series.values, axis=0)
# Make the autocorrelation time the unit of time
dt = 1/I

C = series.values
plt.plot(np.arange(0,C.size)*dt, C,lw=2)

plt.xlabel('$\\tau / T_0$', fontsize=18)
plt.ylabel('$C(\\tau)$', fontsize=18)

fname = join(
    abspath(dirname(__file__)), basename(splitext(__file__)[0])+'.eps'
    )
plt.savefig(fname)
