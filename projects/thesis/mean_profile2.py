import matplotlib.pyplot as plt
import iris
from irise import plot
from irise.plot.util import multilabel, legend
from systematic_forecasts import second_analysis
from myscripts.projects.thesis import plotdir


coord = 'altitude'
mappings = ['pv_full', 'pv_main', 'pv_phys']
ncols = len(mappings)

title = ['Forecast minus analysis',
         'PV budget',
         'Physics PV tracers']

xlabel = 'PV (PVU)'
ylabel = 'Height (km)'
#ylabel = 'Vertical distance from boundary layer top (km)'

#xlims = [(0.1, 0.8), (-0.5, 0.5), (-0.5, 0.5)]
xlims = [(-0.2, 0.2), (-0.2, 0.2), (-0.2, 0.2)]
#ylim = (-1, 1)
ylim = (0, 15)


def tropopause_profile():

    # Initialise the plot
    fig = plt.figure(figsize=(18, 15))

    # Loop over mappings
    for n, mapping in enumerate(mappings):
        mapping = second_analysis.mappings[mapping]
        for m, domain in enumerate(['ridges', 'troughs']):
            cubes = second_analysis.get_data(coord, domain)
            ax = plt.subplot2grid((2, ncols), (m, n))

            if n == 0:
                profile_error(cubes, ax, mapping, coord)
            else:
                profile_multi(cubes, ax, mapping, coord)

            plt.title(title[n])
            ax.set_xlim(*xlims[n])
            ax.set_ylim(*ylim)
            legend(ax, key=second_analysis.get_idx,
                        loc='best', ncol=2, bbox_to_anchor=(0.9, -0.2))

            if n == 0:
                ax.set_ylabel(ylabel)

            else:
                ax.set_ylabel('')
                ax.get_yaxis().set_ticklabels([])

            if n == 1:
                ax.set_xlabel(xlabel)
            else:
                ax.set_xlabel('')

            plt.title('')
            plt.axvline(color='k')
            plt.axhline(color='k')

        # if coord == 'air_pressure':
        #    ax.set_ylim(ax.get_ylim()[::-1])

    for n, ax in enumerate(fig.axes):
        multilabel(ax, n)

    fig.subplots_adjust(bottom=0.4)

    #plt.savefig(plotdir + 'ch7_low/height_profile.pdf')

    plt.show()

    return


def profile_multi(cubes, axis, mapping, coord):
    for variable in mapping:
        # Extract the plot styles for the variable
        c = mapping[variable]
        # Load the cube
        cube = cubes.extract(variable)[0]
        cube = cube.extract(iris.Constraint(forecast_lead_time=24))
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
        analysis = cube[1:].extract(iris.Constraint(forecast_lead_time=6))

        # 24h lead time (exclude last forecast)
        forecast = cube[:-1].extract(iris.Constraint(forecast_lead_time=30))

        # Take the difference between the 48h forecast and the 24h forecast for
        # the same verification time
        diff = forecast.data - analysis.data
        diff = forecast.copy(data=diff)

        # Take the mean difference
        mean, std_err = second_analysis.extract_statistics(
            diff, 'forecast_index')

        plot.errorbar(mean, mean.coord(coord), xerr=std_err,
                      linestyle=c.linestyle, color=c.color, label=c.symbol)

    return


def nice_units(cube, coord):
    # Nice units
    if cube.coord(coord).units == 'Pa':
        cube.coord(coord).convert_units('hPa')
    elif cube.coord(coord).units == 'm':
        cube.coord(coord).convert_units('km')


if __name__ == '__main__':
    tropopause_profile()
