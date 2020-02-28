import numpy as np
import matplotlib.style
import matplotlib.pyplot as plt

plt.style.use('ggplot')

def ret_gaussian(x):
    # Returns zero-mean, unit variance at point
    return (1./(np.sqrt(2.*np.pi)))*np.exp(-0.5*x*x)

musigma = np.fromfile("../../data/musigma_AVG_10.dat", float, -1, "");

buf = np.fromfile("../../data/pdfData_AVG.dat", float, -1, "");
n=int(len(buf)/2)
f = buf[0:n]*musigma[1]
xi = (buf[n:]-musigma[0])/musigma[1]

# Fit positive tail of the distribution for the time-averaged drag
# Get indices that correspond to xi>3\sigma
I = np.where(xi>3)
xiTrunc = xi[I]
logf = np.log(f[I])
c = np.polyfit(xiTrunc,logf,2)
p = np.poly1d(c) # p is the polynomial and can be evaluated

fig, ax = plt.subplots(figsize=(8,5),constrained_layout=True)
# plots the PDF estimate
line, = ax.plot(xi,f)

# Plots the gaussian fit based on mu and sigma
lineGauss, = ax.plot(xi,ret_gaussian(xi), label='Gaussian estimate')

# Plots the local least-square fit for the positive tail
#lineFit, = ax.plot(xiTrunc,np.exp(p(xiTrunc)), linewidth=2, \
#                   color='k')

# Set figure parameters
ax.set_yscale('log')
ax.set_xticks([-5,-3,-1,0,1,3,5])
ax.set_xticklabels(['$-5\sigma_T$','$-3\sigma_T$','$-\sigma_T$',
                    '$0$','$\sigma_T$','$3\sigma_T$','$5\sigma_T$'], fontsize=16)
ax.set_xlabel('$x=F_T$',fontsize=22)
plt.ylabel('$P(x)$',fontsize=22)
ax.legend(loc='best',fontsize=22)

# Prints figure
fname = 'PDF_AVG.png'
plt.savefig(fname)

plt.show()
