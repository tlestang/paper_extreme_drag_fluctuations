import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def returntimes(amax, wghts, duration):
        """
        Estimate the return time of an observable using AMS sampling
        """
        wghtstilde = wghts[np.argsort(amax)][::-1]
        amaxtilde = np.sort(amax)[::-1]
        ra = np.zeros(len(amax))
        for i, a in enumerate(amaxtilde):
                ra[i] = -duration/np.log(1-np.sum(wghtstilde[0:i+1]))
        I = ~np.isnan(ra)
        return amaxtilde[I], ra[I]

def compute_return_times(dirname, Ta, T, k, N, tau_c=2000):
        filename = os.path.join(dirname, 'A.datout')
        A = np.fromfile(filename, float, -1,'')

        filename = os.path.join(dirname, 'amax.datout')
        amax = np.fromfile(filename, float, -1,'')
        amax = amax

        filename = os.path.join(dirname, 'SCGF.datout')
        lam = np.fromfile(filename, float, -1,'')

        wghts = np.array([np.exp(Ta*tau_c*lam)*np.exp(-k*A_*Ta*tau_c)/N for A_ in A])
        return returntimes(amax, wghts, Ta-T)

def compute_return_times_no_dups(dirname, Ta, T, k, N, tau_c=2000):
        filename = os.path.join(dirname, 'A.datout')
        A = np.fromfile(filename, float, -1,'')

        filename = os.path.join(dirname, 'amax.datout')
        amax = np.fromfile(filename, float, -1,'')
        amax = amax

        filename = os.path.join(dirname, 'SCGF.datout')
        lam = np.fromfile(filename, float, -1,'')

        unique_amax, I = np.unique(amax, return_index=True)
        unique_A = A[I]
        N = len(unique_amax)
        wghts = np.array([np.exp(Ta*lam*tau_c)*np.exp(-k*A_*Ta*tau_c)/N for A_ in unique_A])
        return returntimes(unique_amax, wghts, Ta-T)



    
    
