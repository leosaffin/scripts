from mymodule import load
from mymodule import grid
from mymodule.trajectories import load as trload
from mymodule.trajectories import rdf
from mymodule import plot
import cPickle as pickle
import numpy as np
import matplotlib.pyplot as plt

polelon = 177.5
polelat = 37.5
lonmin = 15
lonmax = -16
latmin = 15
latmax = -16
outfile = '/home/lsaffi/rdf_pv.pkl'

# Load the data at the departure time
cubes = load.full('xjjho',2)
q_adv = cubes.extract('Advection Only PV')[0]
pressure = cubes.extract('air_pressure')[1]
pressure.convert_units('hPa')
lon,lat = grid.xycoords(q_adv)

# Load the trajectory data
filename = '/home/lsaffi/data/out_1h.1'
trajectories = trload.filtered(filename,lonmin=lon[lonmin],
                               lonmax=lon[lonmax],latmin=lat[latmin],
                               latmax=lat[latmax],polelon=polelon,
                               polelat=polelat)


# Find the data at departure points
rdf_pv = rdf.fill(trajectories,q_adv.data,pressure.data,lon,lat)

# Save the result
with open(outfile,'wb') as output:
    pickle.dump(rdf_pv,output)

# Put back in a cube
subcube = q_adv[0]
rdf_pv = q_adv.copy(data=q_adv)

# Plot the output
levels = np.arange(0,10.1,0.25)
plot.level(rdf_pv,levels,rdf_pv,rdf_pv)
plt.savefig('rdf_pv.png')
