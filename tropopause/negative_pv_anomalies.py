import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mymodule import convert, grid, interpolate
from scripts import case_studies


def main(cubes):
    """Find all points within 1km of the tropopause that have a negative PV
    anomaly
    """
    # Find the tropopause height
    pv = convert.calc('ertel_potential_vorticity', cubes)
    grid.add_hybrid_height(pv)
    z = grid.make_cube(pv, 'altitude').data
    zpv2 = get_tropopause_height(pv).data * np.ones_like(z)

    # Find point below the tropopause
    tropopause_relative = np.logical_and(z < zpv2, z > zpv2 - 2000)

    # Find negative pv anomalies
    diff = convert.calc('total_minus_advection_only_pv', cubes)
    negative_pv = diff.data < -1

    # Combine criteria
    criteria = np.logical_and(negative_pv, tropopause_relative)

    # Get indices where criterion is met
    indices = np.where(criteria)

    # Convert to lon, lat, z
    longitude = pv.coord('grid_longitude').points
    lons = np.array([longitude[idx] for idx in indices[2]])
    latitude = pv.coord('grid_latitude').points
    lats = np.array([latitude[idx] for idx in indices[1]])
    height = pv.coord('level_height').points
    altitude = np.array([height[idx] for idx in indices[0]])

    # Scatterplot the locations
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(lons, lats, altitude)
    plt.show()


def get_tropopause_height(pv):
    """Find the altitude where pv=2 is crossed

    Args:
        pv (iris.cube.Cube):

    Returns:
        zpv2 (iris.cube.Cube): 2-dimensional cube with the altitude of the
            highest 2 PVU surface
    """
    z = grid.make_cube(pv, 'altitude')
    pv = grid.make_coord(pv)
    z.add_aux_coord(pv, [0, 1, 2])

    zpv2 = interpolate.to_level(z, ertel_potential_vorticity=[2])[0]

    return zpv2


if __name__ == '__main__':
    forecast = case_studies.iop5b
    cubes = forecast.set_lead_time(hours=24)
    main(cubes)
