import cPickle as pickle
import datetime
import numpy as np
import iris
from iris.cube import Cube, CubeList
from iris.coords import DimCoord
from scripts.season import user_information, diagnostics, subset


path = '/home/lsaffin/Documents/meteorology/data/season/'

plevs = DimCoord(diagnostics.plevs, standard_name='air_pressure', units='Pa')
bin_centres = 0.5 * (diagnostics.bins[:-1] + diagnostics.bins[1:])
advlevs = DimCoord(bin_centres, standard_name='ertel_potential_vorticity',
                   units='PVU')
example_cubes = iris.load('/home/lsaffin/Documents/meteorology/data/' +
                          'iop5_36h.pp')
zlevs = example_cubes[0].coord('level_height')
tdiff = [x.total_seconds() for x in user_information.lead_times[1:]]
tlevs = DimCoord(tdiff, standard_name='time', units='s')
t_index = user_information.lead_times[4:]
err_tlevs = DimCoord(tdiff[3:], standard_name='time', units='s')


def load_all():
    """Loads the full set of data from the analysis of the systematic forecasts

    Returns:
        output (list):
    """
    output = []
    for time in user_information.start_times:
        job_id = user_information.job_ids[time]
        print time
        output.append(load(job_id))

    return output


def load(job_id):
    """ Loads and organises the data from a single forecast

    Args:
        filename (str): The .pkl filename with the raw data
    Returns:
        output (dict): A dictionary mapping cubelists for each domain analysed
    """
    # Initialise the output dictionary
    output = {}

    # Work out the start time of the forecast
    index = user_information.reserved_ids.index(job_id)
    start_time = user_information.start_times[index]

    # Open the raw data from the initial analysis
    with open(path + job_id + '2.pkl') as infile:
        diags = pickle.load(infile)
        errors = pickle.load(infile)

    # Loop over domains analysed
    for domain in subset.subsets:
        # Create a cubelist for the analysed domain
        output[domain] = CubeList()
        # Add all error measures to the cubelist
        for name in diagnostics.error_measures:
            _extract_errors(errors, name, output, domain)
        # Add mslp
        for error_type in ['rms', 'mean']:
            # Extract data for each error measure at each time
            data = []
            for dt in t_index:
                data.append(errors[t_index[0]][dt]
                            ['air_pressure_at_mean_sea_level']
                            [domain][error_type])

            # Create new cube with extracted data
            cube_name = (error_type + '_error_of_' +
                         'air_pressure_at_mean_sea_level')
            newcube = Cube(data=np.array(data), long_name=cube_name,
                           dim_coords_and_dims=[(err_tlevs, 0)])
            output[domain].append(newcube)
        # Add all diagnostics to the cubelist
        for n, name in enumerate(diagnostics.names):
            _extract_diags(diags, start_time, n, name, output, domain)

    return output


def _extract_errors(errors, name, output, domain):
    """
    Args:
        errors (dict): Raw data tree output from first analysis of errors
        name (str): Name of variable to extract
        output (dict): Database to add output cube to
        domain (str): Name of subdomain to extract
    """
    for error_type in ['rms', 'mean']:
        # Extract data for each error measure at each time
        data = []
        for dt in t_index:
            data.append(errors[t_index[0]][dt][name][domain][error_type])

        # Create new cube with extracted data
        cube_name = error_type + '_error_of_' + name        '''
        newcube = Cube(data=np.array(data), long_name=cube_name,
                       dim_coords_and_dims=[(err_tlevs, 0), (plevs, 1)])
        output[domain].append(newcube)


def _extract_diags(diags, start_time, n, name, output, domain):
    """
    Args:
        diags (dict): Raw data tree output from first analysis
        start_time (datetime.datetime): Start time of the forecast data being
            extracted
        n (int): Index of variable to be extracted
        name (str): Name of variable to extract
        output (dict): Database to add output cube to
        domain (str): Name of subdomain to extract
    """
    # Extract pv dipole data at each time
    data = []
    for dt in (user_information.lead_times[1:]):
        try:
            data.append(diags[start_time + dt][domain]['dipole'][0][n])
        except KeyError:
            if n == 0 and domain == 'full':
                print('Skipped at ' + str(dt))
            data.append(np.zeros(len(data[0])))

    # Create new cube with extracted data
    cube_name = 'mass_weighted_mean_of_' + name
    newcube = Cube(data=np.array(data), long_name=cube_name,
                   dim_coords_and_dims=[(tlevs, 0), (advlevs, 1)])
    output[domain].append(newcube)

    # Extract mass
    data = []
    for dt in (user_information.lead_times[1:]):
        try:
            data.append(diags[start_time + dt][domain]['dipole'][1])
        except KeyError:
            data.append(np.zeros(len(data[0])))
    # Create new cube with extracted data
    cube_name = 'mass'
    newcube = Cube(data=np.array(data), long_name=cube_name,
                   dim_coords_and_dims=[(tlevs, 0), (advlevs, 1)])
    output[domain].append(newcube)

    for statistic in ['mean', 'variance']:
        # Extract data for each statistic at each time
        data = []
        for dt in (user_information.lead_times[1:]):
            try:
                data.append(diags[start_time + dt][domain][statistic][n])
            except KeyError:
                data.append(np.zeros(len(data[0])))

        # Create new cube with extracted data
        cube_name = statistic + '_of_' + name
        newcube = Cube(data=np.array(data), long_name=cube_name,
                       dim_coords_and_dims=[(tlevs, 0), (zlevs, 1)])
        output[domain].append(newcube)
