import numpy as np
import matplotlib.pyplot as plt
import cPickle as pickle

# Define a list of linestyles for plotting
linestyle = ['k-','k--','k-.','k:',
             'r-','r--','r-.','r:',
             'c-','c--','c-.','c:',
             'y-','y--','y-.','y:',]

# List Selected Names To Plot
selected = ['']

# Load previously output data
infile = open('/home/lsaffi/data/saturation.pkl', 'rb')
names = pickle.load(infile)
rms_north = pickle.load(infile)
rms_south = pickle.load(infile)
infile.close()
nt = 120
times = np.arange(0,nt+1)

# Plot rms diagnostics
for i,name in enumerate(names):
    if name in selected
        plt.plot(times,rms_south[i,:],linestyle[i],label=name)
plt.xlabel('Time (Hours)')
plt.ylabel('PV (PVU)')
plt.title('Mass Weighted Integral of PV 330-350K Southern Hemisphere')
#plt.legend(loc='best')
plt.axis('tight')
#plt.savefig('global_mw_integral_south_no_legend.png')
