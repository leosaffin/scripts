import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import iris.plot as iplt
from mymodule import convert, plot
from scripts import case_studies
from systematic_forecasts import second_analysis
from scripts.projects.thesis.bl import plotdir


forecasts = [case_studies.iop5b.copy(), case_studies.iop8.copy()]

types = [('Stable', 'green'),
         ('Stable (with stratocumulus)', 'lime'),
         ('Well-mixed', 'red'),
         ('Well-mixed (with stratocumulus)', 'magenta'),
         ('Cumulus-capped', 'blue'),
         ('Cumulus-capped (with stratocumulus)', 'cyan'),
         ('Shear-driven', 'yellow')]


def bl_categories():
    # Initialise the plot
    fig = plt.figure(figsize=(18, 10))

    for n, forecast in enumerate(forecasts):
        cubes = forecast.set_lead_time(hours=24)

        ax = plt.subplot2grid((1, 2), (0, n))
        if n == 0:
            plt.title('IOP5')
        elif n == 1:
            plt.title('IOP8')

        plot.multilabel(ax, n + 2)

        bl_type = convert.calc('boundary_layer_type', cubes)
        cmap = mpl.colors.ListedColormap([t[1] for t in types])
        iplt.pcolormesh(bl_type, cmap=cmap)

        overlay_pressure(cubes)

        plot._add_map()

    # Add category map legend
    handles = []
    for bl_type, colour in types:
        handles.append(mpatches.Patch(color=colour, label=bl_type))

    ax = fig.axes[1]
    ax.legend(handles=handles, ncol=2, loc='upper_right',
              bbox_to_anchor=(0.95, -0.1))

    fig.subplots_adjust(bottom=0.5)

    plt.savefig(plotdir + 'bl_categories')

    return


def bl_heights(**kwargs):
    # Initialise the plot
    fig = plt.figure(figsize=(18, 10))

    for n, forecast in enumerate(forecasts):
        cubes = forecast.set_lead_time(hours=24)

        ax = plt.subplot2grid((1, 2), (0, n))
        z_bl = convert.calc('atmosphere_boundary_layer_thickness', cubes)
        z_bl.convert_units('km')
        im = iplt.pcolormesh(z_bl, **kwargs)

        cs = overlay_pressure(cubes)
        plt.clabel(cs, fmt='%1.0f')

        plot._add_map()

        if n == 0:
            plt.title('IOP5')
        elif n == 1:
            plt.title('IOP8')

        plot.multilabel(ax, n)

    # Add BL Height colourscale
    cbar = plt.colorbar(im, ax=fig.axes, fraction=0.05,
                        orientation='horizontal', extend='max')
    cbar.set_label('Boundary layer thickness (km)')
    cbar.set_ticks(np.linspace(0, 3, 7))

    plt.savefig(plotdir + 'bl_heights')

    return


def overlay_pressure(cubes, levels=np.linspace(950, 1050, 11), colors='k',
                     linewidths=2):
    mslp = convert.calc('air_pressure_at_sea_level', cubes)
    mslp.convert_units('hPa')
    cs = iplt.contour(mslp, levels, colors=colors, linewidths=linewidths)

    return cs


if __name__ == '__main__':
    bl_categories()
    cmap = mpl.cm.get_cmap('terrain', 6)
    bl_heights(vmin=0, vmax=3, cmap=cmap)
    plt.show()
