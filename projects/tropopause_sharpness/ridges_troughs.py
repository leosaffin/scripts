"""Demonstration of ridge/trough diagnostic
"""

import datetime
import numpy as np
import matplotlib.pyplot as plt
import iris
import iris.plot as iplt
from mymodule import convert, grid, interpolate, plot, user_variables
from mymodule.detection import rossby_waves
from scripts import case_studies
from scripts.projects.tropopause_sharpness import plotdir

path = user_variables.datadir

start_time = datetime.datetime(2013, 11, 1)
end_time = datetime.datetime(2014, 2, 1)
forecast_period = iris.Constraint(
    time=lambda t: t >= start_time and t < end_time)

nae_min, nae_max = 26.43, 70.27
theta_max = 340
levels = np.linspace(280, theta_max, 13)


def main(cubes):
    """Plot contours of theta on PV2 coloured by whether they are ridges or
    troughs
    """
    # Initialise the figure
    fig = plt.figure(figsize=(18, 15))

    # Background state eqlats vs theta
    ax = plt.subplot2grid((2, 2), (0, 0))
    background_eqlats()
    plot.multilabel(ax, 0)

    # Background state theta vs latitude vs time
    ax = plt.subplot2grid((2, 2), (0, 1))
    background_theta()
    plot.multilabel(ax, 1)

    # Forecast theta on tropopause
    ax = plt.subplot2grid((2, 2), (1, 0))
    theta, lon, lat = forecast_theta(cubes)
    #plot.multilabel(ax, 2)

    # Anomaly of theta on tropopause
    ax = plt.subplot2grid((2, 2), (1, 1))
    theta_anomaly(theta, lon, lat)
    #plot.multilabel(ax, 3)

    plt.savefig(plotdir + 'ridges_troughs.pdf')
    plt.show()

    return


def background_eqlats():
    """Plot the background state equivalent latitude as a function of theta
    """
    # Load the Background State Equivalent Latitudes
    eqlats = rossby_waves.eqlats

    # Use only the 3-month forecast period
    with iris.FUTURE.context(cell_datetime_objects=True):
        eqlats = eqlats.extract(forecast_period)[0]

    # On 2-PVU surface
    eqlats = interpolate.main(eqlats, ertel_potential_vorticity=2)

    # Extract coordinate for y-axis
    theta = eqlats[0].coord('potential_temperature')

    # Plot each day as a background grey
    for n in range(eqlats.shape[0]):
        iplt.plot(eqlats[n], theta, color=(0.5, 0.5, 0.5))

    # Plot 1st of each month in other colours
    day_1 = iris.Constraint(
        time=lambda t: t.point.day == 1 and t.point.hour == 0)
    with iris.FUTURE.context(cell_datetime_objects=True):
        eqlat_sub = eqlats.extract(day_1)
    for n, c in enumerate(['c', 'y', 'm']):
        iplt.plot(eqlat_sub[n], theta, color=c,
                  label=str(grid.get_datetime(eqlat_sub[n])[0])[0:10])
    plt.xlim(nae_min, nae_max)
    plt.ylim(285, 375)
    plt.axhline(theta_max, color='k', linestyle='--')
    plt.legend(loc='best')
    plt.xlabel(r'$\phi_e$', fontsize=24)
    plt.ylabel(r'$\theta$', fontsize=24)

    plt.title(r'$\phi_e (\theta, q=2)$')

    return


def background_theta():
    # Load the Background State theta
    theta = rossby_waves.theta_pv2_LAT

    # Use only the 3-month forecast period
    with iris.FUTURE.context(cell_datetime_objects=True):
        theta = theta.extract(forecast_period)[0]

    plt.contourf(
        theta.coord('time').points, theta.coord('latitude').points,
        theta.data.transpose(), levels)
    cb = plt.colorbar(orientation='horizontal')
    cb.set_label('K')
    plt.ylim(nae_min, nae_max)
    plt.xlabel('Time (Days Since 2013/11/01)')
    plt.ylabel(r'$\phi$', fontsize=24)
    plt.title(r'$\theta_b (\phi, q=2, t)$')

    return


def forecast_theta(cubes):
    theta = convert.calc('air_potential_temperature', cubes,
                         levels=('ertel_potential_vorticity', [2]))[0]

    theta.data = np.ma.masked_where(theta.data > theta_max, theta.data)
    iplt.contourf(theta, levels)
    plt.gca().coastlines()

    cb = plt.colorbar(orientation='horizontal')
    cb.set_label('K')
    plt.title('(c)'.ljust(30) + r'$\theta (\lambda, \phi, q=2)$'.ljust(60))

    lon, lat = grid.true_coords(theta)
    lon = theta.copy(data=lon)
    lat = theta.copy(data=lat)

    add_gridlines(lon, lat)

    return theta, lon, lat


def theta_anomaly(theta, lon, lat):
    """
    """
    theta_b = rossby_waves.nae_map(grid.get_datetime(theta)[0])
    theta_anomaly = theta.data - theta_b.data
    theta_anomaly = theta.copy(data=theta_anomaly)

    iplt.contourf(theta_anomaly, levels - 310, cmap='coolwarm', extend='both')
    cb = plt.colorbar(orientation='horizontal')
    cb.set_label('K')
    iplt.contour(theta_anomaly, [0], colors='k')
    plt.gca().coastlines()
    plt.title(
        '(d)'.ljust(30) + r'$\theta^{\prime} (\lambda, \phi, q=2)$'.ljust(65))

    add_gridlines(lon, lat)

    return


def add_gridlines(lon, lat):
    iplt.contour(lon, np.linspace(-180, 180, 37), colors='k', linestyles=':',
                 linewidths=1)
    iplt.contour(lat, np.linspace(-90, 90, 19), colors='k', linestyles=':',
                 linewidths=1)

    kwargs = {'va': 'center', 'ha': 'center', 'fontsize': 20}
    plt.text(2, -21, r'$0^{\circ}$', **kwargs)
    plt.text(-16, -21, r'$20^{\circ}$', **kwargs)
    plt.text(20, -21, r'$20^{\circ}$', **kwargs)

    plt.text(-35, 10, r'$50^{\circ}$', **kwargs)
    plt.text(-35, -2, r'$40^{\circ}$', **kwargs)
    plt.text(-35, -14, r'$30^{\circ}$', **kwargs)

if __name__ == '__main__':
    forecast = case_studies.generate_season_forecast(2013, 11, 1)
    cubes = forecast.set_lead_time(hours=24)
    main(cubes)
