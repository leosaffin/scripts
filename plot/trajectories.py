import numpy as np
import matplotlib.pyplot as plt
import cPickle as pickle
from mymodule import files, convert, grid, interpolate, plot

# Load RDF PV
with open('/home/lsaffi/data/rdf_pv.pkl', 'rb') as infile:
    rdf_pv = pickle.load(infile)

# Load final time PV tracers
cubes = files.load('/projects/diamet/lsaffi/xjjhq/*035.pp')
adv = convert.calc('advection_only_pv', cubes)
tot = convert.calc('total_pv', cubes)
p = cubes.extract('air_pressure')[1]

# Add pressure as a coordinate
pcoord = grid.make_coord(p)
adv.add_aux_coord(pcoord, [0, 1, 2])
tot.add_aux_coord(pcoord, [0, 1, 2])

# Interpolate to pressure levels
adv = interpolate.to_level(adv, air_pressure=[5])[0]
tot = interpolate.to_level(tot, air_pressure=[5])[0]

rdf_pv = rdf_pv.T[15:345, 15:585]
rdf_pv = cubes[0][0].copy(data=rdf_pv)
rdf_pv.rename('reverse_domain_filled_pv')
files.save([rdf_pv], '/home/lsaffi/data/IOP5/rdf_pv.pp')

levs = np.linspace(0, 2, 11)
for cube in [adv, tot, rdf_pv]:
    plt.figure()
    plot.level(cube, cube, levs, cmap='cubehelix_r', extend='both')
    plt.savefig('/home/lsaffi/plots/' + cube.name() + '.png')
