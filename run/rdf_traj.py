import numpy as np
import cPickle as pickle
import load
import grid
import trajectories

# Load Pressure and Advection Only PV
job='xjjho'
t_ref = 35
tracer = {}
pressure = {}
for time in xrange(1,t_ref+1):
    cubes = load.all(job,time)
    tracer[time] = cubes.extract('Advection Only PV')[0]
    pressure[time] = cubes.extract('air_pressure')[1]

# Load Trajectories
traj_file = '/home/lsaffi/data/out_3h.1'
traj_list = load.lagranto(traj_file)

# Trace PV at start of trajectory
for traj in traj_list:
    traj.rdf(t_ref,tracer,pressure,polelon=177.5,polelat=37.5)

ntraj = len(traj_list)
lon = np.zeros(ntraj)
lat = np.zeros(ntraj)
rdf_pv = np.zeros(ntraj)

for n in xrange(0,ntraj):
    lon[n] = traj_list[n].positions['lon'][-1]
    lat[n] = traj_list[n].positions['lat'][-1]
    rdf_pv[n] = traj_list[n].rdf_pv


[x_p,y_p] = grid.unrotate(cubes[0].coord('grid_longitude').points,
                          cubes[0].coord('grid_latitude').points, 177.5,37.5)
grid_pv = trajectories.regular_grid(rdf_pv,lon,lat,x_p,y_p)

# Save as pkl files
filename = '/home/lsaffi/data/rdf_pv.pkl'
with open(filename,'wb') as output:
    pickle.dump(grid_pv,output)

