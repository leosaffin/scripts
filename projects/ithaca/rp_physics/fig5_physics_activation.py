"""
Need to consider the switching on and off of physics schemes with reduced
precision. Show the active/deactive points as a function of precision for
selected physics schemes (Vertical Diffusion/Surface Fluxes/Convection)
"""

import numpy as np
import matplotlib.pyplot as plt
import iris.plot as iplt

from myscripts.statistics import count
from myscripts.models import speedy
from myscripts.projects.ithaca.tendencies import load_tendency


def main():
    variable = 'Temperature'
    sigma = speedy.sigma_levels[0]
    precisions = range(5, 24)

    # Create a two by two grid with shared x and y axes along rows and columns
    fig, axes = plt.subplots(nrows=2, ncols=2, sharex=True,
                             figsize=[12.0, 7.2])

    plt.axes(axes[0, 0])
    scheme = 'Condensation'
    make_plot(variable, scheme, sigma, precisions)

    plt.axes(axes[0, 1])
    scheme = 'Vertical Diffusion'
    make_plot(variable, scheme, sigma, precisions)
    plt.legend(title='Number of gridpoints')

    plt.axes(axes[1, 0])
    scheme = 'Surface Fluxes'
    make_plot(variable, scheme, sigma, precisions)

    plt.axes(axes[1, 1])
    scheme = 'Convection'
    make_plot(variable, scheme, sigma, precisions)

    plt.show()

    return


def make_plot(variable, scheme, sigma, precisions):
    rp = load_tendency(
        variable=variable, scheme=scheme,
        rp_scheme=scheme.replace(' ', '_').replace('-', '_').lower(),
        sigma=sigma, precision=precisions)

    fp = load_tendency(
        variable=variable, scheme=scheme,
        rp_scheme='all_parametrizations',
        sigma=sigma, precision=52)
    plt.title(scheme)
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
