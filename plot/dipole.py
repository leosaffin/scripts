import matplotlib.pyplot as plt
import cPickle as pickle
import numpy as np

names = ['Total Minus Advection Only PV','Sum of PV Tracers']

# Load PV dipoles
with open('/home/lsaffi/data/integrated_dipole.pkl','rb') as infile:
    data = pickle.load(infile)

binmin = data['binmin']
binmax = data['binmax']
binspace = data['binspace']
times = data['times']
mean = data['dipole']

# Calculate array of bin-centres for plotting
bin_centres = np.arange(binmin + binspace/2.0,binmax,binspace)

levels = np.arange(-0.145,0.146,0.01)

for name in names:
    plt.clf()
    plt.contourf(times,bin_centres,mean[name].transpose(),
                 levels,cmap='bwr',extend='both')
    plt.colorbar(label='PVU',ticks=[levels[0],0,levels[-1]],
                 orientation='horizontal')
    plt.contour(times,bin_centres,mean[name].transpose(),
                [0],colors='k',linestyles='--')
    plt.xlabel('Time (Hours)')
    plt.ylabel('Advection Only PV (PVU)')
    plt.savefig('dipole' + str(name) + '.png')

