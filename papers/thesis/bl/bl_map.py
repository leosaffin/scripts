from math import ceil
import numpy as np
import matplotlib.pyplot as plt
import iris.plot as iplt
from mymodule import convert, plot
from scripts import case_studies
from systematic_forecasts import second_analysis
from scripts.papers.thesis.bl import plotdir

names = [
    'total_minus_advection_only_pv',
    #'short_wave_radiation_pv',
    'long_wave_radiation_pv',
    #'microphysics_pv',
    'gravity_wave_drag_pv',
    'convection_pv',
    'boundary_layer_pv',
    'dynamics_tracer_inconsistency',
    #'residual_pv'
]
nrows = int(ceil(np.sqrt(len(names))))
ncols = int(ceil(len(names) / float(nrows)))


def main(cubes, levels, *args, **kwargs):
    # Initialise the plot
    fig = plt.figure(figsize=(18, 20))

    for n, name in enumerate(names):
        row = n / ncols
        col = n - row * ncols
        print row, col
        ax = plt.subplot2grid((nrows, ncols), (row, col))

        cube = convert.calc(name, cubes, levels=levels)[0]
        im = iplt.pcolormesh(cube, *args, **kwargs)
        plot._add_map()
        plt.title(second_analysis.all_diagnostics[name].symbol)

    for n, ax in enumerate(fig.axes):
        plot.multilabel(ax, n)

    cbar = plt.colorbar(im, ax=fig.axes, orientation='horizontal',
                        fraction=0.05, spacing='proportional')
    cbar.set_label('PVU')
    # cbar.set_ticks(np.array(levels)[::2])

    plt.savefig(plotdir + 'iop5_bl_map.png')
    # plt.show()

    return

if __name__ == '__main__':
    forecast = case_studies.iop5b.copy()
    cubes = forecast.set_lead_time(hours=24)
    z_bl = convert.calc('boundary_layer_height', cubes)
    levels = ('altitude', z_bl.data[None, :, :])
    main(cubes, levels, vmin=-10, vmax=10, cmap='coolwarm')
