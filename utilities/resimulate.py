# This script resimulate the dynamics corresponding to a drag fluctuation
# in a long drag timeseries, potentially split in several files.
# Usage: python resimulate_fluct fluctuations.csv [--full]
# where fluctuations.csv is a CSV file of the type
#
# directory0,init_file0,nb_timesteps0
# directory1,init_file1,nb_timesteps1
#

import os
import csv
import argparse

import simulate

description = "Resimulate one or several fluctuations in the control run."
parser = argparse.ArgumentParser(description=description)
parser.add_argument(
    "directory",
    type=str,
    help="Location of the control run directories relative to current directory.",
)
parser.add_argument(
    "--full",
    action="store_true",
    help="Whether or not to resimulate dynamics from most recent saved state.",
)
parser.add_argument(
    "fluct_idx", metavar="N", type=int, nargs="+", help="a fluctuation index"
)

args = parser.parse_args()

with open("peaks.csv", mode="r") as extremes_file:
    extremes_reader = csv.reader(extremes_file, delimiter=",")
    line_count = 0
    flucts = [_tuple for i, _tuple in enumerate(extremes_reader) if i in args.fluct_idx]

for counter, fluct in enumerate(flucts):
    dirname, init_file, nb_timesteps, peak, value = fluct
    tvismin = int(nb_timesteps) - 2000
    tmax = int(nb_timesteps) + 2000
    if tvismin < 0:
        tvismin = 0
    path = os.path.join(args.directory, dirname, "populations", init_file)
    simulate.simulate(path, 0, tmax, tvismin, tmax)

    event_dir = os.path.join(args.directory, "event_{}".format(counter))
    if not os.path.isdir(event_dir):
        os.mkdir(event_dir)
    for filename in [
        "ux.dat",
        "uy.dat",
        "rho.dat",
        "dragFile.dat",
        "viscousBot.dat",
        "viscousFront.dat",
        "viscousRear.dat",
        "viscousTop.dat",
        "pFront.dat",
        "pRear.dat",
    ]:
        os.rename(filename, os.path.join(event_dir, filename))
        print("Moved {} to {}".format(filename, os.path.join(event_dir, filename)))
