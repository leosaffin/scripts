"""Functions for calculating global statistics

Shorthands for cube.collapsed on a lat/lon grid with various different
aggregators.
"""

from iris.analysis import MEAN, STD_DEV, COUNT
from iris.analysis.cartography import cosine_latitude_weights


def global_mean(cube):
    weights = cosine_latitude_weights(cube)
    mean = cube.collapsed(['longitude', 'latitude'], MEAN, weights=weights)

    return mean


def root_mean_square(cube):
    weights = cosine_latitude_weights(cube)**2
    rms = (cube**2).collapsed(['longitude', 'latitude'],
                              MEAN, weights=weights)**0.5

    return rms


def ensemble_std_dev(cube):
    std = cube.collapsed(['ensemble_member'], STD_DEV)
    std = root_mean_square(std)

    return std


def rms_diff(zfc, zref):
    rms = root_mean_square(zfc - zref)
    rms.rename('RMS error in {}'.format(zfc.name()))

    return rms


def mean_diff(zfc, zref):
    mean = global_mean(zfc - zref)
    mean.rename('Mean error in {}'.format(zfc.name()))

    return mean


def count(zfc, func=lambda x: x != 0):
    nzfc = zfc.collapsed(['longitude', 'latitude'], COUNT, function=func)
    nzfc.rename('Number of {}'.format(zfc.name()))

    return nzfc
