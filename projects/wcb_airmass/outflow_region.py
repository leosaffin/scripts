"""Plot demonstrating the outflow region of the warm conveyor belt

$\theta-\theta_{adv}$ shows regions of cross-isentropic ascent
Contour of 2-PVU shows tropopause, highlighting ridge area
Trajectory start and end points show warm conveyor belt transport into outflow
"""
from math import cos
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy.ndimage import filters
import iris.plot as iplt
from mymodule import convert, grid, plot
from mymodule.constants import r
from mymodule.detection.rossby_waves import tropopause_contour
from scripts import case_studies

r = r.data


def main():
    lead_time = 48
    levels = ('air_potential_temperature', [320])

    forecast = case_studies.iop5_extended.copy()
    cubes = forecast.set_lead_time(hours=lead_time)
    dtheta = convert.calc('total_minus_advection_only_theta', cubes,
                          levels=levels)[0]
    pv = convert.calc('ertel_potential_vorticity', cubes, levels=levels)[0]

    closed_loop, points = get_points(dtheta.copy(), pv.copy())
    closed_loop = increase_circuit_resolution(closed_loop, 25000)

    make_plot(dtheta, pv, closed_loop, vmin=-20, vmax=20, cmap='coolwarm')

    return


def get_points(dtheta, pv):
    # Smooth the theta_adv and pv data first
    dtheta.data = filters.gaussian_filter(dtheta.data, sigma=10, truncate=4)
    pv.data = filters.median_filter(pv.data, size=20)

    # Extract the contour surrounding the outflow region
    criteria = np.logical_and(pv.data < 2, dtheta.data > 0)
    pv.data = criteria.astype(int)
    cs = iplt.contour(pv, [0.5])
    contours = tropopause_contour.get_contour_verts(cs)
    closed_loop = tropopause_contour.get_tropopause_contour(contours[0])
    path = mpl.path.Path(closed_loop)

    # Create an array containing all the grid points within the outflow region
    lon, lat = grid.get_xy_grids(dtheta)
    points = np.transpose(np.array([lon.flatten(), lat.flatten()]))
    points = points[np.where(path.contains_points(points))]

    return closed_loop, points


def increase_circuit_resolution(points, resolution):
    """Add points around the circuit loop
    """
    # Loop over all points around the circuit.
    n = 0
    while n < len(points) - 1:
        # Calculate distances from current point to next point
        lat = (points[n, 1] + points[n + 1, 0]) / 2
        dlon = points[n + 1, 0] - points[n, 0]
        dlat = points[n + 1, 1] - points[n, 1]
        dx = r * cos(np.deg2rad(lat)) * np.deg2rad(dlon)
        dy = r * np.deg2rad(dlat)
        distance = (dx ** 2 + dy ** 2) ** 0.5
        # Insert a point if the next point is further away than the required
        # resolution
        if distance > resolution:
            # Put the next point along the same line
            frac = resolution / distance
            new_lon = points[n, 0] + frac * dlon
            new_lat = points[n, 1] + frac * dlat
            points = np.insert(points, n + 1, [new_lon, new_lat], 0)

        # Always jump to the next point. This will either be the inserted point
        # or the next point along that is within the required resolution
        n += 1

    return points


def make_plot(theta_adv, pv, points, **kwargs):
    plot.pcolormesh(theta_adv, **kwargs)
    iplt.contour(pv, [2], colors='k', linewidths=2)
    plt.scatter(points[:, 0], points[:, 1])

    return


if __name__ == '__main__':
    main()
