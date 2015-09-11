import cPickle as pickle
import datetime
import numpy as np
from iris.cube import Cube, CubeList
from iris.coords import DimCoord
from scripts.season import user_information, diagnostics, subset


plevs = DimCoord(diagnostics.plevs, standard_name='air_pressure', units='Pa')
advlevs = DimCoord(diagnostics.bins, standard_name='ertel_potential_vorticity',
                   units='PVU')
zlevs = DimCoord(np.linspace(1, 50, 50), standard_name='level_height',
                 units='m')
tdiff = [x.total_seconds() for x in user_information.lead_times]
tlevs = DimCoord(tdiff, standard_name='time', units='s')
t_index1 = user_information.lead_times[4:]
err_tlevs1 = tlevs[4:]
t_index2 = user_information.lead_times[8:]
err_tlevs2 = tlevs[8:]


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
    with open(job_id + '2.pkl') as infile:
        diags = pickle.load(infile)
        errors = pickle.load(infile)

    # Loop over domains analysed
    for domain in subset.subsets:
        # Create a cubelist for the analysed domain
        output[domain] = CubeList()
        # Add all error measures to the cubelist
        for name in diagnostics.error_measures:
            _extract_errors(errors, name, output, domain)
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
    for error_type in ['RMS', 'MEAN']:
        for t_index, t_coord, prefix in [(t_index1, err_tlevs1, 'one_day_'),
                                         (t_index2, err_tlevs2, 'two_day_')]:

            # Extract data for each error measure at each time
            data = []
            for dt in t_index:
                data.append(errors[t_index[0]][dt][name][error_type])

            # Create new cube with extracted data
            cube_name = prefix + error_type.lower() + '_error_of_' + name
            newcube = Cube(data=np.array(data), long_name=cube_name,
                           dim_coords_and_dims=[(t_coord, 0), (plevs, 1)])
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
    for dt in user_information.lead_times:
        data.append(diags[start_time + dt][domain]['dipole'][0][n])

    # Create new cube with extracted data
    cube_name = 'mass_weighted_mean_of_' + name
    newcube = Cube(data=np.array(data), long_name=cube_name,
                   dim_coords_and_dims=[(tlevs, 0), (advlevs, 1)])
    output[domain].append(newcube)

    for statistic in ['MEAN', 'VARIANCE']:
        # Extract data for each statistic at each time
        data = []
        for dt in user_information.lead_times:
            data.append(diags[start_time + dt][domain][statistic][n])

        # Create new cube with extracted data
        cube_name = statistic.lower() + '_of_' + name
        newcube = Cube(data=np.array(data), long_name=cube_name,
                       dim_coords_and_dims=[(tlevs, 0), (zlevs, 1)])
        output[domain].append(newcube)
