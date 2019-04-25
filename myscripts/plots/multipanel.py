from math import ceil
import numpy as np
import matplotlib.pyplot as plt
import iris.plot as iplt
from irise import convert, grid
from irise.plot.util import multilabel, add_map, even_cscale
from myscripts.models.um import case_studies
from myscripts.projects.thesis.fronts import plotdir
from systematic_forecasts import second_analysis


names = ['total_minus_advection_only_pv',
         #'short_wave_radiation_pv',
         'long_wave_radiation_pv',
         'microphysics_pv',
         #'gravity_wave_drag_pv',
         'convection_pv',
         'boundary_layer_pv',
         'dynamics_tracer_inconsistency'
         #'residual_pv'
         ]

nrows = int(ceil(np.sqrt(len(names))))
ncols = int(ceil(len(names) / float(nrows)))

slices = slice(75, -5), slice(140, -120)


def main(cubes, levels, *args, **kwargs):
    # Initialise the plot
    fig = plt.figure(figsize=(18, 20))

    pv = convert.calc('ertel_potential_vorticity', cubes, levels=levels)[0]
    theta = convert.calc('equivalent_potential_temperature', cubes,
                         levels=levels)[0][slices]

    rh = convert.calc('relative_humidity', cubes, levels=levels)[0][slices]

    lon, lat = grid.true_coords(theta)
    lonmask = np.logical_or(lon < -15, lon > 5)
    latmask = np.logical_or(lat < 47.5, lat > 62.5)
    areamask = np.logical_or(lonmask, latmask)
    mask = theta.copy(data=areamask.astype(int))

    for n, name in enumerate(names):
        row = n / ncols
        col = n - row * ncols
        print(row, col)
        ax = plt.subplot2grid((nrows, ncols), (row, col))

        cube = convert.calc(name, cubes, levels=levels)[0]  # [slices]
        im = iplt.contourf(cube, *args, **kwargs)
        #iplt.contour(pv, [2], colors='k', linewidths=2)
        iplt.contour(mask, [0.5], colors='k', linestyles='--')
        add_map()
        plt.title(second_analysis.all_diagnostics[name].symbol)

        iplt.contour(theta, [300], colors='k', linewidths=2)
        iplt.contour(rh, [0.8], colors='w', linewidths=2)
        iplt.contourf(rh, [0.8, 2], colors='None', hatches=['.'])

    for n, ax in enumerate(fig.axes):
        multilabel(ax, n)

    cbar = plt.colorbar(im, ax=fig.axes, orientation='horizontal',
                        fraction=0.05, spacing='proportional')
    cbar.set_label('PVU')
    cbar.set_ticks(np.linspace(-2, 2, 17)[::2])

    plt.savefig(plotdir + 'iop5_pv_tracers_24h_' +
                str(levels[1][0])[0:3] + 'hpa.pdf')
    # plt.show()

    return


if __name__ == '__main__':
    forecast = case_studies.iop5b.copy()
    cubes = forecast.set_lead_time(hours=24)
    for p in [60000, 75000, 90000]:
        levels = ('air_pressure', [p])
        main(cubes, levels, even_cscale(2), cmap='coolwarm',
             extend='both')
