"""
Show the errors in physics tendencies as a function of precision. Show both
relative and absolute errors (haven't decided on mean_diff or rms_diff). For
relative errors, this can be directly compared to the machine epsilon so add
this line also. Also print out errors as a function of machine epsilon to be
shown in a table.
"""

import numpy as np
import matplotlib.pyplot as plt
from iris.analysis import maths
from irise.plot.util import legend, multilabel

from myscripts.statistics import global_mean
from myscripts.models.speedy import physics_schemes
from myscripts.projects.ithaca.tendencies import load_tendency


def main():
    # Load cubes
    variable = 'Temperature'
    forecast_period = 2/3
    sigma = 0.95

    filenames = {'All Parametrizations': 'all_parametrizations',
                 'Convection': 'convection',
                 'Condensation': 'condensation',
                 #'Cloud': 'cloud',
                 'Short-Wave Radiation': 'short_wave_radiation',
                 'Long-Wave Radiation': 'long_wave_radiation',
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
    machine_error = 2.0 ** -(sbits + 1)
    for n in range(2):
        plt.axes(axes[1, n])
        plt.plot(sbits, machine_error, '--k')

    # Loop over physics schemes
    for scheme in filenames:
        print(scheme)
        plp = physics_schemes[scheme]

        fp = load_tendency(variable=variable, scheme=scheme, rp_scheme='all_parametrizations', precision=52)
        rp = load_tendency(variable=variable, scheme=scheme, rp_scheme=filenames[scheme], precision=range(5, 24))

        rel_error = display_errors(rp, fp, axes, 0, plp)

        # Print errors
        error = rel_error/machine_error
        print(error.data.min(), error.data.max(), error.data.mean(), '\n')

    # Errors with respect to total physics tendency
    fp = load_tendency(variable=variable, rp_scheme='all_parametrizations', precision=52)

    filenames['Cloud'] = 'cloud'

    for scheme in filenames:
        rp = load_tendency(variable=variable, rp_scheme=filenames[scheme], precision=range(5, 24))
        plp = physics_schemes[scheme]
        rel_error = display_errors(rp, fp, axes, 1, plp, label=scheme)
        error = rel_error / machine_error
        print(scheme, error.data.min(), error.data.max(), error.data.mean())

    # Add dressing to the plot
    plt.axes(axes[1, 1])
    legend(key=lambda x: physics_schemes[x[0]].idx, ncol=2,
           title='Parametrization Schemes')
    multilabel(axes[0, 0], 0, factor=0.01)
    multilabel(axes[0, 1], 1, factor=0.01)
    multilabel(axes[1, 0], 2, factor=0.01)
    multilabel(axes[1, 1], 3, factor=0.01)

    plt.gcf().set_size_inches(16, 9)
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
