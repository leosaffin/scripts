import iris

from myscripts.models.speedy import datadir
from myscripts.projects.ithaca.tendencies import plotdir

path = datadir + 'stochastic/'
plotdir += 'as_sppt/'


def load_tendency(
        variable='Temperature',
        scheme='all physics processes',
        precision=10,
        forecast_period=2/3,
        sigma=0.95,
        total=True):

    name = '{} Tendency due to {}'.format(variable, scheme)

    # Account for floating-point error in lead time
    xmin, xmax = forecast_period * 0.999, forecast_period * 1.001
    time_cs = iris.Constraint(forecast_period=lambda x: xmin < x < xmax)

    cs = iris.Constraint(name, sigma=sigma) & time_cs

    fp_cs = iris.Constraint(precision=52)
    rp_cs = iris.Constraint(precision=precision)

    fp = iris.load_cube(path + 'rp_physics_tendencies.nc', cs & fp_cs)
    if total:
        rp = iris.load_cube(
            path + 'rp_physics_tendencies.nc', cs & rp_cs)
    else:
        rp = iris.load_cube(
            path + 'rp_{}_tendencies.nc'.format(scheme), cs & rp_cs)

    return rp, fp
