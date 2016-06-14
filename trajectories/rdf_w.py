"""Calculate reverse domain filling trajectories using data in height based
co-ordinates.
"""

from datetime import timedelta as dt
import numpy as np
from mymodule import grid, convert, interpolate
from lagranto.caltra import caltra
from scripts import case_studies


def main():
    # Get a mapping from lead times to filenames
    forecast = case_studies.iop5b()
    mapping = forecast._loader._files

    # Create a set of start points for every grid point at 500hpa
    cubes = forecast.set_lead_time(hours=36)
    P = convert.calc('air_pressure', cubes)
    z = grid.make_cube(P, 'altitude')
    z.add_aux_coord(grid.make_coord(P), [0, 1, 2])
    z500 = interpolate.to_level(z, air_pressure=[50000])[0].data
    lon, lat = grid.get_xy_grids(P)
    train = np.array(
        [lon.flatten(), lat.flatten(), z500.flatten()]).transpose()

    # Calculate the back trajectories
    traout = caltra.caltra(
        train, mapping, fbflag= -1,
        tracers=['ertel_potential_vorticity', 'advection_only_pv',
                 'air_pressure', 'air_potential_temperature'])

    np.save('/home/lsaffi/data/rdf_pv', traout)

if __name__ == '__main__':
    main()
