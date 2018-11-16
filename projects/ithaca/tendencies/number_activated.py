"""Plot the number of grid boxes diagnosed to be modified by a physics scheme
as a function of precision.
"""
import numpy as np
import matplotlib.pyplot as plt
import iris
import iris.plot as iplt
from myscripts.statistics import count
from myscripts.models.speedy import datadir


def main():
    # Specify which files and variable to compare
    path = datadir + 'deterministic/'
    scheme = 'Vertical Diffusion'
    string = 'Temperature Tendency due to '
    lead_time = 2 / 3
    pressure = 0.95

    # Load the cubes
    cs = iris.Constraint(cube_func=lambda x: string + scheme in x.name(),
                         forecast_period=lead_time,
                         pressure=pressure)
    rp = iris.load_cube(path + 'rp_*_tendencies.nc', cs)
    fp = iris.load_cube(path + 'fp_tendencies.nc', cs)

    plot_active(rp, fp)
    plt.xlabel('Precision (sbits)')
    plt.ylabel('Number of active gridpoints')
    plt.title(scheme)
    plt.legend()
    plt.show()

    return


def plot_active(rp, fp, **kwargs):
    # Count the number of gridboxes with nonzero tendencies
    n_active, n_activated, n_deactivated, n_zeros = \
        count_active_deactive(rp, fp)
    iplt.plot(n_active, '-k', label='Active', **kwargs)
    iplt.plot(n_activated, '--k', label='Activated', **kwargs)
    iplt.plot(n_deactivated, ':k', label='Deactivated', **kwargs)

    return


def count_active_deactive(rp, fp):
    # Ignore gridboxes where reduced precision has activated or deactivated the
    # physics scheme. Will give e=infinity or e=-1 respectively

    # Create a dummy cube to use the collapsed function
    cube = rp.copy()

    # Number of active gridpoints
    n_active = count(rp)

    # Number of activated gridpoints
    activated = np.logical_and(rp.data != 0, fp.data == 0)
    cube.data = activated
    n_activated = count(cube)

    # Number of deactivated gridpoints
    deactivated = np.logical_and(rp.data == 0, fp.data != 0)
    cube.data = deactivated
    n_deactivated = count(cube)

    # Number of zeros
    n_zeros = count(cube, func=lambda x: x == 0)

    return n_active, n_activated, n_deactivated, n_zeros


if __name__ == '__main__':
    main()
