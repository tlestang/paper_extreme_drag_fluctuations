import numpy as np
import matplotlib.style
import matplotlib.pyplot as plt

plt.style.use('ggplot')


buf = np.fromfile("pdfData_SQ_centered.dat", float, -1, "");
n=len(buf)/2
f = buf[0:n]
xi = buf[n:]

fig,ax = plt.subplots(1,1, figsize=(7.5,5), constrained_layout=True)
lineSQ, = ax.plot(xi,f)
lineSQ.set_label('With obstacle')

buf = np.fromfile("pdfData_NOSQ.dat", float, -1, "");
n=len(buf)/2
f = buf[0:n]
xi = buf[n:]
lineNOSQ, = ax.plot(xi,f, label='No obstacle')

ax.set_yscale('log')
ax.set_xlabel('$f_d - \\bar{f}_d$',fontsize=22)
plt.ylabel('$\log(PDF)$',fontsize=22)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
ax.legend(loc='upper right', fontsize=16)

fname = 'PDF_drag.png'
plt.savefig(fname)

plt.show()
