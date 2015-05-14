import datetime
import cPickle as pickle
import numpy as np
import matplotlib.pyplot as plt
from mymodule import convert, grid, diagnostic
from mymodule.forecast import Forecast


def main(forecast, times):
    """
    """
    means = {}
    for name in names:
        means[name] = np.zeros([len(times) + 1, len(bins) - 1])
    means2 = np.zeros([len(times) + 1, 2])
    for n, time in enumerate(times):
        print(n)
        forecast.set_time(time)

        forecast.cubelist.remove(forecast.cubelist.extract('air_pressure')[0])
        pv = convert.calc('advection_only_pv', forecast.cubelist)
        q = convert.calc('specific_humidity', forecast.cubelist)
        density = convert.calc('air_density', forecast.cubelist)
        surf = convert.calc('atmosphere_boundary_layer_height',
                            forecast.cubelist)

        volume = grid.volume(density)
        mass = volume * density.data

        # Make a tropopause masked
        trop = diagnostic.tropopause2(pv, q)
        mask = surf.data * np.ones(pv.shape) > pv.coord('altitude').points
        mask = np.logical_or(trop, mask)

        for name in names:
            x = convert.calc(name, forecast.cubelist)
            means[name][n + 1, :] = diagnostic.averaged_over(x.data, bins,
                                                             pv.data,
                                                             mass, mask=mask)

        x = convert.calc('total_minus_advection_only_pv', forecast.cubelist)
        means2[n + 1, :] = diagnostic.averaged_over(x.data, bins2, pv.data,
                                                    mass, mask=mask)

    with open('/home/lsaffi/data/dipole.pkl', 'w') as output:
        pickle.dump([means, means2], output)


def plotfig(names, times, bins):
    with open('/home/lsaffi/data/dipole.pkl', 'r') as output:
        means, means2 = pickle.load(output)
    bin_centres = 0.5 * (bins[0:-1] + bins[1:])
    levs = np.linspace(-0.15, 0.15, 16)
    for name in names:
        plt.figure()
        plt.contourf(times, bin_centres, means[name].T, levs, cmap='bwr',
                     extend='both')
        plt.xlabel('Time')
        plt.xlim(times[0], times[-1])
        plt.ylabel('Advection Only PV (PVU)')
        plt.colorbar()
        plt.savefig('/home/lsaffi/plots/' + name + 'dipole.png')
    plt.clf()
    plt.plot(times, means2[:, 0], '-x', label='Tropospheric Anomaly', color='b')
    plt.plot(times, means2[:, 1], '-x', label='Stratospheric Anomaly', color='r')
    plt.xlabel('Time')
    plt.xlim(times[0], times[-1])
    plt.ylabel('Mass Weighted Mean PV (PVU)')
    plt.legend(loc='best')
    plt.savefig('/home/lsaffi/plots/acc_dipole.png')

if __name__ == '__main__':
    directory = '/projects/diamet/lsaffi/xjjhq/xjjha_'
    start_time = datetime.datetime(2011, 11, 28, 12)
    dt = datetime.timedelta(hours=1)
    times = [start_time + n * dt for n in xrange(37)]
    del times[0]
    mapping = {time: directory +
               str(int((time - start_time).total_seconds() / 3600)).zfill(3) +
               '.pp'
               for time in times}

    names = ['total_minus_advection_only_pv', 'sum_of_physics_pv_tracers']
    bins = np.linspace(0, 8, 33)
    bins2 = [0, 2, 8]
    iop5 = Forecast(start_time, mapping)
    #main(iop5, times)
    times = np.linspace(0, 36, 37)
    plotfig(names, times, bins)
