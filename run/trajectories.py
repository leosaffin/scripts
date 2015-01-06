import numpy as np
import cPickle as pickle
import trajectories
import grid
import load

cubes = load.all('xjjho',35)
lon = cubes[0].coord('grid_longitude').points
lat = cubes[0].coord('grid_latitude').points
[x_p,y_p] = grid.unrotate(lon,lat,177.5,37.5)
domain = [lon[15],lon[-16],lat[15],lat[-16]]

# Load Trajectories Including Boundary Conditions
data = trajectories.load_traj('/projects/diamet/lsaffi/data/out.1',
                              36,domain=domain,polelon=177.5,polelat=37.5)

# Calculate the advection only PV at the start of the trajectories
rdf_pv = trajectories.gather_ends(data,36,'xjjho',polelon=177.5,polelat=37.5)
# Interpolate the advection only PV to grid points
rdf_pv = trajectories.regular_grid(data,rdf_pv,x_p,y_p)
rdf_pv.transpose()

# Save data as pickled files
output = open('/home/lsaffi/data/rdf_pv.pkl', 'wb')
pickle.dump(rdf_pv, output)
output.close()
