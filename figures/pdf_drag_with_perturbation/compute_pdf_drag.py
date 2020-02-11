import sys
import datetime
from os.path import realpath, join
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

list_timeseries = ["../../data/cr_perturb/all_the_timeseries.bin",
              "../../data/control_1_2017_10_31_14_07_55/data_force.datout"]
output_files = ["PDF_drag_perturb.csv", "PDF_drag_one_file.csv"]

var = 0.00173
mu = iter([0.0, 0.0252])
for timeseries, output_file in zip(list_timeseries, output_files):
    # Note that the mean is already substracted
    xtot = np.fromfile(timeseries, float, -1, "") - next(mu)

    print("Computing histogram...")
    xtot = xtot / np.sqrt(var)
    hist, bins = np.histogram(xtot, bins=100, density=True)
    bin_centers = [0.5 * (b[1] + b[0]) for b in zip(bins[:-1], bins[1:])]

    series = pd.Series(data=hist, index=bin_centers)

    output_csv = join("../../data/", output_file)
    with open(output_csv, "w") as f:
        f.write("# Generated with {}\n".format(sys.argv[0]))
        f.write("# {}\n".format(str(datetime.datetime.now())))
        f.write("# mu = 0 var = 1")
        f.write("# {}".format(realpath(timeseries)))
        f.write("#\n")
        series.to_csv(f, header=True)
