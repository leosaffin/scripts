import datetime
import cPickle as pickle
import numpy as np
from mymodule import convert, grid, diagnostic
from mymodule.forecast import Forecast


def main(forecast, times):
    """
    """
    means = {}
    for name in names:
        means[name] = np.zeros([len(times), len(bins) - 1])
    means2 = np.zeros([len(times), 2])
    for n, time in enumerate(times):
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
            means[name][n, :] = diagnostic.averaged_over(x.data, bins, pv.data,
                                                         mass, mask=mask)

        x = convert.calc('total_minus_advection_only_pv')
        means2[n, :] = diagnostic.averaged_over(x.data, bins2, pv.data,
                                                mass, mask=mask)

    with open('/home/lsaffi/data/dipole.pkl')as output:
        pickle.dump([means, means2], output)


if __name__ == '__main__':
    directory = '/projects/diamet/lsaffi/xjjhq/xjjha_'
    start_time = datetime.datetime(2011, 11, 28, 12)
    dt = datetime.timedelta(hours=1)
    times = [start_time + n * dt for n in xrange(37)]
    mapping = {time: directory + str(int((time - start_time).total_seconds() /
                                         3600)) for time in times}
    del mapping[start_time]

    names = ['total_minus_advection_only_pv', 'sum_of_physics_pv_tracers']
    bins = np.linspace(0, 8, 33)
    bins2 = [0, 2, 8]
    iop5 = Forecast(mapping)
    main(iop5, times)
