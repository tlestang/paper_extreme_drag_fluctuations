# Reads the N = 85 drag signals corresponding the the extreme fluctuations
# of the average drag.
# + It sorts the events according to the fluctuations amplitude (AVG drag)
# + It computes the upper and lower bounds of the instant drag over all events.

# Outputs a formatted text file consiting of N lines.
# Next N lines are index of event sorted in descending order
# (most extreme event first)
# Prints max and min over instant timeseries to stdout

import numpy as np
import matplotlib.pyplot as plt

prefix = '/home/thibault/transition_hdd/thibault/These/lbm_code/seq/draft/etude_dynamique/' \
         + 'averaged_drag/'

sig=0.0412 # Standard deviation of instant. drag computed over CR
m=0.0252 # Average instant. drag computed over CR

Nevents = 85
F = np.zeros(Nevents) # Container for the average drag
# Containers for max and min over instant timeseries
minArray=np.zeros(Nevents)
maxArray=np.zeros(Nevents)
# Loops on the Nevents events 
for i in range(0,Nevents):
    fileName=prefix+'event_{:d}_AVG/'.format(i+1)+'data_force.datout'
    # Reads instant. drag
    f = np.fromfile(fileName, float, -1, "")
    F[i] = np.mean(f)

np.savetxt('data/list.txt', np.argsort(-F), '%0.2d')

