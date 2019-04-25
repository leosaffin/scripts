"""
Show the errors in physics tendencies as a function of precision. Show both
relative and absolute errors (haven't decided on mean_diff or rms_diff). For
relative errors, this can be directly compared to the machine epsilon so add
this line also. Also print out errors as a function of machine epsilon to be
shown in a table.
"""
import warnings

import numpy as np
import matplotlib.pyplot as plt
import iris.exceptions
from iris.analysis import maths
from irise.plot.util import legend, multilabel

from myscripts.statistics import global_mean
from myscripts.models import speedy
from myscripts.projects.ithaca.tendencies import plotdir, load_tendency


warnings.filterwarnings('ignore')


schemes = ['All Parametrizations',
           'Condensation', 'Convection', 'Cloud',
           'Short-Wave Radiation', 'Long-Wave Radiation',
           'Surface Fluxes', 'Vertical Diffusion']


def main():
    generate_table()

    return


def generate_table():
    for variable in ['Temperature', 'Specific Humidity',
                     'Zonal Velocity', 'Meridional Velocity']:
        print(variable)
        table = {}
        for scheme in schemes:
            table[scheme] = scheme
        for label, sigma in [('Boundary Layer', speedy.sigma_levels[0]),
                             ('Lower Troposphere', speedy.sigma_levels[1:4]),
                             ('Upper Troposphere', speedy.sigma_levels[4:6]),
                             ('Stratosphere', speedy.sigma_levels[6:8])]:
            main2(variable, sigma, table)
            #plt.savefig(
            #    plotdir + 'error_vs_precision/' +
            #    '{}_{}.png'.format(label, variable).lower().replace(' ', '_'))
            plt.show()

        for scheme in schemes:
            print(table[scheme] + '\\\\')

    return


def main2(variable, sigma, table):
    # Create a two by two grid
    fig, axes = plt.subplots(nrows=1, ncols=2, sharey='row',
                             figsize=(16, 5),
                             subplot_kw={'yscale': 'log'})

    # Show the reference machine epsilon
    sbits = np.arange(5, 24)
    machine_error = 2.0 ** -(sbits + 1)

    # Errors with respect to individual parametrization tendency
    plt.axes(axes[0])
    for scheme in schemes:
        plp = speedy.physics_schemes[scheme]

        try:
            fp = load_tendency(variable=variable, scheme=scheme,
                               rp_scheme='all_parametrizations',
                               sigma=sigma, precision=52)
            rp = load_tendency(variable=variable, scheme=scheme,
                               rp_scheme=filename(scheme),
                               sigma=sigma, precision=sbits)

            # Ignore where tendencies are zero
            rp.data = np.ma.masked_where((rp.data - fp.data) == 0, rp.data)

            display_errors(rp, fp, plp)

        except iris.exceptions.ConstraintMismatchError:
            print('{} cannot be loaded \n'.format(scheme))

    # Errors with respect to total parametrization tendency
    plt.axes(axes[1])
    fp = load_tendency(variable=variable, rp_scheme='all_parametrizations',
                       sigma=sigma, precision=52)

    tendency = global_mean(maths.abs(fp))
    tendency = collapse_sigma(tendency)
    axes[1].axhline(
        tendency.data, linestyle='--', color='k', alpha=0.5)
    axes[1].plot(
        sbits, machine_error * tendency.data, ':k', alpha=0.5)

    for scheme in schemes:
        plp = speedy.physics_schemes[scheme]

        rp = load_tendency(variable=variable, rp_scheme=filename(scheme),
                           sigma=sigma, precision=sbits)

        error = display_errors(rp, fp, plp, label=scheme)
        error = (error/tendency) / machine_error

        table[scheme] += ' & ${:.0f}-{:.0f}\\varepsilon$'.format(error.data.min(), error.data.max())

    # Add dressing to the plot
    multilabel(axes[0], 0, factor=0.01)
    axes[0].set_title('Individual Temperature Tendency')
    axes[0].set_ylabel('Average Tendency Error [{}]'.format(tendency.units))
    axes[0].set_xticks(sbits[::5])

    multilabel(axes[1], 1, factor=0.01)
    axes[1].set_title('Total Temperature Tendency')
    axes[1].set_xticks(sbits[::5])

    fig.text(0.45, 0.01, 'Precision [sbits]')
    legend(ax=axes[1], key=lambda x: speedy.physics_schemes[x[0]].idx, ncol=2)
    plt.subplots_adjust(left=0.08, right=0.98, wspace=0.05)

    return


def filename(scheme):
    return scheme.replace(' ', '_').replace('-', '_').lower()


def display_errors(rp, fp,  plp, **kwargs):
    # Calculate absolute error
    abs_error = maths.abs(rp - fp)
    abs_error = global_mean(abs_error)
    abs_error = collapse_sigma(abs_error)
    plp.plot(abs_error, **kwargs)

    return abs_error


def collapse_sigma(cube, coord_name='sigma'):
    if len(cube.coord(coord_name).points) > 1:
        return cube.collapsed(coord_name, iris.analysis.MEAN)
    else:
        return cube


if __name__ == '__main__':
    main()
