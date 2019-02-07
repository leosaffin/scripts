import numpy as np
from irise import convert, grid


def create_startpoints(cubes, levels, stride=1):
    """Create an array of startpoints

    Output array has shape Nx3 where N is the number of startpoints and the 3
    indices are for longitude, latitude and altitude.

    Args:
        cubes (iris.cube.CubeList)

    Returns:
        train (np.array): The input array to trajectory calculations
    """
    # Get the values of altitude at the given coordinate
    z = convert.calc('altitude', cubes, levels=levels)

    # Get the grid latitude and longitude as 2d arrays
    lon, lat = grid.get_xy_grids(z)

    # Convert the 2d arrays to an Nx3 array
    nz = z.shape[0]
    lon = np.tile(lon[::stride, ::stride].flatten(), nz)
    lat = np.tile(lat[::stride, ::stride].flatten(), nz)
    z = z.data[:, ::stride, ::stride].flatten()

    train = np.array([lon, lat, z]).transpose()

    return train
