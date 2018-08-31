"""Cross-section through large cancellation in cold sector
"""

from math import ceil, floor
import numpy as np
import matplotlib.pyplot as plt
import iris.plot as iplt
from mymodule import convert, interpolate, plot
from myscripts import case_studies
from systematic_forecasts import second_analysis
from myscripts.projects.thesis.bl import plotdir

names = [
    'total_minus_advection_only_pv',
    #'short_wave_radiation_pv',
    'long_wave_radiation_pv',
    #'microphysics_pv',
    #'gravity_wave_drag_pv',
    #'convection_pv',
    'boundary_layer_pv',
    'dynamics_tracer_inconsistency',
    #'residual_pv'
]

nrows = int(ceil(np.sqrt(len(names))))
ncols = int(floor(len(names) / float(nrows)))

# Contour levels to plot variables
plevs = np.linspace(950, 1050, 11)
theta_levs = np.linspace(280, 320, 17)
rh_levs = [0.7, 0.8, 0.9]


# Points for IOP5
xs, xf, ys, yf = -10, 6, 4, 2
manual = [(3.6, 0.6), (3.5, 6), (3.1, 4.7), (2.6, 2.2), (2.3, 0.3),
          (2.6, 3.4), (2.2, 3.7)]

# Points for IOP8
"""
xs, xf, ys, yf = -8, 6, 7, 4
manual = [(5.3, 6.1), (5.5, 5.5), (4.5, 3),
          (4.25, 2.4), (6.3, 6.3), (6.8, 6.4)]
"""


def main(cubes, **kwargs):
    # Pre-calculate parameters on every plot
    tracers = convert.calc(names, cubes)
    mslp = convert.calc('air_pressure_at_sea_level', cubes)
    theta = convert.calc('air_potential_temperature', cubes)
    theta = cs_cube(theta, xs, xf, ys, yf)
    rh = convert.calc('relative_humidity', cubes)
    rh = cs_cube(rh, xs, xf, ys, yf)
    z_bl = convert.calc('boundary_layer_height', cubes)
    z_bl = cs_cube(z_bl, xs, xf, ys, yf)
    z_bl.convert_units('km')

    fig1 = plt.figure(figsize=(18, 12))
    bottom_level(tracers, mslp, fig1, **kwargs)
    fig1.savefig(plotdir + 'iop8_z0.png')

    #fig2 = plt.figure(figsize=(18, 12))
    #cross_sections(tracers, theta, rh, z_bl, fig2)
    #fig2.savefig(plotdir + 'iop8_z0_cs.pdf')

    plt.show()

    return


def cs_cube(cube, xs, xf, ys, yf):
    newcube = interpolate.cross_section(cube, xs, xf, ys, yf, 100)
    for coord in newcube.coords():
        if coord.units == 'm':
            coord.convert_units('km')

    return newcube


def bottom_level(tracers, mslp, fig, **kwargs):
    # Plot each cube separately
    for n, cube in enumerate(tracers):
        row = n / ncols
        col = n - row * ncols
        ax = plt.subplot2grid((nrows, ncols), (row, col))

        # Make the plot
        im = iplt.pcolormesh(cube[0], **kwargs)
        mslp.convert_units('hPa')
        cs = iplt.contour(mslp, plevs, colors='k', linewidths=2)
        plt.clabel(cs, fmt='%1.0f')
        plot._add_map()
        plt.title(second_analysis.all_diagnostics[cube.name()].symbol)

        # Label the cross section points
        if n == 0:
            plt.plot([xs, xf], [ys, yf], '-kx')
            plt.text(xs, ys, 'A', fontsize=20)
            plt.text(xf, yf, 'B', fontsize=20)

    # Add letter labels to panels
    for n, ax in enumerate(fig.axes):
        plot.multilabel(ax, n)

    # Add colorbar at bottom of figure
    cbar = plt.colorbar(im, ax=fig.axes, orientation='horizontal',
                        fraction=0.05)
    cbar.set_label('PVU')

    return


def cross_sections(tracers, theta, rh, z_bl, fig):
    # Plot each cube separately
    for n, cube in enumerate(tracers):
        row = n / ncols
        col = n - row * ncols
        ax = plt.subplot2grid((nrows, ncols), (row, col))

        # Interpolate along the cross section
        cube = cs_cube(cube, xs, xf, ys, yf)
        coords = ['grid_longitude', 'altitude']

        # Make the plot
        im = iplt.contourf(cube, plot.even_cscale(2), coords=coords,
                           cmap='coolwarm', extend='both')
        cs = iplt.contour(theta, theta_levs, coords=coords,
                          colors='k', linewidths=2)
        iplt.plot(z_bl.coord('grid_longitude'), z_bl, color='y')
        iplt.contour(rh, [0.8], coords=coords, colors='w')
        iplt.contourf(rh, [0.8, 2], coords=coords,
                      colors='None', hatches=['.'])
        plt.title(second_analysis.all_diagnostics[cube.name()].symbol)

        if n == 0:
            plt.clabel(cs, fmt='%1.0f', colors='k')
        ax.set_ylim(0, 7)

        if n < 4:
            ax.set_xticks([])

    # Add letter labels to panels
    for n, ax in enumerate(fig.axes):
        plot.multilabel(ax, n)

    # Add colorbar at bottom of figure
    cbar = plt.colorbar(im, ax=fig.axes, orientation='horizontal',
                        fraction=0.05, spacing='proportional')
    cbar.set_label('PVU')
    cbar.set_ticks(np.linspace(-2, 2, 9))

    fig.text(0.075, 0.58, 'Height (km)',
             va='center', rotation='vertical')
    fig.text(0.5, 0.2, 'Grid Longitude', ha='center')
    return


def tephigram(theta, rh):
    for idx in (0, -1):
        fig, ax1 = plt.subplots()

        iplt.plot(theta[idx], '-k')

        ax2 = ax1.twinx()
        iplt.plot(rh[idx], '--k')

    return

if __name__ == '__main__':
    forecast = case_studies.iop8.copy()
    cubes = forecast.set_lead_time(hours=24)
    main(cubes, vmin=-20, vmax=20, cmap='coolwarm')
