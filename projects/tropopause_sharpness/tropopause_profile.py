"""PV and tracers relative to the tropopause at 24-hour lead time
"""


import matplotlib.pyplot as plt
import iris
from mymodule.plot.util import multilabel, legend
from systematic_forecasts import second_analysis
from myscripts.projects.tropopause_sharpness import plotdir


def main():
    # Initialise the plot
    fig = plt.figure(figsize=(18, 12))
    # Add subfigures
    for n in range(2):
        for m in range(3):
            plt.subplot2grid((2, 3), (n, m))

    # Plot composites
    tropopause_profile('distance_from_dynamical_tropopause', 1, fig)

    # Add faint lines for q_adv
    #tropopause_profile('distance_from_advection_only_tropopause', 0.25, fig)
    for n, subdomain in enumerate(['ridges', 'troughs']):
        coord = 'distance_from_advection_only_tropopause'
        alpha = 0.3
        cubes = second_analysis.get_data(coord, subdomain)
        m = 1
        mapping = second_analysis.mappings['pv_main']
        mapping = {k: mapping[k] for k in ('dynamics_tracer_inconsistency',
                                           'sum_of_physics_pv_tracers')}
        ax = fig.axes[n * 3 + m]
        profile_multi(cubes, coord, ax, mapping, alpha)

    fig.subplots_adjust(bottom=0.2)

    # Set labels and limits on plots
    for n, subdomain in enumerate(['ridges', 'troughs']):
        for m in range(3):
            ax = fig.axes[n * 3 + m]
            # X-axis - Same for all plots

            if m == 0:
                ax.set_xlim(-0.5, 0.2)
                ax.set_xticks([-0.4, -0.2, 0, 0.2])
            else:
                ax.set_xlim(-0.2, 0.3)
                ax.set_xticks([-0.2, -0.1, 0, 0.1,  0.2, 0.3])

            if n == 0:

                ax.get_xaxis().set_ticklabels([])

                # Set Titles
                if m == 0:
                    ax.set_title(
                        'Forecast minus analysis')
                elif m == 1:
                    ax.set_title('PV budget')
                elif m == 2:
                    ax.set_title('Physics PV tracers')

            else:
                legend(ax, key=second_analysis.get_idx,
                            loc='best', ncol=2, bbox_to_anchor=(1.0, -0.2),
                            fontsize=25)
                if m == 1:
                    ax.set_xlabel('PV (PVU)')
            # Y-axis - Same for all plots
            ax.set_ylim(-2, 2)
            ax.set_yticks([-2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2])
            if m != 0:
                ax.get_yaxis().set_ticklabels([])

            multilabel(ax, n * 3 + m)

    fig.text(0.075, 0.55, 'Vertical distance from tropopause (km)',
             va='center', rotation='vertical', fontsize=20)
    fig.text(0.05, 0.75, 'Ridges',
             va='center', rotation='vertical', fontsize=20)
    fig.text(0.05, 0.35, 'Troughs',
             va='center', rotation='vertical', fontsize=20)

    plt.savefig(plotdir + 'tropopause_profile_new.pdf')
    # plt.show()

    return


def tropopause_profile(coord, alpha, fig):
    # Columns are Ridges and troughs
    for n, subdomain in enumerate(['ridges', 'troughs']):
        cubes = second_analysis.get_data(coord, subdomain)

        # Rows are for different mappings
        for m, mapping in enumerate(['pv_full', 'pv_main', 'pv_phys']):
            mapping = second_analysis.mappings[mapping]
            ax = fig.axes[n * 3 + m]

            if m == 0:
                # First column is forecast error
                profile_error(cubes, coord, ax, mapping, alpha)
            else:
                # Columns 2 and 3 show full accumulation
                profile_multi(cubes, coord, ax, mapping, alpha)

    return


def profile_multi(cubes, coord, axis, mapping, alpha):
    for variable in mapping:
        # Extract the plot styles for the variable
        c = mapping[variable]
        # Load the cube
        cube = cubes.extract(variable)[0]
        cube = cube.extract(iris.Constraint(forecast_lead_time=24))

        # Plot tropopause gradient vs lead time
        mean, std_err = second_analysis.extract_statistics(
            cube, 'forecast_index')
        axis.errorbar(mean.data, mean.coord(coord).points * 1e-3,
                      xerr=std_err.data, linestyle=c.linestyle,
                      color=c.color, label=c.symbol, alpha=alpha)
        axis.axhline(color='k')
        axis.axvline(color='k')

    return


def profile_error(cubes, coord, axis, mapping, alpha):
    for variable in mapping:
        # Extract the plot styles for the variable
        c = mapping[variable]
        # Load the cube
        cube = cubes.extract(variable)[0]

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

        axis.errorbar(mean.data, mean.coord(coord).points * 1e-3,
                      xerr=std_err.data, linestyle=c.linestyle,
                      color=c.color, label=c.symbol, alpha=alpha)

        axis.axvline(color='k')
        axis.axhline(color='k')

    return


if __name__ == '__main__':
    main()
