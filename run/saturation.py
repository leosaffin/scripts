import numpy as np
import cPickle as pickle
import iris

import load
import grid
import convert

# Define Diagnostics
names = ['Total PV',
         'Total Minus Advection Only PV',
         'Sum of PV Tracers',
         'Residual Error',
         'Short Wave Radiation PV',
         'Long Wave Radiation PV',
         'Radiation PV',
         'Microphysics PV',
         'Gravity Wave Drag PV',
         'Convection PV',
         'Boundary Layer PV',
         'Advection Inconsistency PV']

job = 'xjjhz'
nt = 120
theta_min = 330
theta_max = 350
times = np.arange(0,nt+1)
rms_north = np.zeros((len(names),nt+1))
rms_south = np.zeros((len(names),nt+1))

# loop over time
for t in xrange(1,nt+1):
    print 'time =',t
    # Load Tracers
    cubes = load.all(job,t)

    # Calculate grid volume
    if t==1: 
        volume = grid.volume_global(cubes.extract('air_temperature')[0])

    # Calculate Potential Temperature
    theta = convert.T_to_theta(cubes.extract('air_temperature')[0].data,
                               pressure = cubes.extract('air_pressure')[1].data)
    # Calculate the mass in each gridbox
    density = convert.density(cubes.extract('air_pressure')[1].data,
                              cubes.extract('air_temperature')[0].data)
    mass = volume*density

    # Integrate (roughly) between isentropic layers
    mass = np.ma.masked_where(theta<theta_min,mass)
    mass = np.ma.masked_where(theta>theta_max,mass)

    # Loop of diagnostics
    for i,name in enumerate(names):
        # Extract selected diagnostics
        cube = load.extract(cubes,name)
        # Calculate RMS Diagnostics
        rms_north[i,t] = np.ma.mean((cube.data[:,0:239,:]*mass[:,0:239,:]))
        rms_south[i,t] = np.ma.mean((cube.data[:,240:480,:]*mass[:,240:480,:]))

# Save data as pickled files
output = open('../data/saturation.pkl', 'wb')
pickle.dump(names, output)
pickle.dump(rms_north, output)
pickle.dump(rms_south, output)
output.close()
