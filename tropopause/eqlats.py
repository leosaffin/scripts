"""Read in John's equivalent latitude data and output as netcdf

Input files have name: emuseries_{YYYYMMDDHH}
"""
import datetime
import numpy as np
import matplotlib.pyplot as plt
import iris
from mymodule import convert, interpolate, grid, plot, user_variables

directory = user_variables.datadir + 'eqlats/'


def main(YYYY, MM, DD, HH):
    # Put the text file in to NetCDF
    infile = directory + 'emuseries_' + YYYY + MM + DD + HH
    outfile = directory + 'eqlats_' + YYYY + '_' + MM + '.nc'
    convert_to_nc(infile, outfile)

    # Calculate theta on 2PVU from NetCDF files
    infile = outfile

    # As a function of latitude
    theta_lat = thetapv2_hemisphere(infile)
    outfile = directory + 'theta_2pvu_' + YYYY + '_' + MM + '.nc'
    iris.save(theta_lat, outfile)

    # On the NAE grid
    theta_nae = thetapv2_nae(infile)
    outfile = directory + 'theta_2pvu_nae_' + YYYY + '_' + MM + '.nc'
    iris.save(theta_nae, outfile)

    # Plot the overview of the time period
    plot_summary(theta_lat)
    plt.ion()

    return


def convert_to_nc(infile, outfile):
    """Read in emuseries text file and sort data to netcdf

    Output file contains:
        Equivalent Latitude (PV Level, Theta Level, Time)
        Surface Equivalent Latitude (Theta Level, Time)

    Args:
        infile (str): Name of input text file

        outfile (str): Name of output NetCDF file
    """
    with open(infile) as data:
        # Top line has the start date
        date = data.readline().split()[-1]
        date = datetime.datetime(
            int(date[0:4]), int(date[4:6]), int(date[6:8]), int(date[8:10]))

        # Second line says how many times there are
        ntimes = int(data.readline().split()[0])

        # Third line gives the time interval
        dt = int(data.readline().split()[0])

        # Make a time coordinate
        t_units = 'hours since ' + str(date)
        time = iris.coords.DimCoord(
            np.arange(ntimes) * dt, long_name='time', units=t_units)
        time.convert_units('days since ' + str(date))

        # Next block states the number of latitudes and their values
        nlats = int(data.readline().split()[0])
        latitude = readlines(data, nlats)
        latitude = iris.coords.DimCoord(latitude, standard_name='latitude')

        # Next block states the number of isentropic levels and their values
        ntheta = int(data.readline().split()[0])
        theta = readlines(data, ntheta)
        theta = iris.coords.DimCoord(
            theta, long_name='potential_temperature', units='K')

        # The next line states the top boundary of isentropic levels
        theta_max = float(data.readline().split()[0])

        # The next line states the max/min values of theta at the surface
        surf_theta = data.readline().split()
        surf_theta_max = float(surf_theta[0])
        surf_theta_min = float(surf_theta[1])

        # The next block states the number of PV levels and their values
        npv = int(data.readline().split()[0])
        pv = readlines(data, npv) * 1e6
        pv = iris.coords.DimCoord(
            pv, long_name='ertel_potential_vorticity', units='PVU')

        # The next block is the max PV on theta values
        data.readline()
        pv_max = readlines(data, ntheta)

        # The next block is the minimum PV on theta values
        data.readline()
        pv_min = readlines(data, ntheta)

        # The next block is equivalent latitudes at the surface
        data.readline()
        eqlat_s = np.arcsin(readlines(data, ntheta * ntimes)) * 180 / np.pi
        eqlat_s = iris.cube.Cube(
            np.reshape(eqlat_s, (ntimes, ntheta)),
            long_name="surface_equivalent_latitude",
            units='degrees',
            dim_coords_and_dims=[(time, 0), (theta, 1)])

        # The next block is equivalent latitudes of PV values
        data.readline()
        eqlat = np.arcsin(readlines(data, npv * ntheta * ntimes)) * 180 / np.pi
        eqlat = iris.cube.Cube(
            np.reshape(eqlat, (ntimes, ntheta, npv)),
            long_name="equivalent_latitude",
            units='degrees',
            dim_coords_and_dims=[(time, 0), (theta, 1), (pv, 2)])

        iris.save(iris.cube.CubeList([eqlat, eqlat_s]), outfile)

        return


def readlines(data, npoints):
    values = []
    while len(values) < npoints:
        for value in data.readline().split():
            values.append(float(value))

    return np.array(values)


def theta_pv2(infile):
    """Load equivalent latitude data on 2 PVU

    Args:
        infile (str): NetCDF file holding equivalent latitudes

    Returns:
        eqlats_cube (iris.cube.Cube):
    """
    # Load the equivalent latitude data on PV2
    cubes = iris.load(infile)

    # phi(t, theta, q)
    eqlats_cube = convert.calc('equivalent_latitude', cubes)

    # theta coordinate
    theta = eqlats_cube.coord('potential_temperature').points

    # phi(t, theta, q=2PVU)
    eqlats = interpolate.main(
        eqlats_cube, ertel_potential_vorticity=[2])[:, :, 0].data

    return eqlats_cube, theta, eqlats


def thetapv2_hemisphere(infile):
    """Re-arrange the data as theta(time, longitude)
    """
    # Load the equivalent latitude data on PV2
    eqlats_cube, theta, eqlats = theta_pv2(infile)

    # Create a coordinate for latitude
    nlats = 81
    lat = np.linspace(10, 90, nlats)

    # Initialise the output
    ntimes, ntheta = eqlats.shape
    output = np.zeros([ntimes, nlats])

    # Search downward for the equivalent latitude value
    # Start at theta=400 K
    k_start = np.abs(theta - 400).argmin()
    for n in range(ntimes):
        print(n)
        for j in range(nlats):
            # Search downward
            k = k_start
            while eqlats[n, k] < lat[j] and k < ntheta:
                k += 1

            # Linearly interpolate to find theta
            alpha = ((lat[j] - eqlats[n, k]) /
                     (eqlats[n, k] - eqlats[n, k - 1]))

            output[n, j] = (alpha * theta[k] + (1 - alpha) * theta[k - 1])

    output = iris.cube.Cube(
        output, long_name='potential_temperature', units='K',
        dim_coords_and_dims=[(eqlats_cube.coord('time'), 0),
                             (iris.coords.DimCoord(lat, long_name='latitude',
                                                   units='degrees'), 1)])

    return output


def thetapv2_nae(infile):
    """Re-arrange the data as theta(time, grid_lat, grid_lon)
    """
    # Load the equivalent latitude data on PV2
    eqlats_cube, theta, eqlats = theta_pv2(infile)

    # Load the NAE grid
    cubes = iris.load(directory + '../iop5/diagnostics_024.nc')
    lat = grid.true_coords(cubes[0])[1]

    # Initialise the output
    nt, ntheta = eqlats.shape
    ny, nx = lat.shape
    output = np.zeros([nt, ny, nx])

    # Search downward for the equivalent latitude value
    # Start at theta=400 K
    k_start = np.abs(theta - 400).argmin()
    for n in range(nt):
        print(n)
        for j in range(ny):
            for i in range(nx):
                # Search downward
                k = k_start
                while eqlats[n, k] < lat[j, i] and k < ntheta:
                    k += 1

                # Linearly interpolate to find theta
                alpha = ((lat[j, i] - eqlats[n, k]) /
                         (eqlats[n, k] - eqlats[n, k - 1]))
                output[n, j, i] = (alpha * theta[k] +
                                   (1 - alpha) * theta[k - 1])

    output = iris.cube.Cube(
        output, long_name='potential_temperature', units='K',
        dim_coords_and_dims=[(eqlats_cube.coord('time'), 0),
                             (cubes[0].coord('grid_latitude'), 1),
                             (cubes[0].coord('grid_longitude'), 2)])

    return output


def plot_summary(cube, vmin=250, vmax=400, cmap='plasma', **kwargs):
    """Plot background theta on 2PVU vs latitude for full period
    """
    plot.pcolormesh(cube, vmin=vmin, vmax=vmax, cmap=cmap, **kwargs)

    return

if __name__ == '__main__':
    #main('2009', '11', '01', '00')
    #main('2011', '11', '23', '00')
    main('2013', '11', '01', '00')
