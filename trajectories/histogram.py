import numpy as np
import matplotlib.pyplot as plt
from mymodule.user_variables import datadir, plotdir
from lagranto import trajectory
from scripts.trajectories.cluster import select_cluster


def main():
    job = 'iop5_extended'
    name = 'backward_trajectories_from_outflow'
    variable = 'air_potential_temperature'
    cluster = None
    plotname = plotdir + job + '_' + name + '_histogram_' + variable

    # Load the trajectories
    trajectories = trajectory.load(datadir + job + '/' + name + '.pkl')
    print(len(trajectories))

    # Only include trajectories that stay in the domain
    trajectories = trajectories.select('air_pressure', '>', 0)
    print(len(trajectories))

    # Composite trajectory clusters
    if cluster is not None:
        path = datadir + job + '/' + name
        trajectories = select_cluster(cluster, trajectories, path)
        plotname += '_cluster' + str(cluster)
        print len(trajectories)

    make_plot(trajectories, variable)
    plt.savefig(plotname + '.png')
    plt.show()

    return


def make_plot(trajectories, variable):
    # Calculate percentiles of selected variable
    x = trajectories[variable]
    dx = (x[:, 0])
    xMed = np.median(dx)
    xMean = dx.mean()
    
    hist, bin_edges = np.histogram(dx)

    # Make the plot
    width = bin_edges[1] - bin_edges[0]
    plt.bar(bin_edges[:-1], hist, width=width, color='k', edgecolor='grey')
    plt.axvline(xMean, color='w')
    plt.axvline(xMed, color='k')


    plt.ylabel('Number of trajectories')
    plt.xlabel(variable.replace('_', ' '))

    return


if __name__ == '__main__':
    main()
