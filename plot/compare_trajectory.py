# Plot the difference in trajectories 
# calculated with high and low resolution data
import cPickle as pickle
import numpy as np
import matplotlib.pyplot as plt

# Load previously calculated data
filename = '/home/lsaffi/data/3h_vs_1h_trajectories.pkl'
with open(filename,'rb') as infile:
    diffs = pickle.load(infile)

ylabels = ['Longitude', 'Latitude', 'Pressure (hPa)']
names = ['lon.png','lat.png','pres.png']

# Plot data
for n,diff in enumerate(diffs):
    xvalues = np.sort(np.array(diff.keys()))
    yvalues = np.zeros(len(diff))
    for i,key in enumerate(xvalues):
        yvalues[i] = diff[key]
    plt.figure(n)
    plt.plot(xvalues,yvalues)
    plt.xlabel('Time (Hours)')
    plt.ylabel(ylabels[n])
    plt.savefig(names[n])
