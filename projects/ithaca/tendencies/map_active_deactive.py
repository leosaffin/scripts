"""
When reducing the precision of some of the physics schemes in speedy, the
tendencies in some gridboxes will be set to zero (deactivated). The reverse can
also occur: gridboxes with zero tendencies at double precision have nonzero
tendencies at lower precision (activated).

To visualise where this is happening this script will mark activated and
deactivated gridpoints, for a give reduced precision, on a map of the
double-precision tendencies
"""
import numpy as np
import matplotlib.pyplot as plt
import iris
from mymodule import plot
from myscripts.models.speedy import datadir


def main():
    # Specify which files and variable to compare
    path = datadir + 'deterministic/'
    scheme = 'Surface Fluxes'
    variable = 'Temperature'
    forecast_period = 2/3
    sigma = 0.95  # 0.95, 0.835, 0.685, 0.51, 0.34, 0.2, 0.095, 0.025
    precision = 10

    # Load the cubes
    string = '{} Tendency due to {}'.format(variable, scheme)
    cs = iris.Constraint(cube_func=lambda x: string in x.name(), sigma=sigma,
                         forecast_period=forecast_period)
    rp = iris.load_cube(path + '../rp_*_tendencies.nc', cs)
    rp = rp.extract(iris.Constraint(precision=precision))
    fp = iris.load_cube(path + 'fp_tendencies.nc', cs)

    make_plot(rp, fp, vmin=-1e-4, vmax=1e-4, cmap='coolwarm')
    plt.show()

    return


def make_plot(rp, fp, **kwargs):
    # Show the full-precision tendencies
    plot.pcolormesh(fp, **kwargs)

    # Find locations of activated and deactivated gridpoints
    activated = np.logical_and(rp.data != 0, fp.data == 0)
    deactivated = np.logical_and(rp.data == 0, fp.data != 0)

    # Overlay activated and deactivated gridpoints
    x = fp.coord('longitude').points
    y = fp.coord('latitude').points
    mark_locations(activated, x, y, 'kX')
    mark_locations(deactivated, x, y, 'ko')

    return


def mark_locations(criteria, x, y, *args):
    iy, ix = np.where(criteria)
    xp = (x[ix] + 180) % 360 - 180
    plt.plot(xp, y[iy], *args)

    return


if __name__ == '__main__':
    main()
