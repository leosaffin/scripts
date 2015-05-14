import cPickle as pickle
import datetime
import numpy as np
import matplotlib.pyplot as plt
from mymodule import files, convert, grid


def main(forecast, diagnostics, lead_times):
    nd = len(diagnostics)
    nt = len(lead_times)
    rms = np.zeros([nd, nt])
    mean = np.zeros([nd, nt])

    for n, lead_time in enumerate(lead_times):
        if n != 0:
            print n
            forecast.set_lead_time(lead_time)
            x, surf, pv, q, mass = load(forecast.cubelist, diagnostics)
            mask = make_mask(surf, pv, q)
            rms[:, n], mean[:, n] = calculate(x, mass, mask)
    with open('/home/lsaffi/data/IOP5/rms_vs_time.pkl', 'w') as output:
        pickle.dump(rms, output)
    with open('/home/lsaffi/data/IOP5/mean_vs_time.pkl', 'w') as output:
        pickle.dump(mean, output)
    plot(rms, mean, lead_times, diagnostics)
    plt.savefig('/home/lsaffi/plots/rms_mean_vs_time.png')


def load(cubes, diagnostics):
    cubes.remove(cubes.extract('air_pressure')[0])

    x = []
    for diagnostic in diagnostics:
        x.append(convert.calc(diagnostic, cubes))

    surf = convert.calc('atmosphere_boundary_layer_height', cubes)
    pv = convert.calc('total_pv', cubes)
    q = convert.calc('specific_humidity', cubes)

    density = convert.calc('air_density', cubes)
    volume = grid.volume(density)
    mass = volume * density.data

    return x, surf, pv, q, mass


def calculate(x, mass, mask):
    mmass = np.ma.masked_where(mask, mass)
    mmass1 = np.ma.sum(mmass)
    mmass2 = np.ma.sum(mmass ** 2)

    mean = []
    rms = []
    for y in x:
        y = np.ma.masked_where(mask, y.data)
        rms.append(np.sqrt(np.ma.sum((y * mass) ** 2) / mmass2))
        mean.append(np.ma.sum(y * mass) / mmass1)

    return mean, rms


def make_mask(surf, pv, q):
    bl = surf.data * np.ones(pv.shape) > pv.coord('altitude').points
    stratosphere = np.logical_and(pv.data > 2.0, q.data < 0.001)
    mask = np.logical_or(bl, stratosphere)

    return mask


def plot(rms, mean, lead_times, diagnostics):
    times = [lead_time.seconds / 3600 for lead_time in lead_times]
    for n, diagnostic in enumerate(diagnostics):
        plt.plot(times, rms[n, :], '-x',
                 label='RMS ' + diagnostic)
        plt.plot(times, mean[n, :], '-x',
                 label='Mean ' + diagnostic)

    plt.legend(loc='best')
    plt.xlabel('Lead time (hours)')
    plt.ylabel('Mass Weighted PV (PVU)')
    plt.xlim(lead_times[0], lead_times[-1])

if __name__ == '__main__':
    with open('/home/lsaffi/data/forecasts/iop5.pkl', 'r') as infile:
        iop5 = pickle.load(infile)

    dt = datetime.timedelta(hours=1)
    lead_times = [n * dt for n in xrange(0, 37)]
    diagnostics = ['short_wave_radiation_pv',
                   'long_wave_radiation_pv',
                   'microphysics_pv',
                   'gravity_wave_drag_pv',
                   'convection_pv',
                   'boundary_layer_pv',
                   'advection_inconsistency_pv',
                   'cloud_rebalancing_pv',
                   'total_minus_advection_only_pv',
                   'sum_of_physics_pv_tracers',
                   'initial_residual_pv',
                   'final_residual_pv']
    # main(iop5, lead_times)

    with open('/home/lsaffi/data/IOP5/rms_vs_time.pkl', 'r') as infile:
        rms = pickle.load(infile)
    with open('/home/lsaffi/data/IOP5/mean_vs_time.pkl', 'r') as infile:
        mean = pickle.load(infile)
    lead_times = range(0, 37)
    plot(rms, mean, lead_times, diagnostics)
    plt.savefig('/home/lsaffi/plots/errors1.png')
