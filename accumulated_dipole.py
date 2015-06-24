import cPickle as pickle
import datetime
import numpy as np
import matplotlib.pyplot as plt
from mymodule import convert, grid, diagnostic


def main(forecast, times, names):
    """
    """
    means = {}
    for name in names:
        means[name] = np.zeros([len(times), len(bins) - 1])
    for n, time in enumerate(times[1:]):
        print(time)
        forecast.set_lead_time(datetime.timedelta(hours=time))
        # Load required variables
        pv, q, surf, mass = extract(forecast.cubelist)

        # Make a tropopause and boundary layer mask
        mask = make_mask(pv, q, surf)

        # Calculate the tropopause dipole for each diagnostic
        for name in names:
            x = convert.calc(name, forecast.cubelist)
            means[name][n + 1, :] = diagnostic.averaged_over(x.data, bins,
                                                             pv.data,
                                                             mass, mask=mask)

    with open('/home/lsaffi/data/IOP5/long_dipole2.pkl', 'w') as output:
        pickle.dump(means, output)

    plotfig(names, times, bins, means)


def extract(cubelist):
    """Obtain required variables from cubelist
    """
    # Remove pressure on rho levels
    cubelist.remove(cubelist.extract('air_pressure')[0])
    pv = convert.calc('advection_only_pv', cubelist)
    q = convert.calc('specific_humidity', cubelist)
    surf = convert.calc('atmosphere_boundary_layer_height', cubelist)

    # Calculate the mass in each gridbox
    density = convert.calc('air_density', cubelist)
    volume = grid.volume(density)
    mass = volume * density.data

    return pv, q, surf, mass


def make_mask(pv, q, surf):
    """Makes a mask to ignore the boundary layer and far from the tropopause
    """
    trop = diagnostic.tropopause2(pv, q)
    mask = surf.data * np.ones(pv.shape) > pv.coord('altitude').points
    mask = np.logical_or(np.logical_not(trop), mask)
    diab = np.logical_and(pv.data > 2, q.data > 0.01)
    mask = np.logical_or(mask, diab)

    return mask


def plotfig(names, times, bins, means):
    for name in names:
        plt.plot(times, means[name][:, 0], '-x', label='Tropospheric Anomaly',
                 color='b')
        plt.plot(times, means[name][:, 1], '-x', label='Stratospheric Anomaly',
                 color='r')
        plt.xlabel('Time')
        plt.xlim(times[0], times[-1])
        plt.ylabel('Mass Weighted Mean PV (PVU)')
        plt.legend(loc='best')
        plt.title(name)
        plt.savefig('/home/lsaffi/plots/acc_dipole_long_' + name + '2.png')

if __name__ == '__main__':
    names = ['total_minus_advection_only_pv']
    bins = [-100, 2, 100]
    times = np.linspace(0, 120, 21)
    with open('/home/lsaffi/data/forecasts/iop5_long.pkl') as infile:
        forecast = pickle.load(infile)
    main(forecast, times, names)
