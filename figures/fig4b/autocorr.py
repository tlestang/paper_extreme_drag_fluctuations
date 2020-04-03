import sys
import datetime
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from jfm_paper.utils import get_autocorr

data = "/home/tlestang/grid/control_long_1/data_force.datout"

nreps = 15000
tau_0 = 450  # Turn over in units of timesteps
T = 11 * tau_0


var = 0.00173
mu = 0.0253

# In the following the lag window is prescribed in units of timesteps (dt=1)
series = get_autocorr(data, nreps, T, mu=mu, var=var, dtype=float, verbose=True)

with open("autocorr_drag.csv", "w") as f:
    f.write("# Generated with {}\n".format(sys.argv[0]))
    f.write("# {}\n".format(str(datetime.datetime.now())))
    f.write("# nreps = {}\n".format(nreps))
    f.write("# using {} \n".format(filename))
    f.write("#\n")
    series.to_csv(f, header=True)
