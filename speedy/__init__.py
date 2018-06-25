from iris.analysis import MEAN, STD_DEV
from mymodule.user_variables import datadir, plotdir

datadir = datadir + 'speedy/'
plotdir = plotdir + 'speedy/'


def ensemble_std_dev(cube, weights=None):
    std = cube.collapsed(['ensemble_member'], STD_DEV)
    std = std.collapsed(['longitude', 'latitude'],
                        MEAN, weights=weights)

    return std


def rms_diff(z1, z2, weights=None):
    rms = ((z1-z2)**2).collapsed(['longitude', 'latitude'],
                                 MEAN, weights=weights)**0.5

    return rms


def mean_diff(z1, z2, weights=None):
    mean = (z1-z2).collapsed(['longitude', 'latitude'],
                             MEAN, weights=weights)

    return mean
