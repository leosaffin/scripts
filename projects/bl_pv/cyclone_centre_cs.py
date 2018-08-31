"""Cross-section through IOP8 cyclone centre
"""
from string import ascii_uppercase
from math import ceil
import numpy as np
import matplotlib.pyplot as plt
import iris.plot as iplt
from mymodule import convert, interpolate, plot, user_variables
from myscripts.models.um import case_studies
from systematic_forecasts import second_analysis
from myscripts.projects.bl_pv import plotdir


job = 'iop8_no_microphysics'
forecast = case_studies.iop8_no_microphysics.copy()
track = np.load(user_variables.datadir + job + '_cyclone_track.npy')

names = [
    'total_minus_advection_only_pv',
    'long_wave_radiation_pv',
    'microphysics_pv',
    'convection_pv',
    'boundary_layer_pv',
    'ertel_potential_vorticity',

    'total_minus_advection_only_theta',
    'long_wave_radiation_theta',
    'microphysics_theta',
    'convection_theta',
    'boundary_layer_theta',
    'boundary_layer_latent_heating_theta'
]

coords = ['grid_longitude', 'altitude']

nrows = int(ceil(np.sqrt(len(names))))
ncols = int(ceil(len(names) / float(nrows)))

# Contour levels to plot variables
plevs = np.arange(950, 1050, 5)
theta_levs = np.arange(270, 320, 2.5)
plevs_vert = [950]
rh_levs = [0.7, 0.8, 0.9]

# Points for IOP8 cyclone centre and trailing cold front
keys = ['cyclone_zonal', 'cyclone_meridional', 'front']
points = {}
points[18] = {}
points[18]['cyclone_zonal'] = (-8, 4.5, -2, 6.5)
points[18]['cyclone_meridional'] = (-6.95, 8.67, -4.95, 2.67)
points[18]['front'] = (-9, 3, -5, -2)
points[24] = {}
points[24]['cyclone'] = (-5, 3.5, 3, 8)
points[24]['front'] = (-5, 3.5, 3, 8)

time = 18


def main(cubes):
    fig = overview()
    fig.savefig(plotdir + job + '_overview_' + str(time) + 'h.png')

    for key in keys:
        xs, ys, xf, yf = points[time][key]
        if key is 'front':
            ylims = 0, 4
        else:
            ylims = 0, 8
        fig = cross_sections(xs, xf, ys, yf, ylims)
        fig.savefig(plotdir + job + '_cross_section_' + key + '_' +
                    str(time) + 'h.pdf')

    return


def cs_cube(cube, xs, xf, ys, yf):
    newcube = interpolate.cross_section(cube, xs, xf, ys, yf, 100)
    for coord in newcube.coords():
        if coord.units == 'm':
            coord.convert_units('km')

    return newcube


def overview():
    # [100:280, 100:350]
    mslp = convert.calc('air_pressure_at_sea_level', cubes)[100:280, 100:350]
    mslp.convert_units('hPa')
    pv = convert.calc('ertel_potential_vorticity', cubes,
                      levels=('altitude', [500]))[0, 100:280, 100:350]

    figure = plt.figure(figsize=(12, 10))
    plot_overview(mslp, pv)

    n = 0
    for key in keys:
        xs, ys, xf, yf = points[time][key]
        plt.plot([xs, xf], [ys, yf], '-kx')
        plt.text(xs - 1, ys, ascii_uppercase[n], fontsize=25)
        n += 1
        plt.text(xf, yf, ascii_uppercase[n], fontsize=25)
        n += 1

    return figure


def plot_overview(mslp, pv):
    iplt.contourf(
        pv, plot.even_cscale(2), cmap='coolwarm', spacing='proportional',
        extend='both')
    plot._add_map()
    cbar = plt.colorbar(
        orientation='horizontal', fraction=0.05, spacing='proportional')
    cbar.set_label('PVU')
    cbar.set_ticks(np.linspace(-2, 2, 9))
    cs = iplt.contour(mslp, plevs, colors='k', linewidths=1)
    plt.clabel(cs, fmt='%1.0f', colors='k')
    plt.plot(track[:, 0], track[:, 1], '-y')
    plt.plot(track[time, 0], track[time, 1], 'yx', markersize=15)

    return


def cross_sections(xs, xf, ys, yf, ylims):
    # Pre-calculate parameters on every plot
    tracers = convert.calc(names, cubes)
    cs_tracers = []
    for cube in tracers:
        cs_tracers.append(cs_cube(cube, xs, xf, ys, yf))

    pv = convert.calc('ertel_potential_vorticity', cubes)
    pv = cs_cube(pv, xs, xf, ys, yf)

    theta = convert.calc('air_potential_temperature', cubes)
    theta = cs_cube(theta, xs, xf, ys, yf)

    theta_e = convert.calc('equivalent_potential_temperature', cubes)
    theta_e = cs_cube(theta_e, xs, xf, ys, yf)

    rh = convert.calc('relative_humidity', cubes)
    rh = cs_cube(rh, xs, xf, ys, yf)

    z_bl = convert.calc('boundary_layer_height', cubes)
    z_bl = cs_cube(z_bl, xs, xf, ys, yf)
    z_bl.convert_units('km')

    figure = plt.figure(figsize=(18, 12))
    plot_cross_sections(
        cs_tracers, pv, theta, theta_e, rh, z_bl, figure, ylims)

    return figure


def plot_cross_sections(tracers, pv, theta, theta_e, rh, z_bl, fig, ylims):
    # Plot each cube separately
    for n, cube in enumerate(tracers):
        row = n / ncols
        col = n - row * ncols
        ax = plt.subplot2grid((nrows, ncols), (row, col))

        # Interpolate along the cross section
        im = plot_cross_section(
            cube, pv, theta, theta_e, z_bl, rh, ax, n, ylims)

    # Add letter labels to panels
    for n, ax in enumerate(fig.axes):
        plot.multilabel(ax, n)

    # Add colorbar at bottom of figure
    cbar = plt.colorbar(im, ax=fig.axes, orientation='horizontal',
                        fraction=0.05, spacing='proportional')
    cbar.set_label('K')
    cbar.set_ticks(np.linspace(-20, 20, 9))

    fig.text(0.075, 0.58, 'Height (km)',
             va='center', rotation='vertical')
    fig.text(0.5, 0.2, 'Grid Longitude', ha='center')
    return


def plot_cross_section(cube, pv, theta, theta_e, z_bl, rh,
                       ax, n, ylims):
    # Make the plot
    if cube.units == 'K':
        im = iplt.contourf(cube, plot.even_cscale(20), coords=coords,
                           cmap='coolwarm', extend='both')
    elif cube.units == 'PVU':
        im = iplt.contourf(cube, plot.even_cscale(2), coords=coords,
                           cmap='coolwarm', extend='both')
    else:
        print(cube.units)

    iplt.contour(pv, [2], colors='k', coords=coords)

    cs_theta = iplt.contour(theta, theta_levs, coords=coords,
                            colors='k', linewidths=1, linestyles='-')

    cs_theta_e = iplt.contour(theta_e, theta_levs, coords=coords,
                              colors='w', linewidths=1, linestyles='-')

    iplt.plot(z_bl.coord('grid_longitude'), z_bl, color='y')
    iplt.contour(rh, [0.8], coords=coords, colors='grey')
    iplt.contourf(rh, [0.8, 2], coords=coords,
                  colors='None', hatches=['.'])
    plt.title(second_analysis.all_diagnostics[cube.name()].symbol)

    if n == 0:
        plt.clabel(cs_theta, fmt='%1.1f')
        plt.clabel(cs_theta_e, fmt='%1.1f')
    ax.set_ylim(*ylims)

    if n < (nrows - 1) * ncols:
        ax.set_xticks([])

    if n % ncols != 0:
        ax.set_yticks([])

    return im

if __name__ == '__main__':
    cubes = forecast.set_lead_time(hours=time)
    main(cubes)
