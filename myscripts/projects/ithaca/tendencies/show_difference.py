"""Plot the tendencies at high and low precision and the difference

"""
import matplotlib.pyplot as plt
import iris
import iris.plot as iplt
from irise.plot.util import add_map
from myscripts.models.speedy import datadir, plotdir


def main():
    path = datadir + 'deterministic/'
    variable, units = 'Temperature Tendency', '[K/s]'
    """
    'Temperature Tendency', '[K/s]'
    'Specific Humidity Tendency', '[K/s]'
    'U-Wind Tendency', '[m/s2]'
    'V-Wind Tendency', '[m/s2]'
    """
    scheme = 'Convection'
    """
    Scheme                   |   T   |   q   |  u/v
    -------------------------------------------------
    Convection               |+  2e-4|  -5e-4|
    Large-Scale Condensation |+  2e-4|  -1e-4|
    Short-Wave Radiation     |+  2e-5|       |
    Long-Wave Radiation      |+/-1e-4|       |
    Surface Fluxes           |+/-5e-4|+/-2e-4|+/-1e-3
    Vertical Diffusion       |  -2e-4|  -2e-4|
    """
    name = '{} due to {} {}'.format(variable, scheme, units)

    cs = iris.Constraint(name=name)
    fp = iris.load_cube(path + 'fp_tendencies.nc', cs)
    rp_all = iris.load_cube(path + 'rp_*_tendencies.nc', cs)
    for precision in range(5, 24):
        rp = rp_all.extract(iris.Constraint(precision=precision))

        plot_overview(fp[1, 0], rp[1, 0], vmin=-2e-4, vmax=2e-4, cmap='bwr')
        plt.suptitle('{} compared to {} sbits'.format(fp.name(), precision))

        plt.savefig(plotdir + 'tendency_difference_{}_{}_{}sbits.png'.format(
            variable, scheme, precision).replace(' ', '_'))

        plt.close()
    return


def plot_overview(fp, rp, **kwargs):
    plt.figure(figsize=(12, 9))

    row_title = 2
    row_fig = 8
    col_fig = 8
    row_cbar = 3
    col_cbar = 6

    nrows = row_title + 2*(row_fig + row_cbar)
    ncols = 2*col_fig

    row_fig1 = row_title
    row_cbar1 = row_fig1 + row_fig
    row_fig2 = row_cbar1 + row_cbar
    row_cbar2 = row_fig2 + row_fig

    col_fig1 = 0
    col_fig2 = col_fig1 + col_fig
    col_fig3 = col_fig1 + int(col_fig/2)
    col_cbars = int((ncols - col_fig1 - col_cbar)/2)

    plt.subplot2grid((nrows, ncols), (row_fig1, col_fig1), rowspan=row_fig, colspan=col_fig)
    im = iplt.pcolormesh(fp, **kwargs)
    plt.title('Full Precision')
    add_map()

    plt.subplot2grid((nrows, ncols), (row_fig1, col_fig2), rowspan=row_fig, colspan=col_fig)
    im = iplt.pcolormesh(rp, **kwargs)
    plt.title('Reduced Precision')
    add_map()

    ax = plt.subplot2grid((nrows, ncols), (row_cbar1, col_cbars), rowspan=row_cbar, colspan=col_cbar)
    cbar = plt.colorbar(im, cax=ax, orientation='horizontal')

    plt.subplot2grid((nrows, ncols), (row_fig2, col_fig3), rowspan=row_fig, colspan=col_fig)
    vmax = 0.1*max(abs(kwargs['vmin']), abs(kwargs['vmax']))
    im = iplt.pcolormesh(rp-fp, vmin=-vmax, vmax=vmax, cmap='bwr')
    plt.title('Difference')
    add_map()

    ax = plt.subplot2grid((nrows, ncols), (row_cbar2, col_cbars), rowspan=row_cbar, colspan=col_cbar)
    cbar = plt.colorbar(im, cax=ax, orientation='horizontal')

    return


if __name__ == '__main__':
    main()
