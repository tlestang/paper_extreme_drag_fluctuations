import numpy as np
from os.path import join
from scipy.signal import find_peaks

with open("../data/list_of_dirs.txt", "r", newline="\n") as f:
    dirs = [line.rstrip("\n") for line in f]

sig = 0.0412
mu = 0.0252

restart_pts_period = 20000000
tau_c = 2000

csv_file_handle = open("peaks.csv", "w")
for min_height in np.arange(1, 10.5, 0.5):
    max_height = min_height + 0.5
    peaks = []
    file_of_peaks = []
    peaks_values = []
    for idir, dirname in enumerate(dirs):
        f = np.fromfile(
            join("../data", dirname, "data_force.datout"),
            float,
            -1,
            "",
            offset=25000 * 8,
        )
        f = (f - mu) / sig
        local_peaks, properties = find_peaks(
            f, height=(min_height, max_height), distance=2 * tau_c
        )
        peaks_values.extend(f[local_peaks])
        local_peaks = local_peaks + 25000
        peaks.extend(local_peaks)
        file_of_peaks.extend([idir] * len(local_peaks))

    print("[{}-{}]] I found {} peaks".format(min_height, max_height, len(peaks)))
    if len(peaks) > 0:
        dist_to_restart_pt = [
            peak - (peak // restart_pts_period) * restart_pts_period for peak in peaks
        ]
        peak_idx = np.argmin(dist_to_restart_pt)
        peak_file = file_of_peaks[peak_idx]
        restart_file = "pops_{}.datout".format(peaks[peak_idx] // restart_pts_period)
        csv_file_handle.write(
            "{},{},{:d},{:d},{:f}\n".format(
                dirs[peak_file],
                restart_file,
                dist_to_restart_pt[peak_idx],
                peaks[peak_idx],
                peaks_values[peak_idx],
            )
        )
csv_file_handle.close()
