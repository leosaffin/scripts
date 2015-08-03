import cPickle as pickle
import datetime
import numpy as np
import matplotlib.pyplot as plt
from scripts.season import user_information, diagnostics


names = diagnostics.names
bins = 0.5 * (diagnostics.bins[0:-1] + diagnostics.bins[1:])


def main(dt):
    dipoles = load(dt)
    names = ['total_minus_advection_only_pv',
             'advection_inconsistency_pv',
             'long_wave_radiation_pv',
             'residual']
    residual = (dipoles['total_minus_advection_only_pv'] -
                dipoles['long_wave_radiation_pv'] -
                dipoles['short_wave_radiation_pv'] -
                dipoles['microphysics_pv'] -
                dipoles['gravity_wave_drag_pv'] -
                dipoles['convection_pv'] -
                dipoles['boundary_layer_pv'] -
                dipoles['cloud_rebalancing_pv'] -
                dipoles['advection_inconsistency_pv'])

    dipoles['residual'] = residual
    for name in names:
        mean, stdev = analyse(dipoles[name])
        plotfig(mean, stdev, name)
        #plt.savefig('/home/lsaffi/plots/season/dipole/2.5D_'
        #            + name + '.png')
    plt.axis([0, 8, -0.4, 0.4])
    plt.legend(loc='best')
    plt.savefig('/home/lsaffi/plots/season/dipole/1D_all.png')


def load(dt):
    dipoles = {}
    for name in names:
        dipoles[name] = []

    # Load dipole data
    for start_time in user_information.job_ids:
        if start_time < datetime.datetime(2014, 2, 1):
            job_id = user_information.job_ids[start_time]
            time = start_time + dt

            with open('/home/lsaffi/data/season/' + job_id + '.pkl') as infile:
                data = pickle.load(infile)[time][0]

            for variable, name in zip(data, names):
                dipoles[name].append(variable)

    for name in names:
        dipoles[name] = np.array(dipoles[name])

    return dipoles


def analyse(dipole):
    mean = np.mean(dipole, axis=0)
    stdev = np.std(dipole, axis=0)
    return mean, stdev


def plotfig(mean, stdev, name):
    #plt.figure(1)
    #plt.clf()
    plt.errorbar(bins, mean, yerr=stdev, label=name)
    #axy = (abs(mean) + stdev).max()
    #plt.axis([0, 8, -axy, axy])
    plt.xlabel('Advection Only PV (PVU)')
    plt.ylabel('Mean PV (PVU)')
    #plt.title(name.replace('_', ' '))

if __name__ == '__main__':
    dt = datetime.timedelta(days=1)
    main(dt)
