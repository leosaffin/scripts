import cPickle as pickle
import numpy as np
from mymodule import convert, diagnostic, grid, interpolate
from scripts.season import subset


# Constant parameters for each forecast
bins = np.linspace(0, 8, 33)

# Pressure level for error statistics
plevs = np.linspace(85000, 25000, 13)

names = ['total_minus_advection_only_potential_temperature',
         'total_minus_advection_only_pv',
         'ertel_potential_vorticity',
         'advection_only_pv',
         'dynamics_tracer_inconsistency',
         'microphysics_pv',
         'short_wave_radiation_pv',
         'long_wave_radiation_pv',
         'gravity_wave_drag_pv',
         'convection_pv',
         'boundary_layer_pv',
         'cloud_rebalancing_pv',
         'wind_speed',
         'relative_humidity',
         'specific_humidity']

error_measures = ['ertel_potential_vorticity',
                  'air_potential_temperature',
                  'air_temperature',
                  'relative_humidity',
                  'wind_speed']


class Suite():
    """A collection of diagnostics used to analyse a forecast

    Attributes:
        forecast (mymodule.forecast.Forecast): A collection of forecast data
        id (str): An identifier for saved files to match the job
        data (dict): A database of analysed data from the forecast
        errors (dict): A database of forecast error measures
    """

    def __init__(self, forecast, job_id):
        self.forecast = forecast
        self.id = job_id
        self.data = {}
        self.errors = {}

    def set_time(self, time):
        """ Sets the time of the associated forecast

        Args:
            time (datetime.datetime): Time to set the forecast to
        """
        self.forecast.set_time(time)

    def analyse(self):
        """ Performs an independent analysis of a single timestep
        """
        # Initialise the data storage for this timestep
        self.data[self.forecast.time] = {}

        # Extract the cubes at the current time
        cubes = self.forecast.cubelist

        # Make tropopause mask
        mask = make_mask(cubes)

        # Extract variables
        variables = [convert.calc(name, cubes).data for name in names]
        adv = convert.calc('advection_only_pv', cubes).data
        density = convert.calc('air_density', cubes)
        volume = grid.volume(density)
        mass = volume * density.data

        # Loop over subsets of the domain
        for name in subset.subsets:
            self.data[self.forecast.time][name] = (
                calc_diagnostics(variables, adv, mass, mask,
                                 subset.subsets[name]))

    def analyse_errors(self, suite):
        """Analyses forecast errors

        Args:
            suite (Suite): Another suite holding data about a forecast
                initialised after the forecast held in this suite
        """
        start_dt = suite.forecast.start_time - self.forecast.start_time
        full_dt = suite.forecast.time - self.forecast.start_time
        # Initialise dictionary for two forecasts if it's the first set
        if start_dt == full_dt:
            self.errors[start_dt] = {}
        # Initialise dictionary for current dt
        self.errors[start_dt][full_dt] = {}

        # Calculate mean sea-level pressure variables
        forecast = convert.calc('air_pressure_at_sea_level',
                                self.forecast.cubelist)
        analysis = convert.calc('air_pressure_at_sea_level',
                                suite.forecast.cubelist)
        diff = forecast.data - analysis.data
        self.errors[start_dt][full_dt]['air_pressure_at_mean_sea_level'] = (
            calc_errors(diff))

        # Make pressure coordinates
        p = convert.calc('air_pressure', self.forecast.cubelist)
        p_f = grid.make_coord(p)
        p = convert.calc('air_pressure', suite.forecast.cubelist)
        p_a = grid.make_coord(p)

        # Analyse all 3d fields
        for variable in error_measures:
            # Extract forecast and proxy analysis fields
            cube = convert.calc(variable, self.forecast.cubelist)
            cube.add_aux_coord(p_f, [0, 1, 2])
            forecast = interpolate.to_level(cube, air_pressure=plevs)

            cube = convert.calc(variable, suite.forecast.cubelist)
            cube.add_aux_coord(p_a, [0, 1, 2])
            analysis = interpolate.to_level(cube, air_pressure=plevs)

            diff = (forecast - analysis).data
            self.errors[start_dt][full_dt][variable] = calc_errors(diff)

    def save(self):
        with open('/home/lsaffi/data/season/' +
                  self.id + '2.pkl', 'w') as output:
            pickle.dump(self.data, output)
            pickle.dump(self.errors, output)

    def __del__(self):
        print('Analysed ' + str(self.forecast.start_time))


def make_mask(cubelist):
    """Makes a mask to ignore the boundary layer and far from the tropopause

    Args:
        cubelist (iris.cube.Cubelist):

    Returns:
        mask (np.array): An array with True in places that are to be masked and
            False elsewhere
    """
    pv = convert.calc('advection_only_pv', cubelist)
    q = convert.calc('specific_humidity', cubelist)
    surf = convert.calc('atmosphere_boundary_layer_height', cubelist)
    trop = diagnostic.tropopause(pv, q)
    mask = surf.data * np.ones(pv.shape) > pv.coord('altitude').points
    mask = np.logical_or(np.logical_not(trop), mask)

    return mask


def calc_diagnostics(variables, adv, mass, mask, domain):
    """Calculates a single timestep of diagnostics

    Args:
        variables (list): List of cubes to be analysed for the tropopause
            dipole
        adv (np.array): The data array of the advection only PV
        mass (np.array): The mass in each gridbox
        mask (np.array): A tropopause mask
    """
    # Subset data arrays
    variables = [domain.slice(variable) for variable in variables]
    adv = domain.slice(adv)
    mass = domain.slice(mass)
    mask = domain.slice(mask)

    # Intialise output
    output = {}

    # Calculate PV dipole
    output['dipole'] = diagnostic.averaged_over(variables, bins, adv, mass,
                                                mask=mask)
    output['mean'] = [np.mean(x, axis=(1, 2)) for x in variables]

    output['stdev'] = [np.std(x, axis=(1, 2)) for x in variables]

    # Calculate front diagnostics

    # Calculate Eady growth rate

    return output


def calc_errors(diff):
    """Calculates measures of forecast errors
    """
    output = {}
    for name in subset.subsets:
        output[name] = {}
        ndiff = subset.subsets[name].slice(diff)
        if diff.ndim == 3:
            output[name]['rms'] = np.sqrt(
                np.ma.average(ndiff ** 2, axis=(1, 2)))
            output[name]['mean'] = np.ma.average(ndiff, axis=(1, 2))
        else:
            output[name]['rms'] = np.sqrt(np.ma.mean(ndiff ** 2))
            output[name]['mean'] = np.ma.mean(ndiff)

    return output
