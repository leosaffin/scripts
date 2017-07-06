import matplotlib.pyplot as plt
import pandas as pd
from mymodule import convert, plot
from scripts import case_studies

path = '/home/lsaffin/Documents/meteorology/'
name = 'forward_trajectories'
levels = ('air_potential_temperature', [320])


def main(cubes, filename):
    # Plot a map at verification time
    pv = convert.calc('ertel_potential_vorticity', cubes, levels=levels)[0]
    theta_adv = convert.calc('advection_only_theta', cubes, levels=levels)[0]

    plot.pcolormesh(theta_adv, vmin=300, vmax=340, cmap='coolwarm', pv=pv)

    # Load the trajectories
    trajectories = pd.read_pickle(filename)

    # Plot every trajectory that stays in the domain
    for T in trajectories:
        if (T.altitude.values > 0).all():
            x, y, color = T.grid_longitude, T.grid_latitude, T.altitude
            lc = plot.colored_line_plot(
                x - 360, y, color / 1000, vmin=5, vmax=12, cmap='viridis')

    cbar = plt.colorbar(lc)
    cbar.set_label('km')
    cbar.set_ticks(range(5, 13))

    # Mark the start and end point of trajectories
    plt.scatter(trajectories.values[:, 0, 0], trajectories.values[:, 0, 1],
                color='k', marker='x', linewidths=1, zorder=2)
    plt.scatter(trajectories.values[:, -1, 0], trajectories.values[:, -1, 1],
                color='k', marker='x', linewidths=1, zorder=2)

    plt.title(r'$\theta_{adv}$')
    plt.savefig(path + 'output/' + name + '.png')
    plt.show()

    return


if __name__ == '__main__':
    forecast = case_studies.iop5b.copy()
    cubes = forecast.set_lead_time(hours=24)

    filename = path + 'data/iop5/' + name + '.pkl'
    main(cubes, filename)
