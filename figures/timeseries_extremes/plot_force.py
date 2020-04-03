import numpy as np
import matplotlib.pyplot as plt


prefix = '/home/tlestang/transition_hdd/thibault/These/lbm_code/seq/draft/etude_dynamique/instant_events/'

sig=0.0412
m=0.0252

N = 8000;
tspan = np.linspace(-2,2,N)
Nevents=104;
fbuf=np.zeros((Nevents, N))
for i in range(0,Nevents):
    path_to_file = prefix+'event_{:d}_feb/data_force.datout'.format(i+1)
    fid = open(path_to_file, "rb")
    fbuf[i,:] = (np.fromfile(fid, float, N, "")-m)/sig
    fid.close()

F=np.mean(fbuf,axis=0) # Compute mean over columns
Fdev=np.std(fbuf,axis=0)


fig, ax = plt.subplots(figsize=(8,5),constrained_layout=True)
plt.plot(tspan,F,label='Average')
plt.fill_between(tspan, F-Fdev, F+Fdev, color='gray', alpha=0.2,label='Standard dev.')
ax.set_xticks([-2,-0.5,0,0.5,2])
#ax.set_xticklabels(['${:d}\\tau_c$'.format(x) for x in ax.get_xticks()]),
ax.set_xticklabels(['$t^{\star}-2\\tau_c$','$t^{\star}-\\tau_c /2$','$t^{\star}$','$t^{\star}+\\tau_c /2$','$t^{\star}+2\\tau_c$'], fontsize=16)
ax.set_yticklabels(['${:2.1f}\\sigma$'.format(y) for y in ax.get_yticks()], fontsize=16)
ax.set_xlim((-2,2))
plt.annotate('', xy=(-0.5,-0.35), xytext=(0.5,-0.35), arrowprops=dict(arrowstyle='<->',lw=2))
plt.text(-0.1, -0.05, r'$\tau_c$', fontsize=18)
ax.legend(loc='best',fontsize=16)
ax.set_ylabel('$\\tilde{f}_d(t)$',fontsize=22)
ax.set_xlabel('$t$',fontsize=22)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)

fname = 'timeseries_extremes.eps'
plt.savefig(fname)

plt.show()
