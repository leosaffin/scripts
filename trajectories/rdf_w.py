"""Calculate reverse domain filling trajectories using data in height based
co-ordinates.
"""

import numpy as np
from mymodule import grid, convert, interpolate
from lagranto.caltra import caltra
from myscripts.models.um import case_studies

tracers = ['ertel_potential_vorticity', 'advection_only_pv',
           'air_pressure', 'air_potential_temperature',
           'advection_only_potential_temperature']


def main():
    # Get a mapping from lead times to filenames
    forecast = case_studies.iop5b()
    mapping = forecast._loader._files

    # Create a set of start points for every grid point at 500hpa
    cubes = forecast.set_lead_time(hours=36)
    train = create_startpoints(cubes, 'air_pressure', [50000])

    # Calculate the back trajectories
    traout = caltra.caltra(train, mapping, fbflag=-1, tracers=tracers)

    # Save the output
    # traout.to_pickle('iop5_rdf_500hpa_36h.pkl')

    return traout


def create_startpoints(cubes, coordinate, values):
    """Create an array of startpoints

    Output array has shape Nx3 where N is the number of startpoints and the 3
    indices are for longitude, latitude and altitude.

    Args:
        cubes (iris.cube.CubeList)

    Returns:
        train (np.array): The input array to trajectory calculations
    """
    # Get the values of altitude at the given coordinate
    P = convert.calc(coordinate, cubes)
    z = grid.make_cube(P, 'altitude')
    z.add_aux_coord(grid.make_coord(P), [0, 1, 2])
    z500 = interpolate.to_level(z, **{coordinate: values})[0].data

    lon, lat = grid.get_xy_grids(P)

    # Convert the 2d arrays to an Nx3 array
    train = np.array(
        [lon.flatten(), lat.flatten(), z500.flatten()]).transpose()

    return train

if __name__ == '__main__':
    main()
