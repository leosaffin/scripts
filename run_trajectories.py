import numpy as np
import matplotlib.pyplot as plt
import trajectories
import grid
import load
import interpolate

cubes = load.all('xjjho',35)
lon = cubes[0].coord('grid_longitude').points
lat = cubes[0].coord('grid_latitude').points
[x_p,y_p] = grid.unrotate(lon,lat,177.5,37.5)
domain = [lon[15],lon[-16],lat[15],lat[-16]]

# Load Trajectories Including Boundary Conditions
data = trajectories.load_traj('/projects/diamet/lsaffi/data/out.1',
                              36,domain=domain,polelon=177.5,polelat=37.5)

# Calculate the advection only PV at the start of the trajectories
pv_start = trajectories.gather_ends(data,36,'xjjho',polelon=177.5,polelat=37.5)
# Interpolate the advection only PV to grid points
field = trajectories.regular_grid(data,pv_start,x_p,y_p)
field = np.transpose(field)

# Load final time PV tracers
adv = cubes.extract('Advection Only PV')[0].data
diab = (cubes.extract('Atmospheric Physics 1 PV')[0].data + 
        cubes.extract('Atmospheric Physics 2 PV')[0].data)
other = (cubes.extract('Cloud Rebalancing PV')[0].data + 
         cubes.extract('Pressure Solver PV')[0].data)
tot = cubes.extract('Total PV')[0].data
p_theta = cubes.extract('air_pressure')[1].data
adv500 = interpolate.any_to_pressure(adv,p_theta,[500])
diab500 = interpolate.any_to_pressure(diab,p_theta,[500])
other500 = interpolate.any_to_pressure(other,p_theta,[500])
tot500 = interpolate.any_to_pressure(tot,p_theta,[500])

# Calculate the residual using PV tracers
res1 = tot500 - adv500 - diab500 - other500
# Calculate the residual from reverse domain filled PV
res2 = tot500 - field - diab500 - other500

# Plot the residuals
cscale = np.arange(-2,2 + 2/9.0,2/4.5)
plt.figure(1)
plt.contourf(lon,lat,res1[0,:,:],cscale,cmap='bwr',extend='both')
plt.colorbar()
#plt.contour(lon,lat,lsm,colors='k')
plt.title('IOP5 T+35H PV Budget Residual at 500hPa')
plt.savefig('residual_normal.png')
plt.figure(2)
plt.contourf(lon,lat,res2[0,:,:],cscale,cmap='bwr',extend='both')
plt.colorbar()
#plt.contour(lon,lat,lsm,colors='k')
plt.title('IOP5 T+35H PV Budget Residual at 500hPa')
plt.savefig('residual_trajectory.png')
plt.ion()
plt.show()
