import iris

from myscripts.models.speedy import datadir
from myscripts.projects.ithaca import plotdir

plotdir += 'speedy_precision/tendencies/'
path = datadir + 'deterministic/tendencies/'


def load_tendency(
        variable='Temperature',
        scheme='All Parametrizations',
        rp_scheme='all_parametrizations',
        sigma=0.95,
        forecast_period=2/3,
        precision=10):

    name = '{} Tendency due to {}'.format(variable, scheme)

    # Account for floating-point error in lead time
    xmin, xmax = forecast_period * 0.999, forecast_period * 1.001
    time_cs = iris.Constraint(forecast_period=lambda x: xmin < x < xmax)

    cs = iris.Constraint(name, sigma=sigma, precision=precision) & time_cs

    rp = iris.load_cube(path + 'rp_{}_tendencies.nc'.format(rp_scheme), cs)

    return rp
