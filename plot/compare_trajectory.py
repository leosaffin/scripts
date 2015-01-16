# Plot the difference in trajectories 
# calculated with high and low resolution data
import cPickle as pickle
import numpy as np
import matplotlib.pyplot as plt

# Load previously calculated data
filename = '/home/lsaffi/data/3h_vs_1h_trajectories'
with open(filename,'rb') as infile:
    diffs = pickle.load(infile)

# Plot data

for n,diff in enumerate(diffs):
    xvalues = np.sort(np.array(diff.keys()))
    yvalues = np.zeros(len(diff))
    for i,key in enumerate(xvalues):
        yvalues[i] = diff[key]
    plt.figure(n)
    plt.plot(xvalues,yvalues)



