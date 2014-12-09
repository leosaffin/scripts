import numpy as np
import matplotlib.pyplot as plt
import diagnostics
import grid
import load
import convert

lead_time = 36
job = 'xjjho'
zmin = 3000      # Minimum Height of points (m)
zmax = 15000     # Maximum Height of points (m)
binmin = 0.0     # Bottom of Advection Only Co-ordinate x-axis
binmax = 8.0     # Top of Advection Only Co-ordinate x-axis
binspace = 0.25  # Bin Spacing for advection only co-ordinates
# Define Diagnostics
names = ['Total Minus Advection Only PV',
         'Sum of PV Tracers',
         'Other PV Tracers',]

# Calculate array of bin-centres for plotting
bin_centres = np.arange(binmin + binspace/2.0,binmax,binspace)

# Load Arrays
cubes = load.all(job,lead_time)
adv = cubes.extract('Advection Only PV')[0].data

# Calculate the bins by advection only PV
bins = (np.floor((adv - binmin)/binspace)).astype(int)

# Calculate the volume of each gridbox
volume = grid.volume(cubes.extract('air_temperature')[0])

# Calculate the mass of each gridbox
density = convert.density(cubes.extract('air_pressure')[1],
                          cubes.extract('air_temperature')[0])
mass = volume*density.data

# Mask points away from the tropopause
altitude = cubes.extract('air_temperature')[0].coord('altitude').points
trop = diagnostics.tropopause(adv,altitude)
masked_mass = np.ma.masked_where(trop==0, mass)
# Mask points at certain height levels
masked_mass = np.ma.masked_where(altitude<zmin, masked_mass)
masked_mass = np.ma.masked_where(altitude>zmax, masked_mass)

for name in names:
    cube = load.extract(cubes,name)
    # Calculate the volume weight average for each bin
    mean = np.zeros(len(bin_centres))
    standard_deviation = np.zeros(len(bin_centres))
    for n in xrange(0,len(bin_centres)):
        weight_mask = np.ma.masked_where(bins!=n, masked_mass)
        total_weight = np.ma.sum(weight_mask)
        mean[n] = np.ma.sum(cube.data*weight_mask)/total_weight
        standard_deviation[n] = np.sqrt(np.ma.sum(weight_mask*(
                                        cube.data-mean[n])**2)
                                        /total_weight)
    # Plot dipole
    plt.errorbar(bin_centres,mean,yerr=standard_deviation, label=name)

# Fill in the rest of the plot
plt.plot([binmin, binmax], [0,0], color='k')
plt.xlabel('Advection Only PV')
plt.ylabel('Accumulated PV')
plt.legend(loc='best')
plt.savefig('IOP5_mw_dipole_T36.png')
