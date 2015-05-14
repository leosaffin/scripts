import numpy as np
import matplotlib.pyplot as plt
import cPickle as pickle
from mymodule import files, convert, grid, interpolate, plot

# Load RDF PV
with open('/home/lsaffi/data/rdf_pv.pkl', 'rb') as infile:
    rdf_pv = pickle.load(infile)

# Load final time PV tracers
cubes = files.load('/projects/diamet/lsaffi/xjjhq/*010.pp')
adv = convert.calc('advection_only_pv', cubes)
tot = convert.calc('total_pv', cubes)
p = cubes.extract('air_pressure')[1]

# Add pressure as a coordinate
pcoord = grid.make_coord(p)
adv.add_aux_coord(pcoord, [0, 1, 2])
tot.add_aux_coord(pcoord, [0, 1, 2])

# Interpolate to pressure levels
adv = interpolate.main(adv, air_pressure=500)
tot = interpolate.main(tot, air_pressure=500)

rdf_pv = rdf_pv.T[15:345, 15:585]
rdf_pv = cubes[0][0].copy(data=rdf_pv)

cscale = np.linspace(0, 5, 21)
for cube in [adv, tot, rdf_pv]:
    plt.figure()
    plot.level(cube, cube)
    plt.savefig('/home/lsaffi/plots/' + cube.name() + '.png')
