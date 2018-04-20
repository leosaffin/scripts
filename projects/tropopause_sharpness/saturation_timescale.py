"""Parameters for exponential decay of q_adv contrast
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import iris
from iris.analysis import MEAN
from scipy.optimize import curve_fit
from systematic_forecasts import second_analysis
from mymodule import convert, plot
from scripts.projects.tropopause_sharpness import plotdir


variable = 'advection_only_pv'
coords = [('distance_from_dynamical_tropopause', 'k'),
          ('distance_from_advection_only_tropopause', 'grey')]

subdomains = [('ridges', '-'), ('troughs', '--')]


def func(t, tau, dpv_0, dpv_inf):
    """Function describing exponential decay of PV gradient to a finite value

    Args:
        t (float, np.array): Lead time

        tau (float): Timescale

        dpv_0 (float): Initial gradient

        dpv_inf (float): Decay gradient

    Returns:
        Float or np.array of the fit depending on the input x
    """
    return (dpv_0 - dpv_inf) * np.exp(-t / tau) + dpv_inf


def make_table():
    for coord in (['distance_from_dynamical_tropopause',
                   'distance_from_advection_only_tropopause']):
        for subdomain in (['ridges', 'troughs']):
            cubes = second_analysis.get_data(coord, subdomain)
            pv = convert.calc(variable, cubes)[:, 1:]
            x, y, dy = pv_contrast(pv, coord, 1000)
            popt, pcov, rmse = fit_curve(x, y, dy)
            print(subdomain.capitalize() + ' & ' + str(round(popt[0], 1)) +
                                           ' & ' + str(round(popt[1], 3)) +
                                           ' & ' + str(round(popt[2], 3)) +
                                           ' & ' + str(round(rmse, 3)))
    return


def compare_fits():
    # Initialise the plot
    fig = plt.figure(figsize=(18, 15))

    # Rows are different depths
    for n, dz in enumerate([1000, 2000]):
        # Columns are Ridges and troughs
        for m, subdomain in enumerate(['ridges', 'troughs']):
            ax = plt.subplot2grid((2, 2), (n, m))
            for coord, color in (
                [('distance_from_dynamical_tropopause', 'k'),
                 ('distance_from_advection_only_tropopause', (0.5, 0.5, 0.5))]):
                if n == 0:
                    depth_average(coord, subdomain, dz, color=color)
                    plt.title(subdomain.capitalize())
                else:
                    finite_difference(
                        coord, subdomain, dz, color=color)

    # Add letters to 6-panel figure
    fig.text(0.125, 0.91, '(a)')
    fig.text(0.55, 0.91, '(b)')
    fig.text(0.125, 0.48, '(c)')
    fig.text(0.55, 0.48, '(d)')
    fig.text(0.05, 0.5, r'$\Delta q_{adv}$ (PVU km$^{-1}$)',
             va='center', rotation='vertical')
    fig.text(0.5, 0.05, 'Forecast Lead Time (hours)', ha='center')

    plt.show()

    return


def _single_fit(coord, subdomain, dz, function, **kwargs):
    cubes = second_analysis.get_data(coord, subdomain)
    pv = convert.calc(variable, cubes)
    x, y, dy = function(pv, coord, dz)
    popt, pcov, rmse = fit_curve(x, y, dy)
    print popt, rmse
    plot_fit(x, y, dy, popt, **kwargs)

    return popt, rmse


def finite_difference(coord, subdomain, dz, **kwargs):
    return _single_fit(coord, subdomain, dz, pv_gradient, **kwargs)


def depth_average(coord, subdomain, dz, **kwargs):
    return _single_fit(coord, subdomain, dz, pv_contrast, **kwargs)


def varying_depth(widths, function):
    fig = plt.figure(figsize=(18, 8))
    axes = []
    for n in range(1):
        for m in range(2):
            axes.append(plt.subplot2grid((1, 2), (n, m)))
    for coord, color in coords:
        for subdomain, linestyle in subdomains:
            cubes = second_analysis.get_data(coord, subdomain)
            pv = convert.calc(variable, cubes)

            if subdomain == 'ridges':
                x, y, dy = pv_contrast(pv, coord, 1000)
                popt, pcov, rmse = fit_curve(x, y, dy)
                axes[0].errorbar(x, y, yerr=dy,
                                 linestyle=linestyle, color=color)

            pv = pv[:, 1:]
            if subdomain == 'ridges':
                x2, y, dy = pv_contrast(pv, coord, 1000)
                popt, pcov, rmse = fit_curve(x2, y, dy)
                axes[0].plot(x, func(x, *popt), color=color, linestyle='',
                             marker='o')

            timescale = []
            grad_0 = []
            grad_inf = []
            errors = []
            for dz in widths:
                if dz == 200:
                    x, y, dy = pv_gradient(pv, coord, dz)
                else:
                    x, y, dy = function(pv, coord, dz)
                popt, pcov, rmse = fit_curve(x, y, dy)
                timescale.append(popt[0])
                grad_0.append(popt[1])
                grad_inf.append(popt[2])
                errors.append(rmse)

            grad_0 = np.array(grad_0)
            grad_inf = np.array(grad_inf)
            # axes[2].plot(widths * 1e-3, grad_0,
            #             color=color, linestyle=linestyle, marker='x')
            # axes[3].plot(widths * 1e-3, grad_0 - grad_inf,
            #             color=color, linestyle=linestyle, marker='x')
            axes[1].plot(widths * 1e-3, timescale,
                         color=color, linestyle=linestyle, marker='x')
            # axes[5].plot(widths * 1e-3, errors,
            #             color=color, linestyle=linestyle, marker='x')

    # Set figure labels
    axes[0].set_title(r'$\Delta q_{adv}(t)$ in ridges')
    axes[0].set_xlabel('Forecast Lead Time (hours)')
    axes[0].set_ylabel('PVU')

    axes[1].set_title('Timescale')
    axes[1].set_xlabel(r'$\pm \tilde{z}$ (km)', fontsize=20)
    axes[1].set_ylabel(r'$\tau$ (Hours)')
    """
    axes[2].set_title(r'$\Delta q_{adv}(0)$')
    axes[2].set_xlabel(r'$\pm \tilde{z}$ (km)', fontsize=20)
    axes[2].set_ylabel('PVU')
    #axes[2].set_ylim(0, 5)

    axes[3].set_title(r'$\Delta q_{adv}(0) - \Delta q_{adv}(\infty)$')
    axes[3].set_xlabel(r'$\pm \tilde{z}$ (km)', fontsize=20)
    axes[3].set_ylabel('PVU')
    #axes[3].set_ylim(0, 5)
    """

    for n, axis in enumerate(axes):
        plot.multilabel(axis, n)

    # Create legend table
    fig2 = plt.figure()
    ax = fig2.add_subplot(111)

    lines = []
    for subdomain, linestyle in subdomains:
        for coord, color in coords:
            lines.append(ax.plot([0, 1], [0, 1], linestyle=linestyle,
                                 color=color)[0])

    # create blank rectangle
    extra = Rectangle((0, 0), 1, 1, fc="w", fill=False,
                      edgecolor='none', linewidth=0)

    # Create organized list containing all handles for table. Extra represent
    # empty space
    legend_handle = [extra, extra, extra, extra, lines[0], lines[1],
                     extra, lines[2], lines[3]]
    # Define the labels
    label_column_1 = ["", r"$z(q{=}2)$", r"$z(q_{adv}{=}2)$"]
    label_column_2 = ["Ridges", "", ""]
    label_column_3 = ["Troughs", "", ""]

    # organize labels for table construction
    legend_labels = np.concatenate(
        [label_column_1, label_column_2, label_column_3])

    # Create legend
    axes[1].legend(legend_handle, legend_labels,
                   loc='best', ncol=3, shadow=True, handletextpad=-2)

    fig.savefig(plotdir + 'q_adv_decay_parameters.pdf')
    # plt.show()

    return


def pv_contrast(pv, coord, dz):
    # Stratospheric PV value
    strat = iris.Constraint(**{coord: lambda x: x > 0 and x <= dz})
    pv_s = pv.extract(strat).collapsed(coord, MEAN)

    # Tropospheric PV value
    trop = iris.Constraint(**{coord: lambda x: x < 0 and x >= -dz})
    pv_t = pv.extract(trop).collapsed(coord, MEAN)

    # PV contrast
    dpv = (pv_s - pv_t)  # / (2e-3 * (100 + dz / 2.))
    mean, std_err = second_analysis.extract_statistics(
        dpv, 'forecast_index')

    # Curve parameters
    x = mean.coord('forecast_lead_time').points
    y = mean.data
    dy = std_err.data

    return x, y, dy


def pv_gradient(pv, coord, dz):
    # PV Gradient
    mean, std_err = second_analysis.tropopause_pv_gradient(
        pv, coord=coord, dz=dz)

    # Curve parameters
    x = mean.coord('forecast_lead_time').points
    y = mean.data * 2 * dz * 1e-3
    dy = std_err.data

    return x, y, dy


def fit_curve(x, y, dy):
    # Fit the data to the defined function
    popt, pcov = curve_fit(func, x, y, sigma=dy)

    # Calculate the error in the fit
    y_fit = func(x, *popt)
    rmse = np.mean((y - y_fit) ** 2)**0.5

    return popt, pcov, rmse


def plot_fit(x, y, std_err, popt, **kwargs):
    plt.errorbar(x, y, yerr=std_err, linestyle='-', **kwargs)
    plt.plot(x, func(x, *popt), linestyle='--', **kwargs)

    return


if __name__ == '__main__':
    # compare_fits()
    varying_depth(np.linspace(200, 2000, 10), pv_contrast)
