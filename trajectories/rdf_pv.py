import pickle

import numpy as np
from scipy.interpolate import griddata
from iris.analysis.cartography import rotate_pole, get_xy_grids

from irise.trajectory import load as trload
from irise import convert, files, plot
from myscripts import datadir


def main():
    name = 'advection_only_pv'
    pole_lon = 177.5
    pole_lat = 37.5
    domain = [328.3, 390.35, -17.97, 17.77]
    data_in = datadir + 'iop5/trajectories/trace_500hpa_35h.1'
    data_out = datadir + 'iop5/trajectories/rdf_pv_500hpa_35h'

    rdf_pv(data_in, data_out, name, pole_lon, pole_lat, domain)
    return


def rdf_pv(data_in, data_out, name, pole_lon, pole_lat, domain):
    # Load the trajectories
    trajectories = trload.raw(data_in)

    # Check which trajectories are in the domain
    for trajectory in trajectories:
        in_domain(trajectory, pole_lon, pole_lat, domain)

    # Calculate variable at the start of all trajectories
    rlons, rlats, values, cube = rdf(name, trajectories, pole_lon, pole_lat)

    # Save the preliminary data
    with open(data_out + '.pkl', 'w') as output:
        pickle.dump((rlons, rlats, values), output)

    # Put the values on the normal grid
    lons, lats = get_xy_grids(cube)
    field = regular_grid(values, rlons, rlats, lons, lats)
    cube = cube[0].copy(data=field)

    # Save the field
    files.save([cube], data_out + '.nc')

    return


def in_domain(trajectory, pole_lon, pole_lat, domain):
    """Checks whether the trajectory is in the given domain
    """
    for n in xrange(len(trajectory)):
        lon = trajectory.variable('lon')[n]
        lat = trajectory.variable('lat')[n]
        rlon, rlat = rotate_pole(np.array(lon), np.array(lat),
                                 pole_lon, pole_lat)
        rlon = rlon + 360
        if outside_bounds(rlon, rlat, domain):
            trajectory.data = trajectory.data[0:(n + 1)]
            return

    return


def outside_bounds(rlon, rlat, domain):
    if rlon < domain[0]:
        return True
    if rlon > domain[1]:
        return True
    if rlat < domain[2]:
        return True
    if rlat > domain[3]:
        return True
    return False


def rdf(name, trajectories, pole_lon, pole_lat):
    """ Get the values of variable at the start of trajectories

    Args:
        name (str): Name of variable to calculate at the start of trajectories

        trajectories (list): Length n list of trajectory objects

        pole_lon (float): Rotated pole longitude

        pole_lat (float): Rotated pole latitude

    Returns:
        rlons (list): Length n list of rotated longitude at end of trajectories

        rlons (list): Length n list of rotated latitude at end of trajectories

        values (list): Length n list of variable at start of trajectories
    """
    # Initialise output lists
    rlons = []
    rlats = []
    values = []

    # Loop over all trajectories
    for n, trajectory in enumerate(trajectories):
        if n % 10000 == 0:
            print(n)
        # Extract the position at the last trajectory point
        time = trajectory.variable('time')[-1]
        lon = trajectory.variable('lon')[-1]
        lat = trajectory.variable('lat')[-1]
        p = trajectory.variable('p')[-1]
        pv = trajectory.variable('PV')[-1]

        # Extract the data from the forecast
        if n == 1:
            forecast.set_time(time)
            cube = convert.calc(name, forecast.cubelist)

        # Get the starting position
        lon = trajectory.variable('lon')[0]
        lat = trajectory.variable('lat')[0]
        rlon, rlat = rotate_pole(np.array(lon), np.array(lat),
                                 pole_lon, pole_lat)

        # Save the values for plotting
        rlons.append(float(rlon + 360))
        rlats.append(float(rlat))
        values.append(float(pv))

    return rlons, rlats, values, cube


def regular_grid(field, lons, lats, grid_lon, grid_lat):
    """ Puts the data on a regular grid
    Args:
        field (list): Length n, data
        lons (list): Length n, longitude points
        lats (list): Length n, latitude points
        grid_lon (numpy.ndarray): 2d array of longitude grid
        grid_lat (numpy.ndarray): 2d array of latitude grid
    """
    points = [lons, lats]
    points = np.transpose(np.array(points))
    return griddata(points, field, (grid_lon, grid_lat), method='linear')


if __name__ == '__main__':
    main()
