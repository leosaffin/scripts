import numpy as np
import cPickle as pickle
import diagnostics
import grid
import load
import convert

times = 37
job = 'xjjho'
zmin = 3000      # Minimum Height of points (m)
zmax = 15000     # Maximum Height of points (m)
binmin = 0.0     # Bottom of Advection Only Co-ordinate x-axis
binmax = 8.0     # Top of Advection Only Co-ordinate x-axis
binspace = 0.25  # Bin Spacing for advection only co-ordinates

# Fill an array of bin edges
bins = []
for n in xrange(int(binmax / binspace)):
    bins.append([binmin + binspace * n, binmin + binspace * (n + 1)])

# Define Diagnostics
names = ['Total Minus Advection Only PV', 'Sum of PV Tracers']
mean = {}
for name in names:
    mean[name] = np.zeros((times, len(bins)))

# Loop over times past zero
for time in xrange(1, times):
    # Load Arrays
    cubes = load.all(job, time, coord_cube=2)
    adv = cubes.extract('Advection Only PV')[0].data

    # Calculate the mass of each gridbox
    density = convert.density(cubes.extract('air_pressure')[1],
                              cubes.extract('air_temperature')[0])
    try:
        mass = volume * density.data
    except NameError:
        # Calculate the volume of each gridbox
        volume = grid.volume(cubes[0])
        altitude = cubes[0].coord('altitude').points
        mass = volume * density.data

    # Mask points away from the tropopause
    trop = diagnostics.tropopause(adv, altitude)
    masked_mass = np.ma.masked_where(trop == 0, mass)
    # Mask points at certain height levels
    masked_mass = np.ma.masked_where(altitude < zmin, masked_mass)
    masked_mass = np.ma.masked_where(altitude > zmax, masked_mass)

    for name in names:
        cube = load.extract(cubes, name)
        mean[name][time, :] = diagnostics.dipole(cube, adv, bins, masked_mass)

# Save output
data = {}
data['binmin'] = binmin
data['binmax'] = binmax
data['binspace'] = binspace
data['times'] = range(times)
data['zmin'] = zmin
data['zmax'] = zmax
data['dipole'] = mean
with open('../data/integrated_dipole.pkl', 'wb') as output:
    pickle.dump(data, output)
