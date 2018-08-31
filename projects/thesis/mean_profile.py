import matplotlib.pyplot as plt
import iris
from mymodule import plot
from mymodule.plot.util import multilabel, legend
from systematic_forecasts import second_analysis
from myscripts.projects.thesis import plotdir


def main():
    # Parameters same for all plots
    mappings = ['pv_full', 'pv_main', 'pv_phys']
    domains = ['full', 'sea', 'no_coast']  # , 'ridges', 'troughs']
    title = ['Forecast', 'PV budget', 'Physics PV tracers']
    xlabel = 'PV (PVU)'

    # Ground relative
    """
    coord = 'altitude'
    ylabel = 'Height (km)'
    xlims = [(0, 15), (-0.12, 0.12), (-0.12, 0.12)]
    ylims = (1, 17)
    profile(coord, mappings, domains, title, xlabel, ylabel, xlims, ylims)
    #plt.savefig(plotdir + 'ch7_low/height_profile.pdf')
    plt.show()
    """

    # Tropopause relative
    """
    coord = 'distance_from_dynamical_tropopause'
    ylabel = 'Height (km)'
    xlims = [(-0.5, 0.2), (-0.2, 0.3), (-0.2, 0.3)]
    ylims = (-2, 2)
    profile(coord, mappings, domains, title, xlabel, ylabel, xlims, ylims)
    #plt.savefig(plotdir + 'ch6_tropopause/trop_profile_full.pdf')
    plt.show()
    """

    # BL relative
    coord = 'distance_from_boundary_layer_top'
    ylabel = 'Vertical distance from boundary-layer top (km)'
    xlims = [(0, 0.8), (-0.75, 0.75), (-0.75, 0.75)]
    ylims = (-1, 1)
    profile(coord, mappings, domains, title, xlabel, ylabel, xlims, ylims)
    plt.savefig(plotdir + '../bl_profile_60h.pdf')
    plt.show()

    return


def profile(coord, mappings, domains, title, xlabel, ylabel, xlims, ylims):
    ncols = len(mappings)
    nrows = len(domains)
    # Initialise the plot
    fig = plt.figure(figsize=(18, 25))

    # Loop over mappings
    for m, domain in enumerate(domains):
        cubes = second_analysis.get_data(coord, domain)
        for n, mapping in enumerate(mappings):
            mapping = second_analysis.mappings[mapping]

            ax = plt.subplot2grid((nrows, ncols), (m, n))

            profile_multi(cubes, ax, mapping, coord)

            ax.set_xlim(*xlims[n])
            ax.set_ylim(*ylims)

            if m == 0:
                ax.set_title(title[n])
            else:
                ax.set_title('')

            if m == nrows - 1:
                legend(ax, key=second_analysis.get_idx, loc='upper left',
                            ncol=2, bbox_to_anchor=(0.05, -0.25))
            else:
                ax.get_xaxis().set_ticklabels([])

            if n == 0:
                if m == 1:
                    ax.set_ylabel(ylabel)
                else:
                    ax.set_ylabel('')

            else:
                ax.set_ylabel('')
                ax.get_yaxis().set_ticklabels([])

            if m == nrows - 1 and n == 1:
                ax.set_xlabel(xlabel)
            else:
                ax.set_xlabel('')

            ax.axvline(color='k')
            ax.axhline(color='k')

            if coord == 'air_pressure':
                ax.set_ylim(ax.get_ylim()[::-1])

            multilabel(ax, n + m * ncols)

    fig.subplots_adjust(bottom=0.4)

    return


def profile_multi(cubes, axis, mapping, coord):
    for variable in mapping:
        print(variable)
        # Extract the plot styles for the variable
        c = mapping[variable]
        # Load the cube
        cube = cubes.extract(variable)[0]
        cube = cube.extract(iris.Constraint(forecast_lead_time=60))
        nice_units(cube, coord)

        # Plot tropopause gradient vs lead time
        mean, std_err = second_analysis.extract_statistics(
            cube, 'forecast_index')
        plot.errorbar(mean, mean.coord(coord), xerr=std_err,
                      linestyle=c.linestyle, color=c.color, label=c.symbol)

    return


def profile_error(cubes, axis, mapping, coord):
    for variable in mapping:
        # Extract the plot styles for the variable
        c = mapping[variable]
        # Load the cube
        cube = cubes.extract(variable)[0]
        nice_units(cube, coord)

        # Analysis (exclude first forecast)
        analysis = cube[1:].extract(iris.Constraint(forecast_lead_time=0))

        # 24h lead time (exclude last forecast)
        forecast = cube[:-1].extract(iris.Constraint(forecast_lead_time=24))

        # Take the difference between the 48h forecast and the 24h forecast for
        # the same verification time
        diff = forecast.data - analysis.data
        diff = forecast.copy(data=diff)

        # Take the mean difference
        mean, std_err = second_analysis.extract_statistics(
            diff, 'forecast_index')

        plot.errorbar(mean[1:], mean.coord(coord)[1:], xerr=std_err[1:],
                      linestyle=c.linestyle, color=c.color, label=c.symbol)

    return


def nice_units(cube, coord):
    # Nice units
    if cube.coord(coord).units == 'Pa':
        cube.coord(coord).convert_units('hPa')
    elif cube.coord(coord).units == 'm':
        cube.coord(coord).convert_units('km')


if __name__ == '__main__':
    main()
