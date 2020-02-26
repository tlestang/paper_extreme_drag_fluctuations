from os.path import join
import argparse
import numpy as np

from jfm_paper import utils


parser = argparse.ArgumentParser(
    description="Concatenate all trajecories in a GKTL dir"
)
parser.add_argument(
    "dirname", type=str, help="path to gktl dir relative to current dir"
)
args = parser.parse_args()

sizeof_float = np.dtype(float).itemsize

N = utils.get_gktl_parameters(args.dirname)["nc"]
ntrans = utils.get_gktl_parameters(args.dirname)["transient"]
output_handle = open("all_the_timeseries.bin", "wb")
for j in range(N):
    filename = join(args.dirname, "rep_0_clone_{}.traj".format(j))
    x = np.fromfile(filename, float, -1, "", offset=ntrans * sizeof_float)
    x.tofile(output_handle)
output_handle.close()

# Test
# For each traj, compare first 100 elements
output_handle = open("all_the_timeseries.bin", "rb")
nt = utils.get_gktl_parameters(args.dirname)["Ta"]
for j in range(N):
    filename = join(args.dirname, "rep_0_clone_{}.traj".format(j))
    xref = np.fromfile(filename, float, 100, "", offset=ntrans * sizeof_float)
    output_handle.seek(j * nt * sizeof_float)
    x = np.fromfile(output_handle, float, 100, "")

    np.testing.assert_array_equal(x, xref)
