"""Convert ensemble outputs to probability density functions
"""

import numpy as np
from sklearn.neighbors import KernelDensity
import iris
from myscripts.models.speedy import datadir


def main():
    path = datadir + 'stochastic/ensembles/'
    filename = 'hp_exponent.nc'
    cs = iris.Constraint('geopotential_height', pressure=500)
    ensemble = iris.load_cube(path + filename, cs)[:, 1:]

    bins = np.arange(4000, 6500)
    pdf = pdf_aggregator_function(bins, ensemble.data, 0)
    pdf_cube = repackage_as_cube(pdf, bins, ensemble, 'ensemble_member')
    iris.save(pdf_cube, path + filename.replace('.nc', '_pdf.nc'))

    return


def repackage_as_cube(pdf, bins, old_cube, collapsed_coordinate):
    # Create a cubelist to merge all data together
    pdf_collection = iris.cube.CubeList()

    # axis = old_cube.coord_dims(collapsed_coordinate)
    pdf_cube = old_cube[0].copy()
    pdf_cube.remove_coord(collapsed_coordinate)
    pdf_cube.rename('Probability Density of {}'.format(old_cube.name()))
    pdf_cube.units = ''

    for n, point in enumerate(bins):
        coord = iris.coords.AuxCoord(point, long_name=old_cube.name(),
                                     units=old_cube.units)
        newcube = pdf_cube.copy(data=pdf[n])
        newcube.add_aux_coord(coord)
        pdf_collection.append(newcube)

    return pdf_collection.merge_cube()


def pdf_aggregator_function(bins, data, axis, kernel='gaussian'):
    # Use the standard deviation to determine the bandwidth of the kernels
    bandwidths = np.std(data, axis) / 2

    # Create output array with collapsing dimensions removed and a bins
    # dimension added at the front
    output_shape = [len(bins)] + list(bandwidths.shape)
    density = np.zeros(output_shape)

    idx = 0
    for index, bw in np.ndenumerate(bandwidths):
        if index[0] == idx:
            print(idx)
            idx += 1

        # Get the full set of data at the index
        selector = list(index)
        selector.insert(axis, ...)
        data_1d = data[tuple(selector)].flatten()

        # Evaluate the probability density at each point
        density[tuple([...] + list(index))] =\
            gridpoint_pdf(bins, data_1d, bw, kernel=kernel)

    return density


def gridpoint_pdf(points, values, bandwidth, kernel='gaussian'):
    """Convert a set of individual values to a probability density

    Args:
        points (np.ndarray): Points to evaluate the probability density at
        values: Values to convert to probability density
        bandwidth: The width of the probability density kernel to apply to each
            value
        kernel: Kernel used to weight each individual value

    Returns:
        np.ndarray: The probability density evaluated at the input points
    """
    kde = KernelDensity(
        kernel=kernel, bandwidth=bandwidth).fit(values[:, np.newaxis])

    return np.exp(kde.score_samples(points[:, np.newaxis]))


if __name__ == '__main__':
    main()
