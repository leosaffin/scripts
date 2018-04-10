"""Plot demonstrating the outflow region of the warm conveyor belt

$\theta-\theta_{adv}$ shows regions of cross-isentropic ascent
Contour of 2-PVU shows tropopause, highlighting ridge area
Trajectory start and end points show warm conveyor belt transport into outflow
"""
import numpy as np
import matplotlib as mpl
from scipy.ndimage import filters
import iris.plot as iplt
from mymodule import convert, grid, plot
from mymodule.detection.rossby_waves import tropopause_contour
from scripts import case_studies


def main():
    lead_time = 48
    levels = ('air_potential_temperature', [320])

    forecast = case_studies.iop5_extended()
    cubes = forecast.set_lead_time(hours=lead_time)
    theta_adv = convert.calc('advection_only_theta', cubes, levels=levels)[0]

    closed_loop, points = get_points(theta_adv)

    print(closed_loop)
    print(points)

    return


def get_points(theta_adv):
    # Smooth the theta_adv data first
    theta_adv.data = filters.median_filter(theta_adv.data, size=25)

    # Extract the contour surrounding the outflow region
    cs = iplt.contour(theta_adv, [0])
    contours = tropopause_contour.get_contour_verts(cs)
    closed_loop = tropopause_contour.get_tropopause_contour(contours)
    path = mpl.Path(closed_loop)

    # Create an array containing all the grid points within the outflow region
    lon, lat = grid.get_xy_grids(theta_adv)
    points = np.transpose(np.array([lon.flatten(), lat.flatten()]))
    points = np.extract(path.contains_points(points), points)

    return closed_loop, points


def make_plot(theta_adv, pv, wcb_trajectories, **kwargs):

    plot.pcolormesh(theta_adv, **kwargs)
    iplt.contour(pv, [2], colors='k', linewidths=2)
    wcb_trajectories.scatter('kx', time=(0, 'h'))
    wcb_trajectories.scatter('kx', time=(48, 'h'))

    return


if __name__ == '__main__':
    main()
