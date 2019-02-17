import numpy as np
import matplotlib.style
import matplotlib.pyplot as plt

plt.style.use('ggplot')

def ret_gaussian(x):
    return (1./(np.sqrt(2.*np.pi)))*np.exp(-0.5*x*x)

musigma = np.fromfile("musigma_AVG_10.dat", float, -1, "");

buf = np.fromfile("pdfData_AVG.dat", float, -1, "");
n=len(buf)/2
f = buf[0:n]*musigma[1]
xi = (buf[n:]-musigma[0])/musigma[1]

fig, ax = plt.subplots(figsize=(8,5),constrained_layout=True)

lineSQ, = ax.plot(xi,f)
lineSQ.set_label('PDF of $F_T$')



# buf = np.fromfile("pdfData_NOSQ.dat", float, -1, "");
# n=len(buf)/2
# f = buf[0:n]
# xi = buf[n:]
lineNOSQ, = ax.plot(xi,ret_gaussian(xi), label='Gaussian PDF')


ax.set_yscale('log')
ax.set_xticks([-5,-3,-1,0,1,3,5])
ax.set_xticklabels(['$-5\sigma_T$','$-3\sigma_T$','$-\sigma_T$','$0$','$\sigma_T$','$3\sigma_T$','$5\sigma_T$'], fontsize=16)
ax.set_xlabel('$F_T$',fontsize=22)
plt.ylabel('$\log(PDF)$',fontsize=22)
ax.legend(loc='best',fontsize=22)

fname = 'PDF_AVG.png'
plt.savefig(fname)

plt.show()
