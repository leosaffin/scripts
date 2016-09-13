import iris
from iris.cube import CubeList
from mymodule import convert, interpolate, grid, variable
from scripts.files import stash_maps


def main():
    # Filename parameters
    strlen = 3
    inpath = '/projects/diamet/lsaffi/xjjhq/xjjhqa_p'
    outpath = '/projects/diamet/lsaffi/temp/'
    time = 'hours since 2011-11-28 12:00:00'

    # Load grid orography
    z_0 = iris.load('/projects/diamet/lsaffi/nae_orography.nc')[0][0, 0]
    orog = grid.make_coord(z_0)

    # Define which area of grid to subset
    slices = slice(0, 50), slice(15, 345), slice(15, 585)

    for n in range(36):
        print n
        # Tracers
        infile = inpath + 'a' + str(n).zfill(strlen)
        outfile = outpath + 'pv_tracers_' + str(n + 1).zfill(strlen)
        tracers(infile, outfile, stash_maps=[stash_maps.pv_tracers],
                orography=orog, slices=slices, time=time)

        # Prognostics
        nddiag_name = inpath + 'b' + str(n).zfill(strlen)
        progs_name = inpath + 'c' + str(n).zfill(strlen)
        outfile = outpath + 'prognostics_' + str(n + 1).zfill(strlen)
        prognostics(nddiag_name, progs_name, outfile, orography=orog,
                    slices=slices, time=time)

        # Diagnostics
        infile = inpath + 'd' + str(n).zfill(strlen)
        outfile = outpath + 'diagnostics_' + str(n + 1).zfill(strlen)
        diagnostics(infile, outfile, slices=slices[1:], time=time)


def ff2nc(infile, outfile, **kwargs):
    cubes = iris.load(infile)

    cubes = redo_cubes(cubes, **kwargs)

    iris.save(cubes, outfile + '.nc')


def tracers(infile, outfile, **kwargs):
    cubes = iris.load(infile)

    cubes = redo_cubes(cubes, **kwargs)

    iris.save(cubes, outfile + '.nc')


def prognostics(nddiag_name, progs_name, outfile, **kwargs):
    cubes = CubeList()

    # Extract u, v, w, q, q_cl and q_cf from the NDdiag file
    _nddiag(cubes, nddiag_name)

    # Extract rho, theta and exner on theta levels from prognostics file
    _prognostics(cubes, progs_name)

    cubes = redo_cubes(cubes, **kwargs)

    iris.save(cubes, outfile + '.nc')


def diagnostics(infile, outfile, **kwargs):
    cubes = iris.load(infile)

    cubes = convert.calc(['boundary_layer_type',
                          'air_pressure_at_sea_level',
                          'atmosphere_boundary_layer_thickness',
                          'convective_rainfall_amount',
                          'stratiform_rainfall_amount'], cubes)

    cubes = redo_cubes(cubes, **kwargs)

    iris.save(cubes, outfile + '.nc')


def redo_cubes(cubes, stash_maps=[], orography=None, slices=None, time=None):
    # Define attributes of custom variables by stash mapping
    for stash_map in stash_maps:
        stash_map.remap_cubelist(cubes)

    for cube in cubes:
        # Remove unneeded attributes
        cube.attributes = {}

        try:
            # Use the hybrid height coordinate as the main vertical coordinate
            cube.remove_coord('model_level_number')
            iris.util.promote_aux_coord_to_dim_coord(cube, 'level_height')

            # Add hybrid height coordinates
            if orography is not None:
                cube.add_aux_coord(orography, [1, 2])
                grid.add_hybrid_height(cube)

        except iris.exceptions.CoordinateNotFoundError:
            # Coordinate not found for 2d cubes
            pass

        # Remove unneccessary time coordinates
        for coord in ['forecast_period', 'forecast_reference_time']:
            cube.remove_coord(coord)

        # Convert the main time coordinate
        if time is not None:
            cube.coord('time').convert_units(time)

    return CubeList([cube[slices] for cube in cubes])


def _nddiag(newcubes, filename):
    # Load the cubes
    cubes = iris.load(filename)

    # Extract w to use grid dimensions
    w = convert.calc('upward_air_velocity', cubes)
    newcubes.append(w)

    # u and v are staggered on rho-levels
    for name in ('x_wind', 'y_wind'):
        cube = convert.calc(name, cubes)
        cube = interpolate.remap_3d(cube, w, 'level_height')
        newcubes.append(cube)

    # Simply copy across cubes on theta levels
    for name in ('specific_humidity',
                 'mass_fraction_of_cloud_liquid_water_in_air',
                 'mass_fraction_of_cloud_ice_in_air'):
        cube = convert.calc(name, cubes)
        newcubes.append(cube)

    for cube in newcubes:
        cube.remove_coord('surface_altitude')

    return


def _prognostics(newcubes, filename):
    # Load the cubes
    cubes = iris.load(filename)

    # Extract theta
    theta = convert.calc('air_potential_temperature', cubes)

    # Remap rho to theta-levels
    rho = convert.calc('unknown', cubes)
    rho.rename('air_density')
    rho.units = 'kg m-3'
    rho = interpolate.remap_3d(rho, theta, 'level_height')

    # Extract exner on theta levels (ignore on rho levels)
    exner = cubes.extract('dimensionless_exner_function')[1]

    # Add the prognostics to the newcubelist
    [newcubes.append(cube) for cube in [rho, theta, exner]]

    return


if __name__ == '__main__':
    main()
