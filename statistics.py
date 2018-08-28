"""Functions for calculating global statistics

Shorthands for cube.collapsed on a lat/lon grid with various different
aggregators.
"""

from iris.analysis import MEAN, STD_DEV, COUNT
from iris.analysis.cartography import cosine_latitude_weights


def ensemble_std_dev(cube):
    std = cube.collapsed(['ensemble_member'], STD_DEV)
    weights = cosine_latitude_weights(std)
    std = std.collapsed(['longitude', 'latitude'],
                        MEAN, weights=weights)

    return std


def rms_diff(zfc, zref):
    weights = cosine_latitude_weights(zfc)
    rms = ((zfc-zref)**2).collapsed(['longitude', 'latitude'],
                                    MEAN, weights=weights)**0.5
    rms.rename('RMS error in {}'.format(zfc.name()))

    return rms


def mean_diff(zfc, zref):
    weights = cosine_latitude_weights(zfc)
    mean = (zfc-zref).collapsed(['longitude', 'latitude'],
                                MEAN, weights=weights)
    mean.rename('Mean error in {}'.format(zfc.name()))

    return mean


def count(zfc, func=lambda x: x != 0):
    nzfc = zfc.collapsed(['longitude', 'latitude'], COUNT, function=func)
    nzfc.rename('Number of {}'.format(zfc.name()))

    return nzfc
