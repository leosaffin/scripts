import numpy as np
import matplotlib.pyplot as plt
import cPickle as pickle
import load
import interpolate

# Load RDF PV
with open('/home/lsaffi/data/rdf_pv.pkl','rb') as infile:
    rdf_pv = pickle.load(infile)

# Load final time PV tracers
cubes = load.all('xjjho',35)
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
