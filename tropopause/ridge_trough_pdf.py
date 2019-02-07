from datetime import timedelta as dt
import numpy as np
import matplotlib.pyplot as plt
from irise import convert, grid
from irise.detection import rossby_waves
from myscripts.models.um import case_studies


def main(cubes, xbins, ybins, xlabel, ylabel, **kwargs):
    """
    """
    # Load variables
    thetapv2 = convert.calc('air_potential_temperature', cubes,
                            levels=('ertel_potential_vorticity', [2]))[0]
    z_bl = convert.calc('atmosphere_boundary_layer_thickness', cubes)

    # Create a ridge trough mask
    theta_b = rossby_waves.nae_map(grid.get_datetime(thetapv2)[0])
    dtheta = thetapv2.data - theta_b.data

    # Calculate the pdf for ridges/troughs vs bl height
    colourplot(z_bl.data.flatten(), dtheta.flatten(), xbins, ybins, **kwargs)

    # Calculate the individual pdf for bl height
    lineplot(z_bl.data, xbins, xlabel)

    # Calculate the individual pdf for ridges/troughs
    lineplot(dtheta, ybins, ylabel)

    plt.show()


def colourplot(xdata, ydata, xbins, ybins, **kwargs):
    H, x, y = np.histogram2d(xdata, ydata, bins=(xbins, ybins))
    H = np.log(H)
    plt.pcolormesh(x, y, H.transpose(), **kwargs)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.colorbar()
    plt.ylim(y[0], y[-1])


def lineplot(a, bins, label):
    H, x = np.histogram(a, bins=bins)
    plt.figure()
    plt.bar(x[:-1], H, width=x[1] - x[0], color='k', edgecolor='w')
    plt.xlabel(label)


if __name__ == '__main__':
    forecast = case_studies.iop5()
    cubes = forecast.set_lead_time(dt(hours=36))
    xbins = np.linspace(0, 4000, 9)
    xlabel = 'Boundary Layer Height (m)'
    ybins = np.linspace(-50, 50, 21)
    ylabel = r'$\theta - \theta_b$ (K)'
    main(cubes, xbins, ybins, xlabel, ylabel, vmin=0, vmax=10, cmap='plasma')
