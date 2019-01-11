"""
Need to consider the switching on and off of physics schemes with reduced
precision. Show the active/deactive points as a function of precision for
selected physics schemes (Vertical Diffusion/Surface Fluxes/Convection)
"""

import numpy as np
import matplotlib.pyplot as plt
import iris
import iris.plot as iplt
from myscripts.statistics import count
from myscripts.models.speedy import datadir


def main():
    # Load cubes
    path = datadir + 'deterministic/'
    cs = iris.Constraint(
        cube_func=lambda x: 'Temperature Tendency' in x.name(),
        forecast_period=2/3, sigma=0.95)
    rp_cubes = iris.load(path + 'rp_*_tendencies.nc', cs)
    fp_cubes = iris.load(path + 'fp_tendencies.nc', cs)

    # Create a two by two grid with shared x and y axes along rows and columns
    fig, axes = plt.subplots(nrows=2, ncols=2, sharex=True,
                             figsize=[12.0, 7.2])

    plt.axes(axes[0, 0])

    plt.axes(axes[0, 1])
    scheme = 'Vertical Diffusion'
    make_plot(rp_cubes, fp_cubes, scheme)
    plt.legend(title='Number of gridpoints')

    plt.axes(axes[1, 0])
    scheme = 'Surface Fluxes'
    make_plot(rp_cubes, fp_cubes, scheme)

    plt.axes(axes[1, 1])
    scheme = 'Convection'
    make_plot(rp_cubes, fp_cubes, scheme)

    plt.show()

    return


def make_plot(rp_cubes, fp_cubes, scheme):
    plt.title(scheme)
    name = 'Temperature Tendency due to {} [K/s]'.format(scheme)
    rp = rp_cubes.extract_strict(iris.Constraint(name))
    fp = fp_cubes.extract_strict(iris.Constraint(name))
    plot_active(rp, fp)

    return


def plot_active(rp, fp, **kwargs):
    # Count the number of gridboxes with nonzero tendencies
    n_active, n_activated, n_deactivated, n_zeros = \
        count_active_deactive(rp, fp)

    for linestyle, label, data in [('-k', 'Active', n_active),
                                   ('--k', 'Activated', n_activated),
                                   (':k', 'Deactivated', n_deactivated)]:
        iplt.plot(data, linestyle, label=label, **kwargs)

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
