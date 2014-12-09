import numpy as np
import matplotlib.pyplot as plt
import iris
import convert
import diagnostics
import grid
import load
import smoothing

names = ['Total minus Advection Only PV',
         'Sum of PV Tracers',
         'Residual Error',
         'Advection Inconsistency PV']
'''
names = ['Short Wave Radiation PV',
         'Long Wave Radiation PV',
         'Radiation PV',
         'Microphysics PV',
         'Gravity Wave Drag PV',
         'Convection PV',
         'Boundary Layer PV']
'''
'''
linestyle = ['k-', 'r-', 'c-','y-',
             'k:', 'r:', 'c:','y:']

lead_time = 24
job = 'xkcqa'
zmin = 3000   # Bottom of area (m)
zmax = 15000  # Top of area (m)
binmin = -14.025
binmax = 14.025
binspace = 0.05         # Bin Spacing for advection only co-ordinates
# Calculate array of bin-centres for plotting
bin_edges=np.arange(binmin,binmax+binspace/2.0,binspace)
bin_centres = np.arange(binmin+binspace/2.0,binmax,binspace)

# Load Arrays
cubes = load.all(job,lead_time,theta_cube=2)

# Calculate The Volume of gridboxes
volume = grid.volume(cubes[0])
height = cubes[0].coord('level_height').points

z_0 = np.abs(height - zmin).argmin()
if height[z_0] - zmin < 0:
    z_0 += 1
z_m = np.abs(height - zmax).argmin()
if height[z_m] - zmax > 0:
    z_m -= 1
volume = volume[z_0:z_m,:,:]

cubes = cubes.extract(iris.Constraint(level_height=
                                      lambda cell: zmin < cell < zmax))
# Calculate the mass in each gridbox
mass = volume*convert.density(cubes.extract('air_pressure')[1],
                              cubes.extract('air_temperature')[0])

adv = cubes[0].data

kernel = smoothing.get_kernel(3,3,'mean')
'''
plt.clf()
# Loop over diagnostics
for i,name in enumerate(names):
    # Explicitly calculate selected diagnostics
    cube = load.extract(cubes,name)
    data = np.zeros(cube.data.shape)
    #data = np.ma.masked_where(adv>6,cube.data)
    for k in xrange(0,z_m-z_0):
        data[k,:,:] = smoothing.smooth2d(cube.data[k,:,:],kernel)
    #data = data[:,15:-15,15:-15]

    # Calculate pdf
    [pdf,edges] = np.histogram(data,bins=bin_edges,
                               weights=mass,density=True)
    pdf = np.log(pdf)
    plt.plot(bin_centres,pdf,linestyle[i],label=name)

plt.xlabel('PV')
plt.ylabel('Log Probability Density')
plt.axis('tight')
plt.title('Mass Weighted Probability Density Functions of PV Tracers 3-15km')
plt.legend(loc='best')

