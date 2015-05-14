import cPickle as pickle
import datetime
import numpy as np
import matplotlib.pyplot as plt
from mymodule import files, convert, grid


def main(forecast, lead_times):
    nt = len(lead_times)
    rms_err = np.zeros(nt)
    rms_res = np.zeros(nt)
    mean_err = np.zeros(nt)
    mean_res = np.zeros(nt)

    for n, lead_time in enumerate(lead_times):
        if n != 0:
            print n
            forecast.set_lead_time(lead_time)
            q_err, q_res, surf, pv, q, mass = load(forecast.cubelist)
            mask = make_mask(surf, pv, q)
            results = calculate(q_err, q_res, mass, mask)
            rms_err[n] = results[0]
            rms_res[n] = results[1]
            mean_err[n] = results[2]
            mean_res[n] = results[3]
    with open('/home/lsaffi/data/errors.pkl', 'w') as output:
        pickle.dump([rms_err, rms_res, mean_err, mean_res], output)
    plot(lead_times, rms_err, rms_res, mean_err, mean_res)
    plt.savefig('/home/lsaffi/plots/errors.png')


def load(cubes):
    cubes.remove(cubes.extract('air_pressure')[0])

    q_err = convert.calc('missing_term', cubes)
    q_res = convert.calc('residual_error', cubes)
    surf = convert.calc('atmosphere_boundary_layer_height', cubes)
    pv = convert.calc('total_pv', cubes)
    q = convert.calc('specific_humidity', cubes)

    density = convert.calc('air_density', cubes)
    volume = grid.volume(density)
    mass = volume * density.data

    return q_err, q_res, surf, pv, q, mass


def calculate(q_err, q_res, mass, mask):
    mmass = np.ma.masked_where(mask, mass)
    err = np.ma.masked_where(mask, q_err.data)
    res = np.ma.masked_where(mask, q_res.data)

    mmass1 = np.ma.sum(mmass)
    mmass2 = np.ma.sum(mmass ** 2)
    rms_err = np.sqrt(np.ma.sum((err * mass) ** 2) / mmass2)
    rms_res = np.sqrt(np.ma.sum((res * mass) ** 2) / mmass2)
    mean_err = np.ma.sum(err * mass) / mmass1
    mean_res = np.ma.sum(res * mass) / mmass1

    return rms_err, rms_res, mean_err, mean_res


def make_mask(surf, pv, q):
    bl = surf.data * np.ones(pv.shape) > pv.coord('altitude').points
    stratosphere = np.logical_and(pv.data > 2.0, q.data < 0.001)
    mask = np.logical_or(bl, stratosphere)

    return mask


def plot(lead_times, rms_err, rms_res, mean_err, mean_res):
    plt.plot(lead_times, rms_err, '-x',
             label='Root Mean Square Initial Residual')
    plt.plot(lead_times, rms_res, '-x',
             label='Root Mean Square Final Residual')
    plt.plot(lead_times, mean_err, '-x',
             label='Mean Initial Residual')
    plt.plot(lead_times, mean_res, '-x',
             label='Mean Final Residual')
    plt.legend(loc='best')
    plt.xlabel('Lead time (hours)')
    plt.ylabel('Mass Weighted PV (PVU)')
    plt.xlim(lead_times[0], lead_times[-1])

if __name__ == '__main__':
    with open('/home/lsaffi/data/forecasts/iop5.pkl', 'r') as infile:
        iop5 = pickle.load(infile)

    dt = datetime.timedelta(hours=1)
    lead_times = [n * dt for n in xrange(0, 37)]
    #main(iop5, lead_times)
    with open('/home/lsaffi/data/errors.pkl', 'r') as infile:
        [rms_err, rms_res, mean_err, mean_res] = pickle.load(infile)
    lead_times = range(0, 37)
    plot(lead_times, rms_err, rms_res, mean_err, mean_res)
    plt.savefig('/home/lsaffi/plots/errors1.png')
