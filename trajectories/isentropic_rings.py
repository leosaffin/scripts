"""Overlay the isentropic circuit on a field at each timestep of the forecast
and show the points of the 3d trajectories calculated from the same region
"""

from datetime import timedelta
import matplotlib.pyplot as plt
import numpy as np
import iris.plot as iplt
from cartopy import crs
from lagranto import trajectory
from mymodule import convert, plot
from mymodule.user_variables import datadir, plotdir
from scripts import case_studies
from scripts.trajectories.cluster import select_cluster

def main():
    path = '/projects/diamet/lsaffi/'
    job = 'iop5_extended'
    forecast = case_studies.iop5_extended.copy()
    theta_level = 320
    cluster = 3
    dt1 = timedelta(hours=0)
    dt2 = timedelta(hours=-48)
    
    # Load the bounding isentropic trajectories
    name = 'isentropic_backward_trajectories_from_outflow_boundary'
    rings = trajectory.load(path + job + '/' + name + '.pkl')
    rings = rings.select('air_potential_temperature', '==', theta_level)
    print len(rings)
    
    # Load the 3d trajectories
    name = 'backward_trajectories_from_outflow_coarse'
    trajectories = trajectory.load(datadir + job + '/' + name + '.pkl')
    print(len(trajectories))

    # Only include trajectories that stay in the domain
    trajectories = trajectories.select('air_pressure', '>', 0)
    print(len(trajectories))

    trajectories = trajectories.select(
        'air_potential_temperature', '==', theta_level-2.5, time=[dt1])
    print len(trajectories)

    # Composite trajectory clusters
    if cluster is not None:
        if theta_level is not None:
            path = datadir + job + '/' + name + '_' + str(theta_level) + 'K'
        else:
            path = datadir + job + '/' + name
        trajectories = select_cluster(cluster, trajectories, path)
    print len(trajectories)

    plt.figure()
    for n, cubes in enumerate(forecast):
        print n
        plt.clf()
        make_plot(cubes, rings, trajectories, theta_level, n+2)

        plt.savefig(plotdir + 'isentropic_rings_' + str(theta_level) + 'K_' +
                    str(n).zfill(3) + '.png')
    return

def make_plot(cubes, rings, wcb, theta_level, n):
    # Plot a map at verification time
    levels = ('air_potential_temperature', [theta_level])
    pv = convert.calc('ertel_potential_vorticity', cubes, levels=levels)[0]
    plot.pcolormesh(pv, vmin=-2, vmax=2, cmap='coolwarm')
    iplt.contour(pv, [0, 2], colors='k', linewidths=2)
    plot._add_map()

    # Load the trajectories
    x = wcb['grid_longitude'] - 360
    y = wcb['grid_latitude']
    c = wcb['air_potential_temperature']
    
    # Plot the 3d trajectory positions
    plt.scatter(x[:, -n], y[:, -n], c=c[:, -n],
                vmin=300, vmax=340, cmap='coolwarm')

    # Plot the isentropic boundary
    x = rings['grid_longitude'] - 360
    y = rings['grid_latitude']
    plt.plot(x[:, -n], y[:, -n], color='r', linewidth=3)

    return


if __name__ == '__main__':
    main()
