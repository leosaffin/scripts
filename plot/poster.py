import iris.quickplot as qplt
import iris.plot as iplt
import matplotlib.pyplot as plt
import numpy as np
import cPickle as pickle
import load

# Load Land Sea Mask
with open('../data/NAE.pkl') as infile:
    nae = pickle.load(infile)
lsm = nae[0]

# Load Data
cubes = load.all('xjjho',36,coord_cube=2)
total_pv = cubes.extract('Total PV')[0]
surf_p = cubes.extract('surface_air_pressure')[0]
# Set Land points to 0
surf_p.data = surf_p.data*(lsm - 1)*-1

# Get Grid Info
x = cubes[0].coord('grid_longitude').points
x = x-360
y = cubes[0].coord('grid_latitude').points
yp = np.zeros(x.shape)
yp[:] = y[200]

# Plot PV
qplt.contourf(total_pv[33,15:345,15:585],np.arange(2,10.1,0.25),
              cmap='cubehelix',extend='max')
iplt.contour(cubes[0][33,15:345,15:585],[2],linestyles='--',colors='k')

# Plot Surface Pressure at Sea
iplt.contour(surf_p[15:345,15:585],np.arange(970,1031,5),colors='k')

# Automatically Label Contour Lines
#ax = iplt.contour(surf_p[15:345,15:585],np.arange(970,1031,15),colors='k')
#plt.clabel(ax,fontsize='10',colors='r')
# Manually Label Contour Lines
plt.annotate(970,(-1.77,12.65))
plt.annotate(985,(-9.05,8.88))
plt.annotate(1000,(-10.8,1.075))
plt.annotate(1015,(-16.32,-6.464))

# Add Land Sea Image
plt.gca().stock_img()
# Draw Coastlines
plt.gca().coastlines()

# Plot Cross Section Line
plt.plot(x[15:585],yp[15:585],'--',color='r')

# Remove Title
plt.title('')
# Save Figure
plt.savefig('poster_plot_adv.png')

levels = np.arange(-2,2.1,2/13.5)

for cube in cubes:
    if 'PV' in cube.name():
        plt.clf()
        qplt.contourf(cube[0:45,200,15:585],levels,cmap='bwr',extend='both')
        iplt.contour(total_pv[0:45,200,15:585],[2],color='k')
        iplt.contour(cubes[0][0:45,200,15:585],[2],linestyles='--',color='k')
        plt.savefig(cube.name() + '_adv.png')
