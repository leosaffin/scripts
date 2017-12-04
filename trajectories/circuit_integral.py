from datetime import timedelta
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.path import Path
import iris
import iris.plot as iplt
import iris.quickplot as qplt
from iris.analysis import SUM
from iris.analysis.cartography import unrotate_pole
from mymodule import convert, grid
from mymodule.user_variables import datadir, plotdir
from mymodule.constants import omega
from lagranto import caltra, trajectory, pyLagranto
from scripts import case_studies
from scripts.trajectories.cluster import select_cluster

a = 6378100

def main():
    names = ['dx', 'dy', 'dz', 'dlambda', 'length', 'relative_circulation',
             'planetary_circulation', 'absolute_circulation']
    units = ['m', 'm', 'm', 'm', 'm', 's^-1', 's^-1', 's^-1']
    
    # IOP5 (early start)
    forecast = case_studies.iop5_extended.copy()
    job = 'iop5_extended'
    name = 'isentropic_backward_trajectories_from_outflow_boundary'
    theta_level = 320
    
    # Load trajectories
    filename = datadir + job + '/' + name + '.pkl'
    trajectories = trajectory.load(filename)
    print len(trajectories)
    
    # Only include trajectories that stay in the domain
    #trajectories = trajectories.select('air_pressure', '>', 0)
    #print(len(trajectories))

    # Select an individual theta level
    dt1 = timedelta(hours=0)
    trajectories = trajectories.select(
        'air_potential_temperature', '>', theta_level-2.5, time=[dt1])
    trajectories = trajectories.select(
        'air_potential_temperature', '<', theta_level+2.5, time=[dt1])
    print len(trajectories)

    ntra = len(trajectories)
    levels = ('air_potential_temperature', [theta_level])

    results = iris.cube.CubeList()
    for n, cubes in enumerate(forecast):
        print n
        if n == 0:
            # Load grid parameters
            example_cube = convert.calc('upward_air_velocity', cubes,
                                        levels=levels)
            nx, ny, nz, xmin, ymin, dx, dy, hem, per, varnames = \
                caltra.grid_parameters(example_cube, levels)

            # Create a 1d array of points for determining which gripoints are
            # contained in the trajectory circuit when performing volume
            # integrals
            glon, glat = grid.get_xy_grids(example_cube)
            gridpoints = np.array([glon.flatten(), glat.flatten()]).transpose()
            cs = example_cube.coord_system()

        # Load trajectory positions -(n+2) because the trajectories are
        # backwards in time. +2 to skip the analysis which is not in the
        # forecast object (i.e. n=0 corresponds to idx=-2 in the trajectories)
        leftflag = (trajectories['air_pressure'][:, -(n+2)] < -0.).astype(int)
        x = trajectories.x[:, -(n+2)]
        y = trajectories.y[:, -(n+2)]
        z = trajectories['altitude'][:, -(n+2)]
        theta = trajectories['air_potential_temperature'][:, -(n+2)]
        r = a+z

        # Calculate enclosed area integrals
        integrals = mass_integrals(cubes, x, y, glat, gridpoints,
                                   nx, ny, theta_level)
        for icube in integrals:
            results.append(icube)

        # Load wind data at the current forecast time
        spt1, uut1, vvt1, wwt1, p3t1 = caltra.load_winds(cubes, levels)

        # Interpolate the wind fields to the trajectory waypoints
        u_wp = pyLagranto.trace.interp_to(
            uut1, x, y, theta, leftflag, p3t1, spt1, xmin, ymin,
            dx, dy, nx, ny, nz, ntra)
        v_wp = pyLagranto.trace.interp_to(
            vvt1, x, y, theta, leftflag, p3t1, spt1, xmin, ymin,
            dx, dy, nx, ny, nz, ntra)
        w_wp = pyLagranto.trace.interp_to(
            wwt1, x, y, theta, leftflag, p3t1, spt1, xmin, ymin,
            dx, dy, nx, ny, nz, ntra)
        
        # Convert to global coordinates in radians
        lon, lat = unrotate_pole(x, y, cs.grid_north_pole_longitude,
                                 cs.grid_north_pole_latitude)
        
        rlon = np.deg2rad(x)
        rlat = np.deg2rad(y)
        
        lon = np.deg2rad(lon)
        lat = np.deg2rad(lat)
        
        # Calculate the velocity due to Earth's rotation
        u_abs = omega.data * r * np.cos(lat)
        
        # Integrate around the circuit
        cintegrals = circuit_integrals(u_abs, u_wp, v_wp, w_wp, lon, lat, rlon, rlat, z, r)
        
        for n, value in enumerate(cintegrals):
            ccube = icube.copy(data=value)
            ccube.rename(names[n])
            ccube.units = units[n]
            results.append(ccube)
            
    iris.save(results.merge(),
              datadir + 'circulations_' + str(theta_level) + 'K.nc')
    
    return


def circuit_integrals(u_abs, u, v, w, lon, lat, glon, glat, z, r):
    # Integrate u.dl around the circuit of trajectories
    # 1st and last 2 trajectories are the same so don't double count
    dlambda, dx, dy, dz = [], [], [], []
    for n in range(1, len(u)-1):
        # dlambda is length along true longitudes to match the direction of
        # the Earth rotation
        dlambda.append(r[n] * np.cos(lat[n]) * 0.5 * (lon[n+1] - lon[n-1]))
        
        # dx and dy are in the direction of the rotated grid which corresponds
        # to the wind fields in the forecast
        dx.append(r[n] * np.cos(glat[n]) * 0.5 * (glon[n+1] - glon[n-1]))
        dy.append(r[n] * 0.5 * (glat[n+1] - glat[n-1]))
        
        # dz is independent of grid rotation
        dz.append(0.5 * (z[n+1] - z[n-1]))
        
    dlambda = np.array(dlambda)
    dx = np.array(dx)
    dy = np.array(dy)
    dz = np.array(dz)

    # \int dl: Tracks the errors in each calculation (should be zero)
    dx_tot = np.sum(dx)
    dy_tot = np.sum(dy)
    dz_tot = np.sum(dz)
    dlambda_tot = np.sum(dlambda)
    
    # \int |dl|
    length = np.sum(np.sqrt(dx ** 2 + dy ** 2 + dz ** 2))
    
    # u * r cos(phi) dlambda
    circ_u = u[1:-1] * dx
                   
    # v * r dphi
    circ_v = v[1:-1] * dy
        
    # w * dz
    circ_w = w[1:-1] * dz
    
    # u_abs * r cos(phi) dlambda
    circ_p = u_abs[1:-1] * dlambda
    """
    r_ave = 0.5 * (r[1:] + r[:-1])

    dlambda = r_ave * np.cos(0.5 * (lat[1:] + lat[:-1])) * (lon[1:] - lon[:-1])
    dx = r_ave * np.cos(0.5 * (glat[1:] + glat[:-1])) * (glon[1:] - glon[:-1])
    dy = r_ave * (glat[1:] - glat[:-1])
    dz = (z[1:] - z[:-1])

    # \int dl
    dx_tot = np.sum(dx)
    dy_tot = np.sum(dy)
    dz_tot = np.sum(dz)
    dlambda_tot = np.sum(dlambda)

    # \int |dl|
    length = np.sum(np.sqrt(dx ** 2 + dy ** 2 + dz ** 2))

    # u * r cos(phi) dlambda
    circ_u = 0.5 * (u[1:] + u[:-1]) * dx

    # v * r dphi
    circ_v = 0.5 * (v[1:] + v[:-1]) * dy

    # w * dz
    circ_w = 0.5 * (w[1:] + w[:-1]) * dz

    # u_abs * r cos(phi) dlambda
    circ_p = 0.5 * (u_abs[1:] + u_abs[:-1]) * dlambda
    """

    rel_circulation = np.sum(circ_u + circ_v + circ_w)
    planetary_circulation = np.sum(circ_p)
    abs_circulation = np.sum(circ_u + circ_v + circ_w + circ_p)

    return dx_tot, dy_tot, dz_tot, dlambda_tot, length, rel_circulation, planetary_circulation, abs_circulation


def mass_integrals(cubes, x, y, glat, gridpoints, nx, ny, theta_level):
    # Include points within circuit boundary
    points = np.array([x, y]).transpose()
    pth = Path(points)
    
    # Mask all points that are not contained in the circuit
    mask = np.logical_not(pth.contains_points(gridpoints).reshape([ny, nx]))

    # Area = r**2 cos(phi) dlambda dphi
    levels=('air_potential_temperature',
            [theta_level-2.5, theta_level, theta_level+2.5])
    zth = convert.calc('altitude', cubes, levels=levels)
    area = (a + zth[1])**2 * np.cos(np.deg2rad(glat)) * np.deg2rad(0.11)**2
    area.units = 'm^2'
    area.rename('area')
    total_area = integrate(area, mask)
    
    # Volume = area * dz
    volume = area * (zth[2] - zth[0])
    volume.rename('volume')
    total_volume = integrate(volume, mask)
    
    # Mass density * volume
    levels=('air_potential_temperature', [theta_level])
    density = convert.calc('air_density', cubes, levels=levels)[0]
    mass = density * volume
    mass.rename('mass')
    total_mass = integrate(mass, mask)
    
    # Circulation = \int rho.pv.dv
    pv = convert.calc('ertel_potential_vorticity', cubes, levels=levels)[0]
    pv_substance = pv * mass
    circulation = integrate(pv_substance, mask)
    
    # Convert from PVU to SI units and divide by dtheta=5K
    circulation = circulation * 1e-6 / 5
    
    circulation.rename('mass_integrated_circulation')
    
    return total_area, total_volume, total_mass, circulation


def integrate(cube, mask):
    cube = cube.copy()
    cube.data = np.ma.masked_where(mask, cube.data)
    result = cube.collapsed(['grid_longitude', 'grid_latitude'], SUM)
    
    return result


def load_from_files():
    cubes = iris.load(datadir + 'circulations_320K.nc')
    plot_timeseries(cubes)
    return


def plot_timeseries(cubes):
    for cube in cubes:
        if 'circulation' in cube.name():
            iplt.plot(cube, label=cube.name())
    
    plt.legend(ncol=2, loc='best')
    plt.savefig(plotdir + 'circulation.png')
    

    for cube in cubes:
        if 'circulation' not in cube.name():
            plt.figure()
            qplt.plot(cube)
            plt.savefig(plotdir + cube.name() + '.png')
    
    plt.show()

    return


if __name__=='__main__':
    main()
    load_from_files()
    
