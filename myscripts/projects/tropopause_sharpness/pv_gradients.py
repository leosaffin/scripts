"""Gradients of PV and tracers as a function of lead time
"""

import matplotlib.pyplot as plt
import iris
from iris.analysis import MEAN
from irise.plot.util import multilabel, legend
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
    pv_gradients('distance_from_dynamical_tropopause', 1, fig)

    # Add faint lines for q_adv
    #pv_gradients('distance_from_advection_only_tropopause', 0.25, fig)
    for n, subdomain in enumerate(['ridges', 'troughs']):
        coord = 'distance_from_advection_only_tropopause'
        alpha = 0.3
        cubes = second_analysis.get_data(coord, subdomain)
        m = 1
        mapping = second_analysis.mappings['pv_main']
        mapping = {k: mapping[k] for k in ('dynamics_tracer_inconsistency',
                                           'sum_of_physics_pv_tracers')}
        ax = fig.axes[n * 3 + m]
        pv_gradients_multi(cubes, coord, ax, mapping, alpha)
    fig.subplots_adjust(bottom=0.2)

    # Set labels and limits on plots
    for n, subdomain in enumerate(['ridges', 'troughs']):
        for m in range(3):
            ax = fig.axes[n * 3 + m]

            # X-axis - Same for both rows
            ax.set_xticks([0, 12, 24, 36, 48, 60])
            if n == 0:
                ax.get_xaxis().set_ticklabels([])

                # Set Titles
                if m == 0:
                    ax.set_title('Forecast')
                elif m == 1:
                    ax.set_title('PV budget')
                elif m == 2:
                    ax.set_title('Physics PV tracers')

            else:
                legend(ax, key=second_analysis.get_idx,
                            loc='best', ncol=2, bbox_to_anchor=(1.0, -0.2),
                            fontsize=25)
                if m == 1:
                    ax.set_xlabel('Forecast lead time (hours)')

            # Y-Axis
            if m == 0:
                # First column custom
                if n == 0:
                    ax.set_ylim(3.0, 3.6)
                else:
                    ax.set_ylim(2.4, 3.0)

            elif m == 1:
                # Columns 2
                ax.set_ylim(-0.1, 0.5)

            else:
                ax.set_ylim(-0.05, 0.25)

            multilabel(ax, n * 3 + m)

    fig.text(0.075, 0.55, 'PV (PVU)', va='center', rotation='vertical',
             fontsize=20)
    fig.text(0.05, 0.75, 'Ridges',
             va='center', rotation='vertical', fontsize=20)
    fig.text(0.05, 0.35, 'Troughs',
             va='center', rotation='vertical', fontsize=20)

    plt.savefig(plotdir + 'pv_gradients_new.pdf')
    plt.show()

    return


def pv_gradients(coord, alpha, fig):
    # Rows are Ridges and troughs
    for n, subdomain in enumerate(['ridges', 'troughs']):
        cubes = second_analysis.get_data(coord, subdomain)

        # Columns are for different mappings
        for m, mapping in enumerate(['pv_full', 'pv_main', 'pv_phys']):
            mapping = second_analysis.mappings[mapping]
            ax = fig.axes[n * 3 + m]
            pv_gradients_multi(cubes, coord, ax, mapping, alpha)

    return


def pv_gradients_multi(cubes, coord, axis, mapping, alpha):
    for variable in mapping:
        # Extract the plot styles for the variable
        c = mapping[variable]
        # Load the cube
        cube = cubes.extract(variable)[0][1:]
        # Plot tropopause gradient vs lead time
        pv_s = cube.extract(
            iris.Constraint(**{coord: lambda x: x > 0 and x <= 1000}))
        pv_s = pv_s.collapsed(coord, MEAN)
        pv_t = cube.extract(
            iris.Constraint(**{coord: lambda x: x < 0 and x >= -1000}))
        pv_t = pv_t.collapsed(coord, MEAN)

        dpv = (pv_s - pv_t)
        mean, std_err = second_analysis.extract_statistics(
            dpv, 'forecast_index')
        # mean, std_err = second_analysis.tropopause_pv_gradient(
        #    cube, coord=coord, dz=400)
        axis.errorbar(mean.coord('forecast_lead_time').points, mean.data,
                      yerr=std_err.data, linestyle=c.linestyle,
                      color=c.color, label=c.symbol, alpha=alpha)
        axis.axhline(color='k')

    return


if __name__ == '__main__':
    main()
