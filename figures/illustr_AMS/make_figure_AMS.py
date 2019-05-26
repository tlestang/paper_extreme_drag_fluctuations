import os

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

prefix = '/home/tlestang/transition_hdd/thibault/These/AMS/AMS_OU_AVG/run_for_figure_AMS/'
with open(os.path.join(prefix, 'input.in'), 'r') as f:
    lines = [line.rstrip() for line in f]
Nc = int(lines[0])
Ta = int(lines[1])
T = int(lines[2])
dt = float(lines[3])

ndtAVG = int(np.floor(T/dt))

idx = int(np.fromfile(os.path.join(prefix, 'killed_copie.datout'), np.int32, -1, ''))

Nt = int(np.floor(Ta/dt))
tspan = np.linspace(0,Ta-T,Nt-ndtAVG+1)
lblidx = [1, 2, 3]

filename = os.path.join(prefix, 'clone_{}_iter_1.traj'.format(idx))
x = np.fromfile(filename, float, -1, '')

series = pd.Series(x).rolling(ndtAVG).mean()
xAVG = series.values[ndtAVG-1:]

fig,ax = plt.subplots(1,1, figsize=(18,9), constrained_layout=True)
ax.plot(tspan, xAVG, linewidth=2.5)

amax = [0,0,0]
linestyle = ['-']*3
linestyle[idx]='--'
for j in range(0,3):
    filename = os.path.join(prefix, 'clone_{}_init.traj'.format(j))
    x = np.fromfile(filename, float, -1, '')
    series = pd.Series(x).rolling(ndtAVG).mean()
    xAVG = series.values[ndtAVG-1:]

    amax[j] = np.amax(xAVG)
    ii = np.argmax(xAVG)
    ax.plot(tspan, xAVG, linestyle=linestyle[j], color='k', linewidth=2.5)

    ax.plot(ii*dt, amax[j], linestyle=None, marker='s', markersize=7, color='k')
    plt.plot(tspan, amax[j]*np.ones(len(xAVG)), color='k', linestyle='--')

brch_pt, = ax.plot(1.75,amax[idx], 'o', linestyle=None, markersize=10, color='r')

plt.plot(tspan, 2*np.ones(len(xAVG)), linestyle='--', color='k', linewidth=2.5)

plt.text(1.2,-1.4,'$2$', fontsize=22)
plt.text(1.2,-0.6,'$1$', fontsize=22)
plt.text(1.2,0.35,'$3$', fontsize=22)

amax.sort()
plt.text(0.5,amax[0]+0.07,'$Q_1$', fontsize=28)
plt.text(0.5,amax[1]-0.17,'$Q_2$', fontsize=28)
plt.text(0.5,amax[2]+0.07,'$Q_3$', fontsize=28)

plt.title('$1$ branched on $3$', fontsize=28)
plt.text(4,-1.2,'$N = 3$ trajectories', fontsize=28)
plt.text(4,-1.4,'$Q_{1} < Q_{2} < Q_{3}$', fontsize=28)


ax.set_yticks([-1,0]+[1,2])
ax.set_yticklabels(['$-1$', '$0$', '$1$', '$Q$'],
                   fontsize=28)
ax.set_ylabel(r'$\xi$', fontsize=30)
ax.set_xticks([0,2.25,4.5,6.75,9])
ax.set_xticklabels(['$0$', '$T_a / 4$', '$T_a / 2$', '$3T_a / 4$', '$T_a$'])
plt.xticks(fontsize=28)
ax.set_xlim((0,9))
ax.set_xlabel(r'$t$', fontsize=30)

fname = 'illustr_AMS.pdf'
plt.savefig(fname)
plt.show()
