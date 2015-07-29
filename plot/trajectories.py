import numpy as np
import matplotlib.pyplot as plt
import iris
from mymodule import files, convert, grid, interpolate, plot

# Load RDF PV
rdf_pv = iris.load('/home/lsaffi/data/rdf_pv_trace.nc')[0]
rdf_pv.rename('reverse_domain_filled_pv')

# Load final time PV tracers
cubes = files.load('/projects/diamet/lsaffi/xjjhq/*035.pp')
adv = convert.calc('advection_only_pv', cubes)
tot = convert.calc('total_pv', cubes)
qsum = convert.calc('sum_of_physics_pv_tracers', cubes)
p = cubes.extract('air_pressure')[1]

# Add pressure as a coordinate
pcoord = grid.make_coord(p)
adv.add_aux_coord(pcoord, [0, 1, 2])
tot.add_aux_coord(pcoord, [0, 1, 2])
qsum.add_aux_coord(pcoord, [0, 1, 2])

# Interpolate to pressure levels
adv = interpolate.to_level(adv, air_pressure=[500])[0]
tot = interpolate.to_level(tot, air_pressure=[500])[0]
qsum = interpolate.to_level(qsum, air_pressure=[500])[0]

# Calculate epsilon from two different measure of conserved PV
res1 = tot.data - adv.data - qsum.data
res2 = tot.data - rdf_pv.data - qsum.data

# Make epsilons into iris cubes
res1 = adv.copy(data=res1)
res1.rename('epsilon')
res2 = adv.copy(data=res2)
res2.rename('epsilon_rdf')

# Plot full PV measures
levs = np.linspace(0, 2, 9)
for cube in [adv, tot, rdf_pv]:
    plt.figure()
    plot.level(cube, adv, levs, cmap='cubehelix_r', extend='both')
    plt.savefig('/home/lsaffi/plots/' + cube.name() + '_500hpa.png')
'''
# Plot epsilons
levs = np.linspace(-2.1, 2.1, 16)
levs = [-2, -1.75, -1.5, -1.25, -1, -0.75, -0.5, -0.25,
        0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2]
for cube in [res1, res2]:
    plt.figure()
    plot.level(cube, cube, levs, cmap='bwr', extend='both')
    plt.savefig('/home/lsaffi/plots/' + cube.name() + '_500hpa.png')
'''
