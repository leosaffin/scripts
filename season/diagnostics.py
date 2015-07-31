import cPickle as pickle
import numpy as np
from mymodule import convert, diagnostic, grid


# Constant parameters for each forecast
bins = np.linspace(0, 8, 33)
names = ['total_minus_advection_only_pv',
         'advection_inconsistency_pv',
         'microphysics_pv',
         'short_wave_radiation_pv',
         'long_wave_radiation_pv',
         'gravity_wave_drag_pv',
         'convection_pv',
         'boundary_layer_pv',
         'cloud_rebalancing_pv']


class Suite():
    """A collection of diagnostics used to analyse a forecast
    """

    def __init__(self, forecast, job_id):
        self.forecast = forecast
        self.id = job_id
        self.data = {}

    def set_time(self, time):
        self.forecast.set_time(time)

    def analyse(self):
        # Extract the cubes at the current time
        cubes = self.forecast.cubelist

        # Calculate all diagnostics
        diagnostics = analyse_timestep(cubes)

        self.data[self.forecast.time] = diagnostics

    def save(self):
        with open('/home/lsaffi/data/season/' +
                  self.id + '.pkl', 'w') as output:
            pickle.dump(self.data, output)

    def __del__(self):
        print('Analysed ' + str(self.forecast.start_time))


def analyse_timestep(cubelist):
    """
    """
    cubelist.remove(cubelist.extract('air_pressure')[0])
    cubelist.remove(cubelist.extract('surface_altitude')[0])

    # Make tropopause mask
    mask = make_mask(cubelist)

    # Extract variables
    variables = [convert.calc(name, cubelist).data for name in names]
    adv = convert.calc('advection_only_pv', cubelist).data
    density = convert.calc('air_density', cubelist)
    volume = grid.volume(density)
    mass = volume * density.data

    # Calculate PV dipole
    means, weights = diagnostic.averaged_over(variables, bins, adv, mass,
                                              mask=mask)

    return [means, weights]


def make_mask(cubelist):
    """Makes a mask to ignore the boundary layer and far from the tropopause
    """
    pv = convert.calc('total_pv', cubelist)
    q = convert.calc('specific_humidity', cubelist)
    surf = convert.calc('atmosphere_boundary_layer_height', cubelist)
    trop = diagnostic.tropopause2(pv, q)
    mask = surf.data * np.ones(pv.shape) > pv.coord('altitude').points
    mask = np.logical_or(np.logical_not(trop), mask)

    return mask
