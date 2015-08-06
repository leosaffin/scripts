import cPickle as pickle
import datetime
import numpy as np
import matplotlib.pyplot as plt
from scripts.season import user_information, diagnostics


names = diagnostics.names
bins = 0.5 * (diagnostics.bins[0:-1] + diagnostics.bins[1:])


def main(dt):
    """Creates a line plot for each forecast at lead time dt

    Args:
        dt (datetime.timedelta): Lead time to load
    """
    # Load the data at lead time dt
    dipoles = load1(dt)

    # Loop over each pv tracer
    for name in names:
        # Calculate mean and standard deviation
        mean, stdev = analyse1(dipoles[name])
        plotfig1(mean, stdev, name)
        plt.savefig('/home/lsaffi/plots/season/dipole/2.5D_'
                    + name + '.png')


def main2(dt):
    """Creates a colour contour plot through each forecast at lead time dt

    Args:
        dt (datetime.timedelta): Lead time to load
    """
    # Load the data at lead time dt
    dipoles = load1(dt)
    with open('/home/lsaffi/data/season/nao.pkl') as infile:
        nao = pickle.load(infile)

    # Loop over each pv tracer
    for name in names:
        plotfig2(dipoles[name], nao)
        plt.savefig('/home/lsaffi/plots/season/dipole/92D_' + str(dt.days) +
                    'D_' + name + '_pc.png')


def main3():
    """Creates a colour contour plot of the average pv accumulation
    """
    # Load the data at all lead times
    dipoles = load3()


def load1(dt):
    """

    Args:
        dt (datime.timedelta): Lead time

    Returns:
        dipoles (dict): Mapping of dipole data at lead time dt to each pv
            tracer
    """
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


def load3():
    """
    """
    dipoles = {}
    for name in names:
        dipoles[name] = {}

    # Load dipole data
    for start_time in user_information.job_ids:
        if start_time < datetime.datetime(2014, 2, 1):
            job_id = user_information.job_ids[start_time]

            with open('/home/lsaffi/data/season/' + job_id + '.pkl') as infile:
                data = pickle.load(infile)

            for time in data:
                for variable, name in zip(data[time][0], names):
                    dipoles[name][time] = variable

    # Convert into numpy arrays
    return dipoles


def analyse1(dipole):
    """Calculate mean and standard deviation

    Args:
        dipole (np.array): 2D array

    Returns:
        mean:
        stdev:
    """
    mean = np.mean(dipole, axis=0)
    stdev = np.std(dipole, axis=0)
    return mean, stdev


def plotfig1(mean, stdev, name):
    plt.figure(1)
    plt.clf()
    plt.errorbar(bins, mean, yerr=stdev, label=name)
    axy = (abs(mean) + stdev).max()
    plt.axis([0, 8, -axy, axy])
    plt.xlabel('Advection Only PV (PVU)')
    plt.ylabel('Mean PV (PVU)')
    plt.title(name.replace('_', ' '))


levs = np.linspace(-0.3, 0.3, 16)
days = np.linspace(2, 93, 92)


def plotfig2(dipole, nao):
    plt.figure(1)
    plt.clf()
    #plt.contourf(days, bins, dipole.transpose(), levs, cmap='bwr')
    plt.pcolor(days, diagnostics.bins, dipole.transpose(),
               vmin= -0.3, vmax=0.3, cmap='bwr')
    plt.axis([days[0], days[-1], bins[0], bins[-1]])
    plt.xlabel('Days Since 2013/11/01')
    plt.ylabel('Advection Only PV (PVU)')
    plt.colorbar()


if __name__ == '__main__':
    dt = datetime.timedelta(days=1)
    main2(dt)
