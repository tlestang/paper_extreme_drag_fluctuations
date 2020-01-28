import csv
import os
import numpy as np
import matplotlib.style
import matplotlib.pyplot as plt

plt.style.use('ggplot')

meanPf = 5.68;
meanPr = 5.65;
meanDrag = 0.0252;
M = (meanPf + meanPr)/2;
sig = 0.0412;
mu = 0.0252;

path_csv = "../../utilities/peaks.csv"
csv_file_handle = open(path_csv, "r")

flucts_reader = csv.reader(csv_file_handle, delimiter=",")
flucts = [_tuple for i, _tuple in enumerate(flucts_reader) if os.path.isfile("../../data/event_{}/dragFile.dat".format(i))]
csv_file_handle.seek(0)
event_dirs = ["../../data/event_{}".format(i) for i, _tuple in enumerate(flucts_reader) if os.path.isfile("../../data/event_{}/dragFile.dat".format(i))]
csv_file_handle.close()

maxDrag = []
frontContrib = []
rearContrib = []
for counter, fluct in enumerate(flucts):
    dirname, init_file, nb_timesteps, peak, value = fluct
    drag = np.fromfile(os.path.join(event_dirs[counter],'dragFile.dat'), float, -1, "")
    pFront = np.fromfile(os.path.join(event_dirs[counter],'pFront.dat'), float, -1, "")
    pRear = np.fromfile(os.path.join(event_dirs[counter],'pRear.dat'), float, -1, "")
    vTop = np.fromfile(os.path.join(event_dirs[counter],'viscousTop.dat'), float, -1, "")
    vBot = np.fromfile(os.path.join(event_dirs[counter],'viscousBot.dat'), float, -1, "")
    vFront = np.fromfile(os.path.join(event_dirs[counter],'viscousFront.dat'), float, -1, "")
    vRear = np.fromfile(os.path.join(event_dirs[counter],'viscousRear.dat'), float, -1, "")

    t_star = min(int(nb_timesteps), 2000)
    maxDrag.append(drag[t_star])
    frontContrib.append((pFront[t_star]-meanPf)/(maxDrag[counter]-meanDrag))
    rearContrib.append((meanPr+pRear[t_star])/(maxDrag[counter]-meanDrag))

maxDrag = np.array(maxDrag)
maxDrag = (maxDrag-mu) / sig
    
fig,ax = plt.subplots(figsize=(9,5), constrained_layout=True)


lineRear, =ax.plot(maxDrag, rearContrib, marker='o', label=r'$-\Delta p^{\star}_{base}/\tilde{f}^{\star}_d$')
lineRear.set_linestyle('None')

lineFront, =ax.plot(maxDrag, frontContrib, marker='^', label=r'$\Delta p^{\star}_{fb}/\tilde{f}^{\star}_d$')
lineFront.set_linestyle('None')

ax.set_xlabel(r'$\tilde{f}^{\star}_d / \sigma$',fontsize=22)
ax.legend(loc='best', fontsize=22)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)

fname = 'pressure_ratio.png'
plt.savefig(fname)

plt.show()
