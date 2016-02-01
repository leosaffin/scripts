import matplotlib.pyplot as plt
from mymodule import files, convert, grid, interpolate, plot


def main(cubes):
    """Calculate and plot the distance from the tropopause to cloud
    """
    # Get altitude as a cube
    pv = convert.calc('ertel_potential_vorticity', cubes)
    z = grid.make_cube(pv, 'altitude')
    pv = grid.make_coord(pv)

    # rh = convert.calc('mass_fraction_of_cloud_liquid_water_in_air', cubes)
    rh = convert.calc('mass_fraction_of_cloud_ice_in_air', cubes)
    # rh = convert.calc('relative_humidity', cubes)
    rh = grid.make_coord(rh)

    z.add_aux_coord(pv, [0, 1, 2])
    z.add_aux_coord(rh, [0, 1, 2])

    # Calculate the height of the tropopause
    z_pv2 = interpolate.to_level(z, ertel_potential_vorticity=[2])[0]

    # Calculate the height of the cloud top
    z_cloud = interpolate.to_level(
        z, mass_fraction_of_cloud_ice_in_air=[0.000001])[0]

    # Calculate the distance between cloud and tropopause
    dz = z_pv2.data - z_cloud.data
    dz = z_pv2.copy(data=dz)

    # Plot
    plot.pcolormesh(dz)
    plt.show()

if __name__ == '__main__':
    cubes = files.load('datadir/xjjhq/xjjhq_036.pp')
    main(cubes)
