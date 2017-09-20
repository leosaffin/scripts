import numpy as np
import matplotlib.pyplot as plt
from mymodule import plot
from mymodule.user_variables import datadir
from lagranto import trajectory
from systematic_forecasts import second_analysis


def main(filename):
    job = 'iop5_extended'
    name = 'forward_trajectories_from_low_levels_gt600hpa'
    variable = 'air_potential_temperature'
    cluster = 3
    plotname = datadir + job + '_' + name + '_spread_' +  variable

    # Load the trajectories
    trajectories = trajectory.load(datadir + job + '/' + name + '.pkl')
    print(len(trajectories))

    # Only include trajectories that stay in the domain
    trajectories = trajectories.select('air_pressure', '>', 0)
    print(len(trajectories))
    
    # Composite trajectory clusters
    if cluster is not None:
        plotname += '_cluster' + str(cluster)
        clusters = np.load(path + job + '/' +  name + '_clusters.npy')
        indices = np.where(clusters==cluster)
        trajectories = trajectory.TrajectoryEnsemble(
            trajectories.data[indices], trajectories.times, trajectories.names)
    
    plot(trajectories, variable, cluster=cluster)
    plt.savefig(plotname + '.png')
    plt.show()
    
    return


def plot(trajectories, variable):
    times = trajectories.times

    # Calculate percentiles of selected variable
    c=second_analysis.all_diagnostics[variable]
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

