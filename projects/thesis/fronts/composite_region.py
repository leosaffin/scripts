"""Composite PV tracers in warm and cold sectors defined in custom region
"""

import numpy as np
import matplotlib.pyplot as plt
import iris.plot as iplt
import iris.quickplot as qplt
from mymodule import convert, diagnostic, interpolate, grid, plot
from myscripts import case_studies
from systematic_forecasts import second_analysis
from myscripts.projects.thesis.fronts import plotdir


mappings = [second_analysis.full, second_analysis.budget,
            second_analysis.tracers]
#mappings = [second_analysis.humidity, second_analysis.thermal]

names = [name for m in mappings for name in m.keys()]
ncol = len(mappings)

levels = np.linspace(487.5, 1012.5, 22)


slices = slice(70, -20), slice(120, -100)

theta_front = 300


def main(cubes):
    theta = convert.calc('equivalent_potential_temperature', cubes)
    P = convert.calc('air_pressure', cubes)
    P.convert_units('hPa')
    mass = convert.calc('mass', cubes)

    lon, lat = grid.true_coords(theta)
    lonmask = np.logical_or(lon < -15, lon > 5)
    latmask = np.logical_or(lat < 47.5, lat > 62.5)
    areamask = np.logical_or(lonmask, latmask)

    masks = [np.logical_or(theta.data < theta_front, areamask),
             np.logical_or(theta.data > theta_front, areamask)]

    #overview(cubes, areamask)
    #plt.savefig(plotdir + 'composite_iop8_24h_overview_750hpa.pdf')
    # plt.show()

    z_cold, z_warm = bl_heights(cubes, theta, areamask)

    # Initialise the plot
    fig = plt.figure(figsize=(18, 12))

    diags = convert.calc(names, cubes)
    masses = []
    # Rows are different masks
    for n, mask in enumerate(masks):
        means = diagnostic.averaged_over(diags, levels, P, mass, mask)
        masses.append(convert.calc('mass', means))
        # Columns are for different mappings
        for m, mapping in enumerate(mappings):
            ax = plt.subplot2grid((2, ncol), (n, m))
            composite(means, ax, mapping, mass, P)
            add_trimmings(ax, n, m)
            if m == 0:
                ax.set_xlim(0.1, 1.3)
            elif m == 1:
                ax.set_xlim(-0.6, 0.6)
            else:
                ax.set_xlim(-1, 1)

            plot.multilabel(ax, 3 * n + m, yreversed=True, fontsize=25)

            if n == 0:
                plt.axhline(z_cold, color='k', linestyle='--')
            elif n == 1:
                plt.axhline(z_warm, color='k', linestyle='--')
    add_figlabels(fig)
    fig.savefig(plotdir + 'composite_iop5_24h.pdf')

    plt.figure()
    for mass in masses:
        qplt.plot(mass, mass.coord('air_pressure'))
        ax.set_ylim(950, 500)

    plt.show()

    return


def overview(cubes, areamask):
    theta_P = convert.calc('equivalent_potential_temperature', cubes,
                           levels=('air_pressure', [75000]))[0]
    plot.contourf(theta_P[slices], np.linspace(280, 320, 17), extend='both')
    mask = theta_P.copy(data=areamask.astype(int))
    iplt.contour(mask[slices], [0.5], colors='k', linestyles='--')
    iplt.contour(theta_P[slices], [theta_front], colors='k')

    return


def composite(cubes, ax, mapping, mass, P):
    for variable in mapping:
        # Extract the plot styles for the variable
        c = mapping[variable]
        # Load the cube
        cube = cubes.extract(variable)[0]

        iplt.plot(cube, cube.coord('air_pressure'),
                  color=c.color, linestyle=c.linestyle, label=c.symbol)

    return


def bl_heights(cubes, theta, areamask):
    # Interpolate theta to bl height
    z_bl = convert.calc('boundary_layer_height', cubes)
    theta_bl = interpolate.to_level(theta, altitude=z_bl.data[None, :, :])[0]

    # Theta on bl defines cold and warm sectors
    cold_mask = np.logical_or(areamask, theta_bl.data > 300)
    warm_mask = np.logical_or(areamask, theta_bl.data < 300)

    # Calculate average bl height in cold and warm sectors
    p = convert.calc('air_pressure', cubes,
                     levels=('altitude', z_bl.data[None, :, :]))[0]
    p.convert_units('hPa')
    cold_z = np.ma.masked_where(cold_mask, p.data)
    warm_z = np.ma.masked_where(warm_mask, p.data)

    return cold_z.mean(), warm_z.mean()


def add_trimmings(ax, n, m):
    """
    # Set Titles
    if n == 0:
        ax.get_xaxis().set_ticklabels([])
    if m == 0:
        ax.set_title('Forecast')
        ax.set_xlim(0, 1.25)
    elif m == 1:
        ax.set_title('PV budget')
        plt.axvline(color='k')
        ax.set_xlim(-0.6, 0.6)
        ax.get_yaxis().set_ticklabels([])
        if n == 1:
            ax.set_xlabel('PV (PVU)')
    elif m == 2:
        ax.set_title('Physics PV tracers')
        plt.axvline(color='k')
        ax.set_xlim(-1, 1)
        ax.get_yaxis().set_ticklabels([])
    """

    # plt.gca().invert_yaxis()
    plt.axvline(color='k')
    ax.set_ylim(950, 500)
    if n == 1:
        plot.legend(ax, key=second_analysis.get_idx,
                    loc='best', ncol=2, bbox_to_anchor=(0.9, -0.2),
                    fontsize=25)

    return


def add_figlabels(fig):
    fig.text(0.075, 0.55, 'Pressure (hPa)',
             va='center', rotation='vertical', fontsize=25)
    fig.text(0.05, 0.75, 'Warm',
             va='center', rotation='vertical', fontsize=25)
    fig.text(0.05, 0.35, 'Cold',
             va='center', rotation='vertical', fontsize=25)
    fig.subplots_adjust(bottom=0.2)
    return


if __name__ == '__main__':
    forecast = case_studies.iop5b.copy()
    cubes = forecast.set_lead_time(hours=24)
    main(cubes)
