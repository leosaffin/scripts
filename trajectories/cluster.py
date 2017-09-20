import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram, fcluster, linkage
from scipy.cluster.vq import kmeans, vq
from iris.analysis.cartography import rotate_pole
from lagranto import trajectory
from mymodule.user_variables import datadir, plotdir

styles = ['-bo', '-gx', '-rx', '-cx', '-mx', '-yx',
          '-bx', '-go', '-ro', '-co', '-mo', '-yo']

def main():
    job = 'iop5_extended'
    name = 'forward_trajectories_from_low_levels_gt600hpa'
    trajectories = trajectory.load(datadir + job + '/' + name + '.pkl')
    trajectories = trajectories.select('air_pressure', '>', 0)
    
    # Perform the clustering
    cluster_array = make_cluster_array(trajectories)
    clusters = perform_clustering(cluster_array)
    plt.savefig(plotdir + job + '_' + name + '_cluster_info.png')
    #np.save(datadir + job + '/' + name + '_clusters.npy', clusters)
    #clusters = np.load(datadir + job + '/' + name + '_clusters.npy')
    
    # Display output
    nclusters = len(set(clusters))
    print('Number of clusters', nclusters)
    plot_clusters(trajectories, clusters)
    plt.savefig(plotdir + job + '_' + name + '_clusters_xy.png')
    plt.show()

    return


def make_cluster_array(trajectories):
    # Normalise the trajectory positions
    x = normalise(trajectories.x)
    y = normalise(trajectories.y)
    z = normalise(trajectories['altitude'])

    # Rearrange array to 2d
    ntraj, ntim = x.shape
    observations = [x, y, z]
    cluster_array = np.zeros([ntraj, ntim * len(observations)])

    for n in range(ntim):
        for m, obs in enumerate(observations):
            cluster_array[:, n + m * ntim] = obs[:, n]
            
    return cluster_array


def perform_clustering(cluster_array, method='average', max_dist=None,
                       nclusters=2):
    if method is 'kmeans':
        clusters = kmeans_cluster(cluster_array, nclusters)
    else:
        clusters = hierarchical(cluster_array, method=method,
                                max_dist=max_dist)

    return clusters


def plot_clusters(trajectories, clusters):
    plt.figure()
    xdata = trajectories.x
    ydata = trajectories.y

    # Plot each trajectory coloured by cluster
    for n, i in enumerate(clusters):
        plt.plot(xdata[n], ydata[n], styles[i % 12], zorder=5)

    # Plot the cluster averages
    for n in set(clusters):
        xm = np.median(xdata[clusters == n], axis=0)
        ym = np.median(ydata[clusters == n], axis=0)
        plt.plot(xm, ym, '-k', zorder=7)

    return


def hierarchical(cluster_array, method='ward', max_dist=None):
    cluster_info = linkage(cluster_array, method)
    
    difference = np.diff(cluster_info[:, 2], 2)
    if max_dist is None:
        max_dist = 1.05*cluster_info[difference.argmax(), 2]

    # Show dendrogram and distance
    plt.figure(figsize=[12, 15])
    plt.subplot2grid([2, 1], [0, 0])
    dendrogram(cluster_info, color_threshold=max_dist)
    plt.axhline(max_dist, color='k', linestyle='--')

    plt.subplot2grid([2, 1], [1, 0])
    plt.plot(cluster_info[1:, 2], '-k')
    ax = plt.twinx()
    ax.plot(difference, '-rx')
    plt.xlim(len(cluster_info) - 22, len(cluster_info) - 2)

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
    main()
