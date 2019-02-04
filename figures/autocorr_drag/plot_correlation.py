import numpy as np
import matplotlib.style
import matplotlib.pyplot as plt

plt.style.use('ggplot')


buf = np.fromfile("correlationData.dat", float, -1, "");
n=len(buf)/2
tDomain = buf[0:n]
c = buf[n:]

fig,ax = plt.subplots(1,1)
ax.set_xlim(0, 3.5)
line0, =ax.plot(np.array([0, 3.5]), np.array([0, 0]))
lineC, = ax.plot(tDomain/2000,c)
line0.set_linestyle('--')
line0.set_linewidth(0.7)

ax.set_xlabel(r'$\tau$',fontsize=16)
plt.ylabel(r'$C(\tau)$',fontsize=16)

plt.show()
