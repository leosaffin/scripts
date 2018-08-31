"""Cross sections of theta_e at different points along a front
"""

from string import ascii_uppercase
import numpy as np
import matplotlib.pyplot as plt
import iris.plot as iplt
from mymodule import convert, grid, plot
from myscripts.models.um import case_studies
from myscripts.projects.thesis.fronts import plotdir
from myscripts.projects.thesis.bl.low_level_cancellation_cs import cs_cube

# Contour levels to plot variables
levels = ('air_pressure', [90000])
plevs = np.linspace(950, 1050, 11)

rh_levs = [0.8]

# Points for IOP5
points = [(-8, 8, 9, 7), (-10, 6, 4, 2), (-12, 4, -1, -3)]
filename = plotdir + 'iop5_24h_front_cs.pdf'
theta_levs = np.linspace(280, 320, 9)

# Points for IOP8
#points = [(-6, 2, 10, 2), (-6, 2, 2, 10), (-12, -6, 5, -5)]
#filename = plotdir + 'iop8_24h_front_cs.pdf'
#theta_levs = np.linspace(275, 315, 9)

nrows, ncols = 2, 2


def main(cubes, **kwargs):
    # Pre-calculate parameters on every plot
    mslp = convert.calc('air_pressure_at_sea_level', cubes)
    mslp.convert_units('hPa')
    theta = convert.calc('equivalent_potential_temperature', cubes,
                         levels=levels)[0]
    rh = convert.calc('relative_humidity', cubes)

    fig = plt.figure(figsize=(18, 15))

    lon, lat = grid.true_coords(theta)
    lonmask = np.logical_or(lon < -15, lon > 5)
    latmask = np.logical_or(lat < 47.5, lat > 62.5)
    areamask = np.logical_or(lonmask, latmask)

    # Plot overview
    ax1 = plt.subplot2grid((2, 2), (0, 0))
    iplt.contourf(theta, theta_levs, cmap='coolwarm', extend='both')
    plot._add_map()
    cs = iplt.contour(mslp, plevs, colors='k', linewidths=2)
    plt.clabel(cs, fmt='%1.0f')
    mask = theta.copy(data=areamask.astype(int))
    iplt.contour(mask, [0.5], colors='k', linestyles='--')
    count = 0
    for n, (xs, xf, ys, yf) in enumerate(points, start=1):
        # Label the cross section points
        plt.plot([xs, xf], [ys, yf], '-kx')
        plt.text(xs, ys, ascii_uppercase[count], color='k', fontsize=20)
        count += 1
        plt.text(xf, yf, ascii_uppercase[count], color='k', fontsize=20)
        count += 1
    plot.multilabel(plt.gca(), 0)

    theta = convert.calc('equivalent_potential_temperature', cubes)
    # Plot cross sections
    titles = ['AB', 'CD', 'EF']
    coords = ['grid_longitude', 'altitude']
    for n, (xs, xf, ys, yf) in enumerate(points, start=1):

        row = n / ncols
        col = n - row * ncols
        ax = plt.subplot2grid((nrows, ncols), (row, col))
        theta_cs = cs_cube(theta, xs, xf, ys, yf)
        rh_cs = cs_cube(rh, xs, xf, ys, yf)
        im = iplt.contourf(theta_cs, theta_levs, coords=coords,
                           cmap='coolwarm', extend='both')
        iplt.contour(rh_cs, rh_levs, coords=coords, colors='w')
        iplt.contourf(rh_cs, [0.8, 2], coords=coords,
                      colors='None', hatches=['.'])
        ax.set_ylim(0, 7)

        if xs > xf:
            ax.invert_xaxis()
            plot.multilabel(ax, n, xreversed=True)
        else:
            plot.multilabel(ax, n)

        ax.set_title(titles[n - 1])
        ax.set_ylabel('Height (km)')
        ax.set_xlabel('Grid Longitude')

    # Add colorbar at bottom of figure
    cbar = plt.colorbar(im, ax=fig.axes, orientation='horizontal',
                        fraction=0.05, spacing='proportional')
    cbar.set_label('PVU')

    fig.savefig(filename)
    plt.show()


if __name__ == '__main__':
    forecast = case_studies.iop5b.copy()
    cubes = forecast.set_lead_time(hours=24)
    main(cubes, vmin=-10, vmax=10, cmap='coolwarm')
