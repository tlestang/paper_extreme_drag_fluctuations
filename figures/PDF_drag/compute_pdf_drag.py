import sys
import datetime
from os.path import splitext

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

files = [
    "/home/tlestang/grid/control_long_{:d}/" "data_force.datout".format(i + 1)
    for i in range(0, 10)
]

print("Computing moments...")
mu = 0.0253
var = 0.00173

for i in range(10):
    print("Loading file {}/10".format(i + 1))
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

output_csv = "../../data/PDF_drag.csv"
with open(output_csv, "w") as f:
    f.write("# Generated with {}\n".format(sys.argv[0]))
    f.write("# {}\n".format(str(datetime.datetime.now())))
    f.write("# mu = 0 var = 1")
    f.write("# /home/tlestang/grid/control_long_{}/data_force.datout")
    f.write("# using {} files\n".format(10))
    f.write("#\n")
    series.to_csv(f, header=True)
