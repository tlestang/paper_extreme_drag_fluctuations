import os
import sys
import datetime
import numpy as np
import pandas as pd

tau_c = 2000
Nc = 1024
Ta = 30
T = 10
blockLength = Nc*Ta*tau_c
DT = 10*T*tau_c

nb_files = 10
files = ["/home/tlestang/grid/control_long_{:d}/"
         "data_force.datout_AVG_20000".format(i+1) for i in range(0,nb_files)]

for filename in files:
    if not(os.path.isfile(filename)):
        raise FileNotFoundError('File {} not found.'.format(filename))

n_windows_in_block = int(np.floor(blockLength/DT))
Ntot = int(os.path.getsize(files[0])/8.)
Nblocks = int(np.floor(Ntot / blockLength))

amaxtilde = np.zeros((n_windows_in_block,nb_files*Nblocks))
for i,filename in enumerate(files):
    print(filename)
    if Ntot < blockLength:
        raise valueError("Length of timeseries for file {} is smaller"
                        "than block lenght".format(filename))
    with open(filename, 'rb') as f:
        for block in range(0,Nblocks):
            f.seek(block*blockLength,0)
            list_of_max = [np.max(np.fromfile(f, float, DT, '')) for n in range(0,n_windows_in_block)]
            amaxtilde[:,i*Nblocks + block] = np.sort(list_of_max)[::-1]

df = pd.DataFrame(amaxtilde)

with open('rt_Nc1024_Ta30_T10.csv', 'w') as f:
    f.write('# Generated with {}\n'.format(sys.argv[0]))
    f.write('# {}\n'.format(str(datetime.datetime.now())))
    f.write('# NBlocks = {}\n'.format(Nblocks))
    f.write('# DT = {}\n'.format(DT))
    f.write('# using {} files'.format(nb_files))
    f.write('#\n')
    df.to_csv(f, header=True)

