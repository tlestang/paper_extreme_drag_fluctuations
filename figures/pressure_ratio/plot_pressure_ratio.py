import numpy as np
import matplotlib.style
import matplotlib.pyplot as plt

plt.style.use('ggplot')

NbEvents = 104;
Nt = 8000;

meanPf = 5.68;
meanPr = 5.65;
meanDrag = 0.0252;
M = (meanPf + meanPr)/2;
sig = 0.0412;
mu = 0.0252;
prefix = '/home/thibault/transition_hdd/thibault/These/lbm_code/seq/draft/etude_dynamique/instant_events/';
maxDrag = np.zeros(NbEvents)
frontContrib = np.zeros(NbEvents)
rearContrib = np.zeros(NbEvents)

for i in range(0,NbEvents):
    pathName=prefix+'event_'+str(i+1)+'_feb/'
    drag = np.fromfile(pathName+'data_force.datout', float, -1, "")
    pFront = np.fromfile(pathName+'pFront.dat', float, -1, "")
    pRear = np.fromfile(pathName+'pRear.dat', float, -1, "")
    vTop = np.fromfile(pathName+'viscousTop.dat', float, -1, "")
    vBot = np.fromfile(pathName+'viscousBot.dat', float, -1, "")
    vFront = np.fromfile(pathName+'viscousFront.dat', float, -1, "")
    vRear = np.fromfile(pathName+'viscousRear.dat', float, -1, "")

    maxDrag[i]=np.amax(drag)
    I = np.argmax(drag)
    frontContrib[i] = (pFront[I]-meanPf)/(maxDrag[i]-meanDrag);
    rearContrib[i] = (meanPr+pRear[I])/(maxDrag[i]-meanDrag);

maxDrag = (maxDrag-mu) / sig
    
fig,ax = plt.subplots(figsize=(9,5), constrained_layout=True)


lineRear, =ax.plot(maxDrag, rearContrib, marker='o', label=r'$\tilde{p}^{\star}_{base}$')
lineRear.set_linestyle('None')

lineFront, =ax.plot(maxDrag, frontContrib, marker='^', label=r'$\tilde{p}^{\star}_{fb}$')
lineFront.set_linestyle('None')

coefFront = np.polyfit(maxDrag, frontContrib, 1);
coefRear = np.polyfit(maxDrag, rearContrib, 1);

frontPolyVal = np.polyval(coefFront, maxDrag)
minIdx = np.argmin(maxDrag)
maxIdx = np.argmax(maxDrag)
fitFront, = ax.plot([np.amin(maxDrag), np.amax(maxDrag)], [frontPolyVal[minIdx], frontPolyVal[maxIdx]])
fitFront.set_color(lineFront.get_color())
fitFront.set_linestyle('--')
fitFront.set_linewidth(0.7)

rearPolyVal = np.polyval(coefRear, maxDrag)
fitRear, = ax.plot([np.amin(maxDrag), np.amax(maxDrag)], [rearPolyVal[minIdx], rearPolyVal[maxIdx]])
fitRear.set_color(lineRear.get_color())
fitRear.set_linestyle('--')
fitRear.set_linewidth(0.7)


ax.set_xlabel(r'$\tilde{f}_d$',fontsize=16)
ax.legend(loc='best', fontsize=16)

fname = 'pressure_ratio.png'
plt.savefig(fname)

plt.show()
