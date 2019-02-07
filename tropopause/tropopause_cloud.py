import matplotlib.pyplot as plt
from irise import convert, grid, interpolate, plot
from myscripts.models.um import case_studies


def main(cubes, **kwargs):
    """Calculate and plot the distance from the tropopause to cloud
    """
    pv = convert.calc('ertel_potential_vorticity', cubes)
    cl = convert.calc('mass_fraction_of_cloud', cubes)

    # Get altitude as a cube
    z = grid.make_cube(pv, 'altitude')

    # Add pv and cloud as coordinates to the altitude cube
    pv = grid.make_coord(pv)
    z.add_aux_coord(pv, [0, 1, 2])
    cl = grid.make_coord(cl)
    z.add_aux_coord(cl, [0, 1, 2])

    # Calculate the height of the cloud top
    z_cloud = interpolate.to_level(z, mass_fraction_of_cloud=[1e-5])[0]

    # Calculate the height of the tropopause
    z_pv2 = interpolate.to_level(z, ertel_potential_vorticity=[2])[0]

    # Calculate the distance from tropopause to cloud
    dz = z_pv2.data - z_cloud.data
    dz = z_pv2.copy(data=dz)

    # Plot
    plot.pcolormesh(dz, **kwargs)
    plt.show()


if __name__ == '__main__':
    forecast = case_studies.iop8()
    cubes = forecast.set_lead_time(hours=36)
    main(cubes, vmin=0, vmax=5000, cmap='plasma_r')
