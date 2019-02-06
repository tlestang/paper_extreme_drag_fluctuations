import numpy as np
import matplotlib.style
import matplotlib.pyplot as plt

plt.style.use('ggplot')


buf = np.fromfile("pdfData_SQ_centered.dat", float, -1, "");
n=len(buf)/2
f = buf[0:n]
xi = buf[n:]

fig,ax = plt.subplots(1,1)
lineSQ, = ax.plot(xi,f)
lineSQ.set_label('With obstacle')

buf = np.fromfile("pdfData_NOSQ.dat", float, -1, "");
n=len(buf)/2
f = buf[0:n]
xi = buf[n:]
lineNOSQ, = ax.plot(xi,f, label='No obstacle')

ax.set_yscale('log')
ax.set_xlabel('$f_d$',fontsize=16)
plt.ylabel('$\log(PDF)$',fontsize=16)
ax.legend(loc='upper right')

fname = 'PDF_drag.png'
plt.savefig(fname)

plt.show()
