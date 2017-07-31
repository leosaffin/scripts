from datetime import timedelta
import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram, fcluster, linkage
from scipy.cluster.vq import kmeans, vq
from lagranto import trajectory
from scripts import case_studies

path = '/home/lsaffin/Documents/meteorology/data/iop5/'
name = 'backward_trajectories_from_320K'
forecast = case_studies.iop5b.copy()
cubes = forecast.set_lead_time(hours=24)


def main(trajectories):
    # Normalise the trajectory positions
    x = normalise(trajectories['grid_longitude'])
    y = normalise(trajectories['grid_latitude'])
    z = normalise(trajectories['altitude'])

    # Rearrange array to 2d
    ntraj, ntim = x.shape
    observations = [x, y, z]
    cluster_array = np.zeros([ntraj, ntim * len(observations)])

    for n in range(ntim):
        for m, obs in enumerate(observations):
            cluster_array[:, n + m * ntim] = obs[:, n]

    # Perform clustering
    clusters = hierarchical(cluster_array, max_dist=7)
    #clusters = kmeans_cluster(cluster_array, 4)

    nclusters = (len(set(clusters)))
    print('Number of clusters', nclusters)

    plt.figure()
    styles = ['bx', 'gx', 'rx', 'cx', 'mx']
    xdata = trajectories['grid_longitude']
    ydata = trajectories['grid_latitude']
    # Plot each cluster
    for n, i in enumerate(clusters):
        plt.plot(xdata[n], ydata[n], '-k')
        for j in [0, -1]:
            plt.plot(xdata[n, j], ydata[n, j], styles[i % 5], zorder=5)

    # Plot the cluster averages
    for n in set(clusters):
        plt.plot(xdata[clusters == n].mean(axis=0),
                 ydata[clusters == n].mean(axis=0),
                 '-' + styles[n % 5], markersize=5, linewidth=2, zorder=6)
    plt.show()

    return


def hierarchical(cluster_array, max_dist=None):
    cluster_info = linkage(cluster_array, 'ward')

    # Show dendrogram and distance
    dendrogram(cluster_info)

    plt.figure()
    plt.plot(cluster_info[1:, 2], '-k')

    ax = plt.twinx()
    difference = np.diff(cluster_info[:, 2], 2)
    ax.plot(difference, '-r')

    plt.xlim(len(cluster_info) - 22, len(cluster_info) - 2)

    if max_dist is None:
        max_dist = cluster_info[difference.argmax(), 2]

    # Select the clusters at a specified cut off
    clusters = fcluster(cluster_info, max_dist, criterion='distance')

    return clusters


def kmeans_cluster(cluster_array, nclusters):
    code_book, distortion = kmeans(cluster_array, nclusters)
    clusters, dist = vq(cluster_array, code_book)

    return clusters


def normalise(x):
    # Calculate the rms change along the trajectory
    delta_x_rms = np.mean((x[:, 0] - x[:, -1])**2)**0.5

    # Normalise the difference
    x_norm = x / delta_x_rms

    return x_norm


if __name__ == '__main__':
    filename = path + name + '.pkl'
    trajectories = trajectory.load(filename)
    dt1 = timedelta(hours=0)
    trajectories = trajectories.select('altitude', '>', 0)
    trajectories = trajectories.select('grid_latitude', '>', 0, time=[dt1])
    trajectories = trajectories.select('grid_longitude', '>', 360, time=[dt1])
    trajectories = trajectories.select('grid_longitude', '<', 380, time=[dt1])
    trajectories = trajectories.select('grid_latitude', '<', 10, time=[dt1])
    main(trajectories)
