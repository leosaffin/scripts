from math import ceil, floor
import numpy as np
import matplotlib.pyplot as plt
import iris.plot as iplt
from irise import convert
from irise.plot.util import multilabel, even_cscale
from systematic_forecasts import second_analysis
from myscripts.projects.thesis import plotdir

filename = plotdir + 'ch7_low/acc_tendencies_height.pdf'

names = ['total_minus_advection_only_pv', 'dynamics_tracer_inconsistency',
         'long_wave_radiation_pv', 'microphysics_pv',
         'convection_pv', 'boundary_layer_pv']

coord = 'altitude'

nrows = int(ceil(np.sqrt(len(names))))
ncols = int(ceil(len(names) / float(nrows)))


def main(*args, **kwargs):
    # Initialise the plot
    fig = plt.figure(figsize=(18, 15))

    cubes = second_analysis.get_data(coord, 'full')
    for n, name in enumerate(names):
        row = n / ncols
        col = n - row * ncols
        ax = plt.subplot2grid((nrows, ncols), (row, col))

        cube = convert.calc(name, cubes)
        cube.coord(coord).convert_units('km')
        mean, std_err = second_analysis.extract_statistics(
            cube, 'forecast_index')

        im = iplt.contourf(mean, *args, **kwargs)
        ax.set_ylim(1, 17)

        ax.set_title(second_analysis.all_diagnostics[name].symbol,
                     fontsize=25)
        multilabel(ax, n)

        if row == 1 and col == 0:
            ax.set_ylabel('Height (km)')

        if row < nrows - 1:
            ax.get_xaxis().set_ticklabels([])

        if col > 0:
            ax.get_yaxis().set_ticklabels([])

    cbar = plt.colorbar(im, ax=fig.axes, fraction=0.05,
                        orientation='horizontal', spacing='proportional')
    cbar.set_ticks([-0.1, -0.05, 0, 0.05, 0.1])
    cbar.set_label('PVU')

    fig.text(0.5, 0.2, 'Forecast Lead Time (hours)', ha='center')

    plt.savefig(filename)
    plt.show()

    return


if __name__ == '__main__':
    main(even_cscale(0.1, 17), cmap='coolwarm', extend='both')
