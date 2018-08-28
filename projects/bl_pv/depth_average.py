from math import ceil, floor
import numpy as np
import matplotlib.pyplot as plt
import iris.plot as iplt
from iris.analysis import MEAN
from mymodule import convert, grid, plot
from scripts import case_studies
from systematic_forecasts.second_analysis import all_diagnostics
from scripts.projects.bl_pv import plotdir


def main():
    forecast = case_studies.iop8_no_microphysics.copy()
    cubes = forecast.set_lead_time(hours=18)

    names = [
        'ertel_potential_vorticity',
        'total_minus_advection_only_pv',
        'long_wave_radiation_pv',
        'microphysics_pv',
        'convection_pv',
        'boundary_layer_pv',
    ]

    nrows = int(floor(np.sqrt(len(names))))
    ncols = int(ceil(len(names) / float(nrows)))

    mask = make_mask(cubes)
    mass = convert.calc('mass', cubes)
    fig = plt.figure(figsize=(18, 10))
    for n, name in enumerate(names):
        row = n / ncols
        col = n - row * ncols
        plt.subplot2grid((nrows, ncols), (row, col))
        im = make_plot(cubes, name, mass, mask,
                       vmin=-2, vmax=2, cmap='coolwarm')
        plt.title(all_diagnostics[name].symbol)

    # Add letter labels to panels
    for n, ax in enumerate(fig.axes):
        plot.multilabel(ax, n)

    # Add colorbar at bottom of figure
    cbar = plt.colorbar(im, ax=fig.axes, orientation='horizontal',
                        fraction=0.05, spacing='proportional')
    cbar.set_label('PVU')
    cbar.set_ticks(np.linspace(-2, 2, 9))

    plt.savefig(plotdir + 'iop8_no_microphysics_bl_depth_average_pv.png')
    plt.show()

    return


def make_mask(cubes):
    z = convert.calc('altitude', cubes)
    z_bl = convert.calc('boundary_layer_height', cubes)
    mask = z.data > z_bl.data

    return mask


def make_plot(cubes, name, mass, mask, **kwargs):
    pv = convert.calc(name, cubes)
    pv.data = np.ma.masked_where(mask, pv.data)

    z = grid.extract_dim_coord(pv, 'z')
    pv_ave = pv.collapsed(z.name(), MEAN, weights=mass.data)

    im = iplt.pcolormesh(pv_ave, **kwargs)
    plot._add_map()

    return im


if __name__ == '__main__':
    main()
