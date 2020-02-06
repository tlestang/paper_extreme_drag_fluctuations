import sys
import datetime

import numpy as np
import pandas as pd

from jfm_paper import utils

files = [
    "/home/tlestang/CtrlRunner_v0.2/data_CR_NOSQ_11_02_2018/fdrag.dat"
]

print("Computing moments...")
mu, var = utils.compute_moments(files, dtype=float)

for i, filename in enumerate(files):
    print("Loading file {}/{}".format(i+1, len(files)))
    x = np.fromfile(files[i], float, -1, "")
    if i == 0:
        xtot = x
    else:
        xtot = np.concatenate((xtot, x))

print("Computing histogram...")
xtot = (xtot - mu) / np.sqrt(var)
hist, bins = np.histogram(xtot, bins=100, density=True)
bin_centers = [0.5 * (b[1] + b[0]) for b in zip(bins[:-1], bins[1:])]

series = pd.Series(data=hist, index=bin_centers)

output_csv = "../../data/PDF_drag_nosq.csv"
with open(output_csv, "w") as f:
    f.write("# Generated with {}\n".format(sys.argv[0]))
    f.write("# {}\n".format(str(datetime.datetime.now())))
    f.write("# mu = 0 var = 1")
    f.write("# {}".format(files[0]))
    f.write("# using {} files\n".format(len(files)))
    f.write("#\n")
    series.to_csv(f, header=True)
