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
            means[name][n + 1, :], weights = (
                diagnostic.averaged_over(x.data, bins, pv.data, mass,
                                         mask=mask))

    with open('/home/lsaffi/data/IOP5/accumulated_dipole.pkl', 'w') as output:
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

    return mask


def plotfig(names, times, bins, means):
    levs = [-0.15, -0.125, -0.1, -0.075, -0.05, -0.025, 0.025, 0.05, 0.075,
            0.1, 0.125, 0.15]
    for name in names:
        plt.figure()
        plt.contourf(times, bins, means[name].transpose(),
                     levs, cmap='bwr', extend='both')
        plt.xlabel('Time')
        plt.xlim(times[0], times[-1])
        plt.ylabel('Advection Only PV (PVU)')
        plt.colorbar(orientation='horizontal')
        plt.title(name)
        plt.savefig('/home/lsaffi/plots/paper/accumulated_dipole_' + name +
                    '.png')

if __name__ == '__main__':
    names = ['total_minus_advection_only_pv',
             'sum_of_physics_pv_tracers']
    bins = np.linspace(0, 8, 33)
    bin_centres = np.linspace(0.025, 7.825, 32)
    times = np.linspace(0, 36, 37)
    with open('/home/lsaffi/data/forecasts/iop5.pkl') as infile:
        forecast = pickle.load(infile)
    #main(forecast, times, names)
    with open('/home/lsaffi/data/IOP5/accumulated_dipole.pkl', 'r') as infile:
        means = pickle.load(infile)
    plotfig(names, times, bin_centres, means)
