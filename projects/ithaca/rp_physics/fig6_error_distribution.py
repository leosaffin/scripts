import warnings

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb

from myscripts.models import speedy
from myscripts.projects.ithaca.tendencies import load_tendency, plotdir


warnings.filterwarnings("ignore")


def main():
    # schemes = ['All Parametrizations']
    # schemes = ['Surface Fluxes', 'Vertical Diffusion', 'Convection']
    schemes = ['Condensation', 'Long-Wave Radiation', 'Short-Wave Radiation']
    name = 'other_parametrizations'

    for variable, units in [('Temperature', 'K/s'),
                            ('Specific Humidity', 's$^{-1}$'),
                            ('Zonal Velocity', 'm/s$^{-2}$'),
                            ('Meridional Velocity', 'm/s$^{-2}$'),
                            ]:
        for sigma in speedy.sigma_levels:
            for precision in [6]:
                make_plot(variable, units, sigma, precision, schemes)

                plt.gcf().set_size_inches(16, 9)

                plt.savefig(plotdir + 'error_distribution/' +
                            '{}_{}_l{}_{}sbits.png'.format(
                                variable.lower().replace(' ', '_'),
                                name,
                                speedy.sigma_levels.index(sigma),
                                precision))

                plt.close()

    return


def make_plot(variable, units, sigma, reduced_precision, schemes):
    fp = load_tendency(variable=variable, sigma=sigma, precision=52)
    tendency = np.abs(fp.data).flatten()
    print(tendency.min(), tendency.max())

    jg = sb.JointGrid(None, None)
    bins = 10. ** np.arange(-12, -2, 0.5)
    bin_widths = [bins[n + 1] - bins[n] for n in range(len(bins) - 1)]

    jg.ax_joint.plot(bins, bins, '--k')

    hists = []
    for scheme in schemes:
        rp = load_tendency(variable=variable,
                           rp_scheme=scheme.lower().replace(' ', '_').replace('-', '_'),
                           sigma=sigma, precision=reduced_precision)
        error = np.abs(rp.data - fp.data).flatten()

        print(schemes, error.min(), error.max())

        plp = speedy.physics_schemes[scheme]

        hist = draw_distribution(tendency, error, jg, plp, bins, bin_widths)
        hists.append(hist)

    for hist, scheme in zip(hists, schemes):
        plp = speedy.physics_schemes[scheme]
        jg.ax_marg_y.barh(bins[:-1], hist, height=bin_widths, align='edge', edgecolor=plp.color, fill=False)

    jg.ax_joint.set_xscale('log')
    jg.ax_joint.set_yscale('log')
    jg.ax_joint.set_xlim(1e-9, 5e-4)
    jg.ax_joint.set_ylim(1e-12, 5e-4)
    jg.ax_joint.set_xlabel('Double-Precision Tendency [{}]'.format(units), fontsize='x-large')
    jg.ax_joint.set_ylabel('Error in Tendency [{}]'.format(units), fontsize='x-large')

    return


def draw_distribution(tendency, error, jg, plp, bins, bin_widths):
    jg.ax_joint.scatter(tendency, error, c=plp.color, linewidths=1, alpha=0.5)

    hist = np.histogram(tendency, bins)[0]
    jg.ax_marg_x.bar(bins[:-1], hist, width=bin_widths, align='edge', color='k')

    hist = np.histogram(error, bins)[0]
    jg.ax_marg_y.barh(bins[:-1], hist, height=bin_widths, align='edge', color=plp.color, alpha=0.4)

    return hist


if __name__ == '__main__':
    main()
