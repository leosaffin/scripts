import numpy as np
import matplotlib.pyplot as plt
import iris.plot as iplt
from iris.analysis import MEAN
from irise import convert
from irise.plot.util import multilabel, legend
from myscripts.models.um import case_studies
from myscripts.projects.thesis.bl import plotdir

label = ['Stable', 'Well mixed', 'Cumulus capped', 'Shear driven']
style = ['-gx', '-rx', '-bx', '-yx']


def main():
    forecasts = [case_studies.iop5b.copy(), case_studies.iop8.copy()]

    fig = plt.figure(figsize=(18, 8))
    for n, forecast in enumerate(forecasts):
        ax = plt.subplot2grid((1, 2), (0, n))

        cubes = forecast.set_lead_time(hours=24)
        theta = convert.calc('air_potential_temperature', cubes)
        bl_type = convert.calc('boundary_layer_type', cubes)
        for m in range(4):
            mask = np.logical_not(np.logical_or(bl_type.data == 2 * m,
                                                bl_type.data == 2 * m + 1))
            mask = mask * np.ones_like(theta.data)
            mean = theta_profile(theta, mask)
            mean = mean - mean[0]
            iplt.plot(mean, mean.coord('atmosphere_hybrid_height_coordinate'),
                      style[m], label=label[m])

        #mask = np.logical_not(mask)
        #mean = theta_profile(theta, mask)
        # iplt.plot(mean, mean.coord('atmosphere_hybrid_height_coordinate'),
        #          '-kx')

        ax.set_xlim(-0.25, 4.5)
        ax.set_xlabel(r'$\theta$')
        ax.set_ylim(0, 1000)
        if n == 0:
            ax.set_ylabel('Height (m)')
            ax.set_title('IOP5')
        else:
            ax.get_yaxis().set_ticklabels([])
            ax.set_title('IOP8')

        plt.axvline(color='k')
        multilabel(ax, n)

    legend(ax, loc='upper left', ncol=2, bbox_to_anchor=(-0.6, -0.2))
    fig.subplots_adjust(bottom=0.4)

    fig.savefig(plotdir + 'theta_profiles.pdf')
    plt.show()

    return


def theta_profile(theta, mask):
    theta = theta.copy()
    theta.data = np.ma.masked_where(mask, theta.data)

    return theta.collapsed(['grid_longitude', 'grid_latitude'], MEAN)


if __name__ == '__main__':
    main()
