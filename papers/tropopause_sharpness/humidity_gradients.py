"""Plot analysis data relative to the tropopause
"""

import matplotlib.pyplot as plt
import iris.plot as iplt
from mymodule import convert, plot
from systematic_forecasts import second_analysis
from scripts.papers.tropopause_sharpness import plotdir

coord = 'distance_from_dynamical_tropopause'
variables = ['specific_humidity',
             'vertical_vorticity',
             'mass_fraction_of_cloud_liquid_water_in_air',
             'mass_fraction_of_cloud_ice_in_air']

nrows = 2
ncols = 2


def humidity_gradients():
    # Initialise the plot
    fig = plt.figure(figsize=(18, 15))

    # Columns are Ridges and troughs
    for n, variable in enumerate(variables):
        row = n / ncols
        col = n - row * ncols
        print row, col
        ax = plt.subplot2grid((nrows, ncols), (row, col))
        for subdomain, linestyle in [('ridges', '-'), ('troughs', '--')]:
            cubes = second_analysis.get_data(coord, subdomain)

            cube = convert.calc(variable, cubes)
            cube.coord(coord).convert_units('km')
            mean, std_err = second_analysis.extract_statistics(
                cube, 'forecast_index')

            if variable == 'vertical_vorticity':
                mean.data = mean.data + 1e-4
            else:
                mean.data = mean.data * 1e3
                std_err.data = std_err.data * 1e3

            iplt.plot(mean[0], mean.coord(coord),  # xerr=std_err[0],
                      linestyle=linestyle, label=subdomain.capitalize(),
                      color='k', marker='x', ms=5)

            ax.set_ylabel('')
            ax.set_ylim(-2, 2)
            if col > 0:
                ax.get_yaxis().set_ticklabels([])

        if variable == 'specific_humidity':
            ax.set_title('Specific Humidity')
            ax.set_xlabel(r'Mass Fraction (g kg$^{-1}$)')
        elif variable == 'vertical_vorticity':
            ax.set_title('Vertical Vorticity')
            ax.set_xlabel(r'Vorticity (s$^{-1}$)')
        elif variable == 'mass_fraction_of_cloud_liquid_water_in_air':
            ax.set_title('Cloud Liquid')
            ax.set_xlabel(r'Mass Fraction (g kg$^{-1}$)')
        elif variable == 'mass_fraction_of_cloud_ice_in_air':
            ax.set_title('Cloud Ice')
            ax.set_xlabel(r'Mass Fraction (g kg$^{-1}$)')

        plt.axhline(color='k')
        plot.multilabel(ax, n)

    plot.legend(ax=fig.axes[0], loc='best')
    fig.text(0.075, 0.5, 'Vertical distance from tropopause (km)',
             va='center', rotation='vertical')

    plt.savefig(plotdir + 'analysis_profiles.pdf')
    plt.show()

if __name__ == '__main__':
    humidity_gradients()
