import matplotlib.pyplot as plt
import cpickle as pickle

# Define a list of linestyles for plotting
linestyle = ['k-','k--','k-.','k:',
             'r-','r--','r-.','r:',
             'c-','c--','c-.','c:',
             'y-','y--','y-.','y:',]

# Load previously output data
infile = open('~/data/saturation.pkl', 'rb')
names = pickle.load(infile)
rms = pickle.load(infile)

# Plot rms diagnostics
for i,name in enumerate(names):
    plt.plot(times,rms[i,:],linestyle[i],label=name)
plt.ion()
plt.xlabel('Time (Hours)')
plt.ylabel('PV (PVU)')
plt.title('Mass Weighted Integral of PV 330-350K')
#plt.legend(loc='best')
plt.axis('tight')
plt.savefig('global_mw_integral.png')
