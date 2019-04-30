from datetime import timedelta
import matplotlib.pyplot as plt
import iris.plot as iplt
from lagranto import trajectory
from irise import convert, plot
from myscripts import datadir, plotdir
from myscripts.models.um import case_studies
from myscripts.trajectories.cluster import select_cluster


def main():
    job = 'iop5_extended'
    name = 'forward_trajectories_from_low_levels_gt600hpa'
    forecast = case_studies.iop5_extended.copy()
    cubes = forecast.set_lead_time(hours=48)

    theta_level = None
    cluster = None
    levels = ('air_potential_temperature', [315])

    make_plot(cubes, job, name, levels, theta_level, cluster,
              vmin=0, vmax=12000, cmap='summer')

    return


def make_plot(cubes, job, name, levels, theta_level, cluster, **kwargs):
    plt.figure(figsize=(12, 10))
    plotname = plotdir + job + '_' + name + '_map'

    # Plot a map at verification time
    pv = convert.calc('ertel_potential_vorticity', cubes, levels=levels)[0]
    dtheta = convert.calc('total_minus_advection_only_theta', cubes,
                          levels=levels)[0]
    mslp = convert.calc('air_pressure_at_sea_level', cubes)
    mslp.convert_units('hPa')

    plot.pcolormesh(dtheta, vmin=-20, vmax=20, cmap='coolwarm', pv=pv)
    cs = iplt.contour(mslp, range(950, 1050, 5), colors='k', linewidths=1)
    plt.clabel(cs, fmt='%1.0f')

    # Load the trajectories
    filename = datadir + job + '/' + name + '.pkl'
    trajectories = trajectory.load(filename)
    print(len(trajectories))

    # Only plot trajectories that stay in the domain
    trajectories = trajectories.select('air_pressure', '>', 0)
    print(len(trajectories))

    # Select individual clusters of trajectories
    if cluster is not None:
        path = datadir + job + '/' + name
        select_cluster(cluster, trajectories, path)
        plotname += '_cluster' + str(cluster)

    if theta_level is not None:
        plotname += '_' + str(theta_level) + 'K'
        dt = timedelta(hours=48)
        trajectories = trajectories.select(
            'air_potential_temperature', '>', theta_level-2.5, time=[dt])
        trajectories = trajectories.select(
            'air_potential_temperature', '<=', theta_level+2.5, time=[dt])
        print(len(trajectories))

    x = trajectories.x - 360
    y = trajectories.y
    c = trajectories['altitude']

    # Plot each individual trajectory
    for n in range(len(trajectories)):
        plot.colored_line_plot(x[n], y[n], c[n], **kwargs)

    # Mark the start and end point of trajectories
    plt.scatter(x[:, 0], y[:, 0], c=c[:, 0],
                linewidths=0.1, zorder=5, **kwargs)
    plt.scatter(x[:, -1], y[:, -1], c=c[:, -1],
                linewidths=0.1, zorder=5, **kwargs)
    plt.colorbar()

    plt.savefig(plotname + '.png')

    return


if __name__ == '__main__':
    main()
