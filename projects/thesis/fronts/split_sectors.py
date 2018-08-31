import numpy as np
import matplotlib.pyplot as plt
import iris.plot as iplt
from mymodule import convert, grid, plot
from myscripts import case_studies


def main(cubes):
    lon, lat = grid.true_coords(cubes[0])
    z300 = convert.calc('altitude', cubes,
                        levels=('equivalent_potential_temperature', [300]))[0]
    z300.convert_units('km')
    mslp = convert.calc('air_pressure_at_sea_level', cubes)
    mslp.convert_units('hPa')

    # Plot overview
    plot.contourf(z300, np.linspace(0, 10, 11))
    cs = iplt.contour(mslp, np.linspace(950, 1050, 11), colors='k')
    plt.clabel(cs, fmt='%1.0f')

    # Warm Sector
    warm_sector = z300.data.mask
    plim = mslp.data < 1000
    loc = np.logical_and(lon > -10, lon < 5)
    ws_mask = np.logical_and(np.logical_and(warm_sector, loc), plim)
    ws_mask = mslp.copy(data=ws_mask)
    iplt.contour(ws_mask, linestyles='--', colors='r')

    # Cold Sector
    cold_sector = z300.data < 5
    loc = np.logical_and(loc, lat < 65)
    cs_mask = np.logical_and(np.logical_and(cold_sector, loc), plim)
    cs_mask = mslp.copy(data=cs_mask)
    iplt.contour(cs_mask, linestyles='--', colors='b')

    plt.title(r'$z(\theta_e = 300)$')

    return


def composite(cubes):
    lon, lat = grid.true_coords(cubes[0])
    theta_e = convert.calc('equivalent_potential_temperature', cubes)
    mslp = convert.calc('air_pressure_at_sea_level', cubes)
    mslp.convert_units('hPa')
    mass = convert.calc('mass', cubes)

    # Warm Sector
    warm_sector = theta_e.data > 300
    plim = mslp.data < 1000
    loc = np.logical_and(lon > -10, lon < 5)
    ws_mask = np.logical_and(np.logical_and(warm_sector, loc), plim)
    ws_mask = theta_e.copy(data=ws_mask)

    for n in range(20):
        c = (n + 1) / 20
        iplt.contour(ws_mask[n], linestyles=':',
                     colors=[(c, c, c)])

    plt.show()
    return


if __name__ == '__main__':
    forecast = case_studies.iop5b.copy()
    cubes = forecast.set_lead_time(hours=24)
    main(cubes)
    plt.figure()
    composite(cubes)
