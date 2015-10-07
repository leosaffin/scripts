import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage.filters import gaussian_filter
import iris
import iris.quickplot as qplt
from mymodule import files, convert, grid, interpolate

sigma = 2
# Load final time PV tracers
cubes = iris.load('/home/lsaffi/data/iop5/trajectories/rdf_pv_etc2.nc')
adv = convert.calc('advection_only_pv', cubes)
tot = convert.calc('total_pv', cubes)
qsum = convert.calc('sum_of_physics_pv_tracers', cubes)
rdf_pv = convert.calc('reverse_domain_filled_pv', cubes)

rdf_pv_sm = gaussian_filter(rdf_pv.data, sigma)
rdf_pv_sm = rdf_pv.copy(data=rdf_pv_sm)
rdf_pv_sm.rename('smoothed_reverse_domain_filled_pv')
# Calculate epsilon from two different measure of conserved PV
res1 = tot.data - adv.data - qsum.data
res2 = tot.data - rdf_pv.data - qsum.data
res_sm = (gaussian_filter(tot.data, sigma) - rdf_pv_sm.data -
          gaussian_filter(qsum.data, sigma))

# Make epsilons into iris cubes
res1 = adv.copy(data=res1)
res1.rename('epsilon')
res2 = adv.copy(data=res2)
res2.rename('epsilon_rdf')
res_sm = adv.copy(data=res_sm)
res_sm.rename('smoothed_epsilon_rdf')

# Plot full PV measures
levs = np.linspace(0, 2, 9)
for cube in [adv, tot, rdf_pv, rdf_pv_sm]:
    plt.figure()
    qplt.contourf(cube, levs, cmap='cubehelix_r', extend='both')
    plt.gca().coastlines()
    plt.gca().gridlines()
    plt.savefig('/home/lsaffi/plots/iop5/' + cube.name() + '_500hpa.png')

# Plot epsilons
levs = np.linspace(-2, 2, 17)
levs = list(levs[0:8]) + list(levs[9:])
for cube in [res1, res2, res_sm]:
    plt.figure()
    qplt.contourf(cube, levs, cmap='bwr', extend='both')
    plt.gca().coastlines()
    plt.gca().gridlines()
    plt.savefig('/home/lsaffi/plots/iop5/' + cube.name() + '_500hpa.png')
