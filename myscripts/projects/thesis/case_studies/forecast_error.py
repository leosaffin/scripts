"""Plot PV on 320K for the forecast and analysis
"""
from string import ascii_lowercase
import numpy as np
import matplotlib.pyplot as plt
import iris.plot as iplt
from irise import convert
from irise.plot.util import add_map, even_cscale
from myscripts.models.um import case_studies
from myscripts.projects.thesis.case_studies import plotdir


def main(dt):
    forecast = case_studies.iop5b.copy()
    cubes_f = forecast.set_lead_time(hours=dt)

    analysis = case_studies.iop5_analyses.copy()
    cubes_a = analysis.set_lead_time(hours=dt)

    # Mask land
    z_0 = convert.calc('altitude', cubes_f)[0]

    make_plots(cubes_f, cubes_a, 'air_potential_temperature',
               ('air_pressure', [90000]), 'K',
               even_cscale(10, 11),
               np.linspace(270, 300, 13))
    plt.savefig(plotdir + 'iop5_T_error.pdf')
    """

    # Low-level pressure
    fig = plt.figure(figsize=(18, 8))
    ax = plt.subplot2grid((1, 2), (0, 0))
    make_plot(cubes_f, cubes_a, 'air_pressure', None, 'hPa',
              even_cscale(5, 11), np.linspace(950, 1050, 11),
              mask=z_0.data != 20)
    plt.title('(a)'.ljust(30) + 'p(20 m)'.ljust(35))

    # Geopotential height
    ax = plt.subplot2grid((1, 2), (0, 1))
    make_plot(cubes_f, cubes_a, 'altitude', ('air_pressure', [50000]), 'm',
              even_cscale(50, 11), np.linspace(5000, 6000, 11))
    plt.title('(b)'.ljust(30) + 'z(500 hPa)'.ljust(35))

    plt.savefig(plotdir + 'iop8_errors.pdf')

    plt.show()
    """

    return


def make_plot(forecast, analysis, variable, levels, units, errlevs, clevs,
              cmap='coolwarm', mask=None):
    # Extract data and errors
    f = convert.calc(variable, forecast, levels=levels)[0]
    a = convert.calc(variable, analysis, levels=levels)[0]
    err = f - a

    for cube in [f, a, err]:
        cube.convert_units(units)

    if mask is not None:
        for cube in [f, a]:
            cube.data = np.ma.masked_where(mask, cube.data)

    # Plot error
    iplt.contourf(err, errlevs, cmap=cmap, extend='both')
    add_map()
    cbar = plt.colorbar(orientation='horizontal', spacing='proportional')
    errlevs.append(0)
    cbar.set_ticks(errlevs)
    cbar.set_label(units)

    # Overlay forecast and analysis
    cs = iplt.contour(f, clevs, colors='k', linewidths=2)
    iplt.contour(a, clevs, colors='k', linewidths=2, linestyles='--')
    plt.clabel(cs, fmt='%1.0f', colors='k')

    return


def make_plots(forecast, analysis, variable, levels, units, errlevs, clevs,
               cmap1='plasma', cmap='coolwarm', mask=None):
    # Extract data and errors
    f = convert.calc(variable, forecast, levels=levels)[0]
    a = convert.calc(variable, analysis, levels=levels)[0]
    err = f - a

    for cube in [f, a, err]:
        cube.convert_units(units)

    if mask is not None:
        for cube in [f, a]:
            cube.data = np.ma.masked_where(mask, cube.data)

    # Initialise the plot
    plt.figure(figsize=(18, 15))

    # Plot absolute values
    plt.subplot2grid((25, 4), (0, 0), colspan=2, rowspan=10)
    im = iplt.contourf(f, clevs, extend='both', cmap=cmap1)
    #iplt.contour(f, [2], colors='k')
    plt.title('(a)'.ljust(28) + 'Forecast'.ljust(35))
    add_map()

    plt.subplot2grid((25, 4), (0, 2), colspan=2, rowspan=10)
    im = iplt.contourf(a, clevs, extend='both', cmap=cmap1)
    #iplt.contour(a, [2], colors='k', linestyles='--')
    plt.title('(b)'.ljust(28) + 'Analysis'.ljust(35))
    add_map()

    ax = plt.subplot2grid((25, 4), (10, 1), colspan=2, rowspan=1)
    cbar = plt.colorbar(im, cax=ax, orientation='horizontal')
    cbar.set_label(units)
    # cbar.set_ticks(range(11))

    # Plot error
    plt.subplot2grid((25, 4), (13, 1), colspan=2, rowspan=10)
    im = iplt.contourf(err, errlevs, cmap=cmap, extend='both')
    #iplt.contour(f, [2], colors='k')
    #iplt.contour(a, [2], colors='k', linestyles='--')
    plt.title('(c)'.ljust(20) + 'Forecast Minus Analysis.'.ljust(38))
    add_map()

    ax = plt.subplot2grid((25, 4), (23, 1), colspan=2, rowspan=1)
    cbar = plt.colorbar(im, cax=ax, orientation='horizontal',
                        spacing='proportional')
    errlevs.append(0)
    cbar.set_ticks(errlevs)
    cbar.set_label(units)

    return


def pv(forecast, analysis, variable, levels, **kwargs):
    pv_f = convert.calc(variable, forecast, levels=levels)[0]
    pv_a = convert.calc(variable, analysis, levels=levels)[0]

    err = pv_f - pv_a
    axes = []

    # Initialise the plot
    fig = plt.figure(figsize=(18, 20))

    axes.append(plt.subplot2grid((25, 4), (0, 0), colspan=2, rowspan=10))
    im = make_pv_plot(pv_f, **kwargs)
    plt.title('Forecast')

    axes.append(plt.subplot2grid((25, 4), (0, 2), colspan=2, rowspan=10))
    im = make_pv_plot(pv_a, **kwargs)
    plt.title('Analysis')

    ax = plt.subplot2grid((25, 4), (10, 1), colspan=2, rowspan=1)
    cbar = plt.colorbar(im, cax=ax, orientation='horizontal')

    axes.append(plt.subplot2grid((25, 4), (13, 1), colspan=2, rowspan=10))
    im = iplt.pcolormesh(err, vmin=-5, vmax=5, cmap='coolwarm')
    iplt.contour(pv_f, [2], colors='k', linewidths=2)
    iplt.contour(pv_a, [2], colors='k', linewidths=2, linestyles='--')
    add_map()
    plt.title('Forecast Minus Analysis')

    ax = plt.subplot2grid((25, 4), (23, 1), colspan=2, rowspan=1)
    cbar = plt.colorbar(im, cax=ax, orientation='horizontal')

    for n, ax in enumerate(axes):
        ax.set_title(ascii_lowercase[n].ljust(20))
    plt.show()


def make_pv_plot(pv, **kwargs):
    im = iplt.pcolormesh(pv, **kwargs)
    iplt.contour(pv, [2], colors='k', linewidths=2)
    add_map()

    return im


if __name__ == '__main__':
    dt = 24
    main(dt)
