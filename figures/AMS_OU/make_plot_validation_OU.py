import numpy as np
import matplotlib.style
import matplotlib.pyplot as plt

plt.style.use('ggplot')

Ta = 5;
Nc = 32;
sig = 1/np.sqrt(2);

compTime = np.fromfile("./comp.dat", float, -1, "")
amax = np.fromfile("./amax.dat", float, -1, "")
Z = np.fromfile("./Z.dat", float, -1, "")

xx = Ta*Nc + np.cumsum(compTime);

buf = np.fromfile("./return_time_analytical.dat", float, -1, "")
n = int(len(buf)/2)
avec = buf[0:n]
rtheo = buf[n:]

fig,ax = plt.subplots(figsize=(8,5),constrained_layout=True)
#ax.plot(xx,amax/sig,marker='o',markersize=1,linestyle='None');
lineLvl, = ax.plot(xx,Z/sig,linestyle='-',label='TAMS');
ax.plot(rtheo,avec/sig, linestyle='-',label='Direct sampling (return time)')
plt.annotate('', xy=(12584,10), xytext=(1.7e19,10), arrowprops=dict(arrowstyle='<->',lw=2,color=lineLvl.get_color()))
plt.text(1e7, 10.2, r'$C(a) = 10^{-17}r(a), a=10\sigma$', fontsize=18)
ax.set_xscale('log')
ax.set_xlabel(r'$r(x \geq a), C_{TAMS}(x \geq a)$',fontsize=22)
ax.set_ylabel('$a$',fontsize=22)
ax.set_yticks([0,2,4,6,8,10])
ax.set_xticks([1e2,1e8,1e14,1e20])
ax.set_xticklabels((r'$10^2\tau_c$',r'$10^8\tau_c$',r'$10^{14}\tau_c$',r'$10^{20}\tau_c$'))
ax.set_yticklabels((r'$0$',r'$2\sigma$',r'$4\sigma$',r'$6\sigma$',r'$8\sigma$',r'$10\sigma$'))
ax.legend(loc='best', fontsize=18)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)

fname = 'AMS_OU.eps'
plt.savefig(fname)

plt.show()
