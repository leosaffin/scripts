# Plot the difference in trajectories 
# calculated with high and low resolution data
import cPickle as pickle
import numpy as np
import matplotlib.pyplot as plt

# Load previously calculated data
filename = '/home/lsaffi/data/lagranto_substeps.pkl'
with open(filename,'rb') as infile:
    diffs = pickle.load(infile)

ylabels = ['Longitude', 'Latitude', 'Pressure (hPa)']
names = ['lon','lat','p']

times = diffs[0]

# Plot data
for i,name in enumerate(names):
    plt.clf()
    plt.plot(times,diffs[1][name])
    plt.xlabel('Time (Hours)')
    plt.ylabel(ylabels[i])
    plt.savefig(name + '_traj_err.png')
