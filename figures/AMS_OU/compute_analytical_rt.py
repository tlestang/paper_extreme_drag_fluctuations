import numpy as np
import scipy.integrate as integrate
import matplotlib.pyplot as plt
from os.path import abspath, dirname, join, basename

prefix = join(
    abspath(dirname(__file__)), "data"
    )

def g(z):
    return np.exp(z*z)
def f0(y):
    I = integrate.quad(lambda z: np.exp(-z*z),-np.inf,y)
    return np.exp(y*y)*I
def fstat(y):
    I = integrate.quad(lambda z: np.exp(-z*z),-np.inf,y)[0]
    return np.exp(y*y)*I*I
sig = 1./np.sqrt(2.)
avec = np.linspace(sig,10.5*sig,128);
oneOvEps = 2.
prefact = (oneOvEps*oneOvEps*oneOvEps) / (2.*np.pi)

k = 0;
#r0 = np.zeros(len(aVec))
rstat = np.zeros(len(avec))
for a in avec:
#    r0[k] = oneOvEps * integrate.quad(f0,0,a)
    rstat[k] = np.sqrt(prefact) * integrate.quad(fstat,-20,a)[0]
    k = k+1;

fo = open(join(prefix, "return_time_analytical.dat"), "wb")
avec.tofile(fo, "")
rstat.tofile(fo, "")
fo.close()
    
  
