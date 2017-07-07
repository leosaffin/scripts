import numpy as np
import matplotlib.pyplot as plt
import iris.plot as iplt
from mymodule import convert, plot
from scripts import case_studies
from scripts.papers.thesis.case_studies import plotdir

levels = ('altitude', [1000])


def main(dt):
    fig = plt.figure(figsize=(18, 8))

    forecast = case_studies.iop8.copy()
    cubes_f = forecast.set_lead_time(hours=24)
    ax = plt.subplot2grid((1, 2), (0, 0))
    wind_speed(cubes_f)
    plt.title(r'Forecast $\mathbf{u}$')

    analysis = case_studies.iop8_analyses.copy()
    cubes_a = analysis.set_lead_time(hours=24)
    ax = plt.subplot2grid((1, 2), (0, 1))
    wind_speed(cubes_a)
    plt.title(r'Analysis $\mathbf{u}$')

    plt.savefig(plotdir + 'iop8_winds.pdf')
    # plt.show()

    return


def wind_speed(cubes):
    u = convert.calc('x_wind', cubes, levels=levels)[0]
    v = convert.calc('y_wind', cubes, levels=levels)[0]
    w = convert.calc('upward_air_velocity', cubes, levels=levels)[0]
    wind = (u.data**2 + v.data**2 + w.data**2)**0.5
    wind = u.copy(data=wind)

    theta = convert.calc('air_potential_temperature', cubes,
                         levels=levels)[0]

    print(wind.data.max(), wind.data.min())
    plot.contourf(wind, np.linspace(0, 50, 11), cmap='magma_r')
    plot.overlay_winds(u, v, 33, 57, scale=1500)

    return


if __name__ == '__main__':
    forecast = case_studies.iop8.copy()
    cubes = forecast.set_lead_time(hours=24)
    main(cubes)
