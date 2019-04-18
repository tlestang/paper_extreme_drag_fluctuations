import matplotlib.pyplot as plt
import numpy as np
from scipy import special,integrate

def ret_gaussian(x):
    """ Returns zero-mean, unit variance at point
    """
    return (1./(np.sqrt(2.*np.pi)))*np.exp(-0.5*x*x)

def integrate_composite_pdf(borneInf, borneSup, pol, norm_factor=1):
    """Return value of integral of the piecewise function
         f(x) = f_gauss(x) for x <=3
                f_fit(x)   for x > 3
       where f_gauss is the zero-mean, unit variance Gaussian PDF and 
       f_fit is the exponential of a polynomial pol

    Parameters
    ----------
    borneInf : float
    borneSup : float
    pol : poly1d
    norm_factor : float, optional

    Returns
    -------
    integral : float
    """
    xvec = np.linspace(borneInf,borneSup,1000)
    dx = xvec[1]-xvec[0]
    gaussian_part = ret_gaussian(xvec[xvec<=3])
    non_gaussian_part = np.exp(p(xvec[xvec>3]))
    full_pdf = np.append(gaussian_part,non_gaussian_part)

    return integrate.trapz(full_pdf,xvec,dx)/norm_factor

Nc = 16384 # Nb of total traj
NN = 20 # Nb of cloning steps
sig = 0.0087714 # Std dev of time-averaged drag (T=10\tau_c)

# List containing the names of the result directories
directories = ['k_0.02_2018_03_26_10_01_46/', 'k_0.025_2018_03_25_20_13_40/',
	   'k_0.03_2018_03_25_20_13_40/']
prefix = '/home/tlestang/transition_hdd/thibault/These/tailleur_lecomte/lbm/2_sq/' \
         + 'grid/illustration_IS/'

# Open a text file
fo = open("foo.txt", "w")
for directory in directories:
    # Read labels and average drag
    # labels is a Nc*NN vector containing the index of ancestors
    # for the next evolution step
    # Ex: Ancestor for traj. 1 after third step is
    # labels[2*Nc + 1]
    #          |
    #    Ancestors for first 2 steps run from 0 to 2*Nc-1   
    full_path = prefix+directory+'labels.datout'
    labels = np.fromfile(full_path, np.int32, -1, "")
    full_path = prefix+directory+'A.datout'
    A = np.fromfile(full_path, float, -1, "")
    # Note that here A takes last cloning step into account

    ## ll is a Nc*NN that contains the ancestor for the continuous
    ## trajectories.
    ll = np.zeros(Nc*NN).reshape(Nc,NN)
    ## ll is constructed as follows
    for j in range(0,Nc):
        ll[j,NN-1] = labels[(NN-1)*Nc+j]
        for evol_step in range(NN-2,-1,-1):
            ancestor_idx = int(ll[j,evol_step+1])
            ll[j,evol_step] = labels[evol_step*Nc + ancestor_idx]

            
    fo.write(directory+'\n')
    fo.write('------------\n')
    fo.write('\\begin{tabular}\n')

    for threshold in [1, 5, 10]:
        #  If two traj start from the same ancestor at time t_threshold,
        # then they necessarily overlap over [0:t_threshold]
        array_of_unique, indices_of_unique = np.unique(ll[:,threshold-1], return_index=True)
        AA = A[indices_of_unique]/sig
        for a in range(1,6):
            nb_traj = len(AA[AA>a])
            fo.write('{}'.format(nb_traj))
            if a<5:
                fo.write(' & ')
            else:
                fo.write(' \\\\ \n')

    # Compute the average number of trajectories which time-average is
    # above the threshold a, among Nc trajectories
    # The PDF for the time-avg drag above 3sigma is estimated by means of least-square
    # fitting the upper tail of the PDF estimate

    buf = np.fromfile("../PDF_AVG/pdfData_AVG.dat", float, -1, "");
    musigma = np.fromfile("../PDF_AVG/musigma_AVG_10.dat", float, -1, "");
    n=int(len(buf)/2)
    f = buf[0:n]*musigma[1]
    xi = (buf[n:]-musigma[0])/musigma[1]
    I = np.where(xi>3)
    xiTrunc = xi[I]
    logf = np.log(f[I])
    c = np.polyfit(xiTrunc,logf,2)
    p = np.poly1d(c) # p is the polynomial and can be evaluated

    # Compute normalisation factor
    norm_factor = integrate_composite_pdf(-10,5,p)

    for a in range(1,6):
        nb_traj_direct = Nc*(1-integrate_composite_pdf(-10,a,p,norm_factor))
        fo.write('{:2.3f}'.format(nb_traj_direct))
        if a<5:
            fo.write(' & ')
        else:
            fo.write(' \\\\ \n')

    fo.write('\\end{tabular}\n')
    fo.write('\n')

fo.close()
            
    
