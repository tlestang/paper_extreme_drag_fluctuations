import numpy as np
import matplotlib.pyplot as plt


prefix = '/home/thibault/transition_hdd/thibault/These/lbm_code/seq/draft/etude_dynamique/' \
         + 'averaged_drag/'

F = np.loadtxt('list.txt', dtype=int)
sig=0.0412
m=0.0252

Nevents = len(F)

musigma = np.fromfile("../PDF_AVG/musigma_AVG_10.dat", float, -1, "");

fig, axes = plt.subplots(nrows=2,ncols=3, figsize=(18,6))

for i in range(0,6):
    fileName=prefix+'event_{:d}_AVG/'.format(F[i]+1)+'data_force.datout'
    f = np.fromfile(fileName, float, -1, "")
    f = f-m
    amp = np.sum(f)/(len(f)-1)/musigma[1]
    f = f/sig
    N = len(f)
    row = i // 3
    col = i % 3
    axes[row,col].plot(np.linspace(0,10,N),f)
    axes[row, col].set_xlim((0, 10))
    axes[row, col].set_ylim((-1,6))

    axes[row, col].set_title(r"$F = {:2.1f}$".format(amp))
    axes[row, col].set_ylim((-0.83,10.63))


plt.show()
