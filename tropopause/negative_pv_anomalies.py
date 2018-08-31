import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mymodule import convert, grid
from myscripts import case_studies
import tropopause


def main(cubes):
    """Find all points within 1km of the tropopause that have a negative PV
    anomaly
    """
    # Find negative pv anomalies
    diff = convert.calc('total_minus_advection_only_pv', cubes)
    negative_pv = diff.data < -1

    # Find the tropopause height
    ztrop, fold_t, fold_b = tropopause.height(cubes)

    # Find point below the tropopause
    z = diff.coord('altitude').points
    tropopause_relative = np.logical_and(z < ztrop, z > ztrop - 2000)

    # Combine criteria
    criteria = np.logical_and(negative_pv, tropopause_relative)

    # Get indices where criterion is met
    indices = np.where(criteria)

    # Convert to lon, lat, z
    longitude = diff.coord('grid_longitude').points
    lons = np.array([longitude[idx] for idx in indices[2]])
    latitude = diff.coord('grid_latitude').points
    lats = np.array([latitude[idx] for idx in indices[1]])
    height = grid.extract_dim_coord(diff, 'z').points
    altitude = np.array([height[idx] for idx in indices[0]])

    # Scatterplot the locations
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(lons, lats, altitude)
    plt.show()


if __name__ == '__main__':
    forecast = case_studies.iop8.copy()
    cubes = forecast.set_lead_time(hours=24)
    main(cubes)
