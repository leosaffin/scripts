"""Time variation of dynamics-tracer inconsistency relative to q=2
"""

import matplotlib.pyplot as plt
import iris.plot as iplt
from mymodule import convert, plot
from systematic_forecasts import second_analysis
from myscripts.projects.tropopause_sharpness import plotdir

coords = ['distance_from_dynamical_tropopause',
          'distance_from_advection_only_tropopause']
name = 'dynamics_tracer_inconsistency'


def main(**kwargs):
    # Initialise the plot
    fig = plt.figure(figsize=(18, 15))

    for n, coord in enumerate(coords):
        for m, subdomain in enumerate(['ridges', 'troughs']):
            cubes = second_analysis.get_data(coord, subdomain)
            cube = convert.calc(name, cubes)
            cube.coord(coord).convert_units('km')
            mean, std_err = second_analysis.extract_statistics(
                cube, 'forecast_index')

            ax = plt.subplot2grid((2, 2), (n, m))
            im = iplt.contourf(mean, plot.even_cscale(0.18), cmap='coolwarm')

            # X-axis - Same for both columns
            ax.set_xticks([0, 12, 24, 36, 48, 60])
            if n == 0:
                ax.get_xaxis().set_ticklabels([])
                ax.set_title(subdomain.capitalize())

            # Y-axis - Same for both rows
            ax.set_ylim(-2, 2)
            ax.set_yticks([-2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2])
            ax.axhline(color='k')
            if m > 0:
                ax.get_yaxis().set_ticklabels([])

    add_labels(fig)

    fig.text(0.5, 0.2, 'Forecast Lead Time (hours)', ha='center')

    for n, axis in enumerate(fig.axes):
        plot.multilabel(axis, n)

    cbar = plt.colorbar(im, ax=fig.axes, orientation='horizontal',
                        fraction=0.05, spacing='proportional')
    cbar.set_ticks([-0.18, -0.09, 0,  0.09, 0.18])
    cbar.set_label('PVU')
    plt.savefig(plotdir + 'inconsistency.pdf')
    plt.show()

    return


def add_labels(fig):
    # Label coordinates
    fig.text(0.075, 0.58, 'Vertical Distance From Tropopause (km)',
             va='center', rotation='vertical')
    fig.text(0.05, 0.75, r'$z - z(q{=}2)$',
             va='center', rotation='vertical', fontsize=25)
    fig.text(0.05, 0.4, r'$z - z(q_{adv}{=}2)$',
             va='center', rotation='vertical', fontsize=25)

    return


if __name__ == '__main__':
    main(vmin=-0.15, vmax=0.15, cmap='coolwarm')
