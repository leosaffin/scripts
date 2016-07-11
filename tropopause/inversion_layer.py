import numpy as np
import matplotlib.pyplot as plt
import iris.plot as iplt
from mymodule import convert, diagnostic, grid, interpolate, variable
from mymodule.detection import rossby_waves
from scripts import case_studies

pvtrop = 3.5
pvname = 'ertel_potential_vorticity'
dz = np.linspace(-3000, 3000, 25)


def main(cubes):
    """
    """
    # Calulate N^2
    theta = convert.calc('air_potential_temperature', cubes)
    nsq = variable.N_sq(theta)

    # Find the tropopause
    z = grid.make_cube(theta, 'altitude')
    pv = grid.make_coord(convert.calc(pvname, cubes))
    z.add_aux_coord(pv, [0, 1, 2])
    ztrop = interpolate.to_level(z, **{pvname: [pvtrop]})[0]

    # Mask ridges and troughs
    theta.add_aux_coord(pv, [0, 1, 2])
    theta_pv = interpolate.to_level(theta, **{pvname: [pvtrop]})[0]
    ridges, troughs = rossby_waves.make_nae_mask(theta_pv)

    # Create profile of N_sq vs tropopause
    weights = grid.volume(theta)
    zbin = theta.copy(data=z.data - ztrop.data)
    for name, mask in [('troughs', ridges), ('ridges', troughs)]:
        nmask = mask * np.ones_like(theta.data)
        #cube = diagnostic.profile(nsq, ztrop, dz, mask=mask)[0]
        cube = diagnostic.averaged_over(nsq, dz, zbin, weights, mask=nmask)[0]
        iplt.plot(cube, cube.coords()[0], label=name)

    plt.axhline(color='k', marker='', linewidth=1)
    plt.axvline(color='k', marker='', linewidth=1)
    plt.xlabel(r'$N^2$ $s^{-1}$')
    plt.ylabel('Distance from the tropopause')
    plt.legend(loc='best')
    plt.title('Tropopause PV = %.1f' % pvtrop)
    plt.show()

if __name__ == '__main__':
    forecast = case_studies.iop8()
    cubes = forecast.set_lead_time(hours=36)
    main(cubes)
