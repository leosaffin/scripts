from datetime import timedelta
import numpy as np
import matplotlib.pyplot as plt
from irise import plot
from myscripts import datadir, plotdir
from lagranto import trajectory
from systematic_forecasts import second_analysis
from myscripts.trajectories.cluster import select_cluster


def main():
    job = 'iop5_extended'
    name = 'backward_trajectories_from_outflow_coarse'
    variable = 'total_minus_advection_only_pv'
    theta_level = 320
    cluster = 3
    plotname = plotdir + job + '_' + name + '_spread_' + variable

    # Load the trajectories
    trajectories = trajectory.load(datadir + job + '/' + name + '.pkl')
    print(len(trajectories))

    # Only include trajectories that stay in the domain
    trajectories = trajectories.select('air_pressure', '>', 0)
    print(len(trajectories))

    if theta_level is not None:
        dt = timedelta(hours=0)
        trajectories = trajectories.select(
            'air_potential_temperature', '>', theta_level-2.5, time=[dt])
        trajectories = trajectories.select(
            'air_potential_temperature', '<', theta_level+2.5, time=[dt])
        print(len(trajectories))

    # Composite trajectory clusters
    if cluster is not None:
        if theta_level is not None:
            path = datadir + job + '/' + name + '_' + str(theta_level) + 'K'
            plotname += '_' + str(theta_level) + 'K'
        else:
            path = datadir + job + '/' + name
        trajectories = select_cluster(cluster, trajectories, path)
        print(len(trajectories))
        plotname += '_cluster' + str(cluster)

    make_plot(trajectories, variable)
    plt.savefig(plotname + '.png')
    plt.show()

    return


def make_plot(trajectories, variable):
    times = trajectories.times

    # Calculate percentiles of selected variable
    c = second_analysis.all_diagnostics[variable]
    x = trajectories[variable]
    xMed = np.median(x, axis=0)
    xMean = x.mean(axis=0)
    x95 = np.percentile(x, 95, axis=0)
    x75 = np.percentile(x, 75, axis=0)
    x25 = np.percentile(x, 25, axis=0)
    x05 = np.percentile(x, 5, axis=0)

    # Make the plot
    plt.fill_between(times, x05, x95, color='lightgrey')
    plt.fill_between(times, x25, x75, color='grey')
    plt.plot(times, xMean, '-w')
    plt.plot(times, xMed, '-k')
    plt.annotate(str(len(trajectories)) + ' Trajectories', xy=(0.7, 0.01),
                 xycoords='axes fraction')
    plt.title(c.symbol)

    plt.xlabel('Time (hours)')
    plt.ylabel(variable.replace('_', ' '))
    plt.grid(True)

    return


if __name__ == '__main__':
    main()
