import numpy as np
import matplotlib.pyplot as plt
import iris.plot as iplt
from mymodule import convert, plot
from myscripts import case_studies
from myscripts.projects.thesis.case_studies import plotdir

levels = ('altitude', [1000])
levs = np.linspace(0, 50, 21)
errlevs = plot.even_cscale(25, levels=21)


def main(dt):
    fig = plt.figure(figsize=(18, 15))

    # Load data
    forecast = case_studies.iop8.copy()
    cubes_f = forecast.set_lead_time(hours=24)
    analysis = case_studies.iop8_analyses.copy()
    cubes_a = analysis.set_lead_time(hours=24)

    # Forecast
    plt.subplot2grid((25, 4), (0, 0), colspan=2, rowspan=10)
    wind_speed(cubes_f, levs, cmap='magma_r')
    plt.title('(a)'.ljust(28) + 'Forecast'.ljust(35))

    # Analysis
    plt.subplot2grid((25, 4), (0, 2), colspan=2, rowspan=10)
    im = wind_speed(cubes_a, levs, cmap='magma_r')
    plt.title('(b)'.ljust(28) + 'Analysis'.ljust(35))

    # Colourbar
    ax = plt.subplot2grid((25, 4), (10, 1), colspan=2, rowspan=1)
    cbar = plt.colorbar(im, cax=ax, orientation='horizontal')
    cbar.set_label(r'm s$^{-1}$')
    cbar.set_ticks(range(0, 60, 10))

    # Plot error
    plt.subplot2grid((25, 4), (13, 1), colspan=2, rowspan=10)
    im = wind_speed(cubes_f, errlevs, cubes_a=cubes_a, cmap='coolwarm')
    plt.title('(c)'.ljust(20) + 'Forecast Minus Analysis.'.ljust(38))

    ax = plt.subplot2grid((25, 4), (23, 1), colspan=2, rowspan=1)
    cbar = plt.colorbar(im, cax=ax, orientation='horizontal',
                        spacing='proportional')
    errlevs.append(0)
    cbar.set_ticks(np.linspace(-25, 25, 11))
    cbar.set_label(r'm s$^{-1}$')

    plt.savefig(plotdir + 'iop8_winds.pdf')
    # plt.show()

    return


def wind_speed(cubes, levs, cubes_a=None, **kwargs):
    u = convert.calc('x_wind', cubes, levels=levels)[0]
    v = convert.calc('y_wind', cubes, levels=levels)[0]
    w = convert.calc('upward_air_velocity', cubes, levels=levels)[0]
    wind = (u.data**2 + v.data**2 + w.data**2)**0.5
    wind = u.copy(data=wind)

    if cubes_a is not None:
        u_a = convert.calc('x_wind', cubes_a, levels=levels)[0]
        v_a = convert.calc('y_wind', cubes_a, levels=levels)[0]
        w_a = convert.calc('upward_air_velocity', cubes_a, levels=levels)[0]
        wind_a = (u_a.data**2 + v_a.data**2 + w_a.data**2)**0.5
        wind.data -= wind_a
        u -= u_a
        v -= v_a
        w -= w_a

    print(wind.data.max(), wind.data.min())
    im = iplt.contourf(wind, levs, **kwargs)
    plot._add_map()
    plot.overlay_winds(u, v, 33, 57, scale=1500)

    return im


if __name__ == '__main__':
    forecast = case_studies.iop8.copy()
    cubes = forecast.set_lead_time(hours=24)
    main(cubes)
