"""
Show the errors in physics tendencies as a function of precision. Show both
relative and absolute errors (haven't decided on mean_diff or rms_diff). For
relative errors, this can be directly compared to the machine epsilon so add
this line also. Also print out errors as a function of machine epsilon to be
shown in a table.
"""

import numpy as np
import matplotlib.pyplot as plt
import iris
from iris.analysis import maths
from mymodule.plot.util import legend, multilabel
from myscripts.statistics import global_mean
from myscripts.models.speedy import datadir, physics_schemes


def main():
    # Load cubes
    path = datadir + 'deterministic/'
    variable, units = 'Temperature', 'K/s'
    forecast_period = 2/3
    sigma = 0.95

    schemes = ['Convection', 'Condensation', 'Short-Wave Radiation',
               'Long-Wave Radiation', 'Surface Fluxes', 'Vertical Diffusion']
    filenames = {'Physics': 'physics',
                 'Convection': 'convection',
                 'Condensation': 'condensation',
                 'Cloud': 'cloud',
                 'Short-Wave Radiation': 'sw_radiation',
                 'Long-Wave Radiation': 'lw_radiation',
                 'Surface Fluxes': 'surface_fluxes',
                 'Vertical Diffusion': 'vertical_diffusion'}

    # Create a two by two grid
    fig, axes = plt.subplots(nrows=2, ncols=2, sharex='all', sharey='row')

    plt.axes(axes[0, 0])
    plt.yscale('log')

    plt.axes(axes[1, 0])
    plt.yscale('log')

    # Show the reference machine epsilon
    sbits = np.arange(5, 24)
    error = 2.0 ** -(sbits + 1)
    for n in range(2):
        plt.axes(axes[1, n])
        plt.plot(sbits, error, '--k')

    # Errors with respect to individual scheme
    cs = iris.Constraint(forecast_period=forecast_period, sigma=sigma)
    fp_cubes = iris.load(path + 'fp_tendencies.nc', cs)
    rp_cubes = iris.load(path + 'rp_*_tendencies.nc', cs)

    # Loop over physics schemes
    for scheme in schemes:
        plp = physics_schemes[scheme]

        if scheme == 'Condensation':
            name = '{} Tendency due to Large-Scale Condensation [{}]'.format(variable, units)
        else:
            name = '{} Tendency due to {} [{}]'.format(variable, scheme, units)

        fp = fp_cubes.extract_strict(iris.Constraint(name))
        rp = rp_cubes.extract_strict(iris.Constraint(name))

        rel_error = display_errors(rp, fp, axes, 0, plp)

        # Print errors
        print(scheme, (rel_error/error).data.mean())

    # Errors with respect to total physics tendency
    schemes += ['Physics', 'Cloud']
    path = datadir + 'stochastic/'

    name = '{} Tendency due to all physics processes'.format(variable)
    cs = iris.Constraint(name, lev=sigma, precision=52)
    fp = iris.load_cube(path + 'rp_physics_tendencies.nc', cs)[1]

    cs = iris.Constraint(name, lev=sigma, precision=lambda x: x < 24)
    for scheme in filenames:
        rp = iris.load_cube(path + 'rp_' + filenames[scheme] + '_tendencies.nc', cs)[:, 1]
        plp = physics_schemes[scheme]
        rel_error = display_errors(rp, fp, axes, 1, plp, label=scheme)
        print(scheme, (rel_error / error).data.mean())

    # Add dressing to the plot
    plt.axes(axes[1, 1])
    legend(key=lambda x: physics_schemes[x[0]].idx, ncol=2,
           title='Physics Schemes')
    multilabel(axes[0, 0], 0, factor=0.01)
    multilabel(axes[0, 1], 1, factor=0.01)
    multilabel(axes[1, 0], 2, factor=0.01)
    multilabel(axes[1, 1], 3, factor=0.01)
    plt.show()

    return


def display_errors(rp, fp, axes, n, plp, **kwargs):
    # Ignore where tendencies are zero
    rp.data = np.ma.masked_where(
        np.logical_or(rp.data == 0, fp.data == 0), rp.data)

    # Calculate absolute error
    plt.axes(axes[0, n])
    abs_error = maths.abs(rp - fp)
    abs_error = global_mean(abs_error)
    plp.plot(abs_error, **kwargs)

    # Calculate relative error
    plt.axes(axes[1, n])
    rel_error = maths.abs((rp - fp) / fp)
    rel_error = global_mean(rel_error)
    plp.plot(rel_error, **kwargs)

    return rel_error


if __name__ == '__main__':
    main()