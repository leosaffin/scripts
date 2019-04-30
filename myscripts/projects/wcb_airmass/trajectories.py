import datetime
import numpy as np
import matplotlib.pyplot as plt
import iris
from lagranto import caltra
from irise import convert, grid, interpolate, plot
from irise.diagnostics import rossby_waves
from myscripts import datadir


def main():
    # Set up the mapping of times to files:
    path = datadir + 'iop5_global/'
    start_time = datetime.datetime(2011, 11, 28, 12)
    mapping = {start_time: path + '20111128_analysis12.nc'}
    for n in range(1, 49):
        time = start_time + datetime.timedelta(hours=n)
        mapping[time] = datadir + '*_' + str(n).zfill(3) + '.nc'

    return


def forward_trajectories(forecast):
    """Calculate 48 hour forward trajectories from low levels

    Start trajectories from all points below 2km
    """
    cubes = forecast.set_lead_time(hours=48)

    z = convert.calc('altitude', cubes)
    theta = convert.calc('air_potential_temperature', cubes)
    theta_adv = convert.calc('advection_only_theta', cubes)
    pv = convert.calc('ertel_potential_vorticity', cubes)
    lon, lat = grid.true_coords(pv)
    glon, glat = grid.get_xy_grids(pv)
    time = grid.get_datetime(pv)
    nz, ny, nx = pv.shape

    eqlats = rossby_waves.eqlats
    cs = iris.Constraint(time=time)
    with iris.FUTURE.context(cell_datetime_objects=True):
        eqlat = eqlats.extract(cs)[0]

    # Interpolate to the theta and PV surfaces
    eqlat = interpolate.main(eqlat, ertel_potential_vorticity=2)
    eqlat = interpolate.main(eqlat,
                             potential_temperature=theta.data.flatten())

    # Define the start points
    trainp = []
    for k in range(nz):
        print(k)
        for j in range(ny):
            for i in range(nx):
                if (theta_adv.data[k, j, i] < 300 < theta.data[k, j, i] and
                        pv.data[k, j, i] < 2 and
                        lat[j, i] > eqlat.data[k * ny * nx + j * nx + i]):
                    trainp.append([glon[j, i], glat[j, i], z.data[k, j, i]])
    trainp = np.array(trainp)

    plot.pcolormesh(pv[33], vmin=0, vmax=10, cmap='cubehelix_r', pv=pv[33])
    plt.scatter(trainp[:, 0], trainp[:, 1])
    plt.show()

    # Calculate the trajectories
    tracers = ['air_potential_temperature', 'air_pressure']
    traout = caltra.caltra(trainp, mapping, fbflag=-1, tracers=tracers)

    # Save the trajectories
    traout.save(datadir + 'backward_trajectories.pkl')


def backward_3d_trajectories_from_outflow():
    """Calculate 3d backward trajectories from defined outflow region
    """
    return


def backward_isentropic_trajectories_from_outflow():
    """Calculate isentropic backward trajectories around boundary of the outflow
    """

    traout = caltra.caltra(trainp, mapping, fbflag=-1, tracers=tracers,
                           levels=('air_potential_temperature', [320]))
    return


if __name__ == '__main__':
    main()
