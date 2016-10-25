import iris
from iris.cube import CubeList
from iris.util import squeeze
from mymodule import calculus, convert, interpolate, grid, variable
from scripts.files import stash_maps


def load_cubes(filename, names):
    cubes = iris.load(filename)
    cubes = convert.calc(names, cubes)

    return cubes


def redo_cubes(cubes, basis_cube, stash_maps=[], slices=None, time=None):
    # Coordinates to copy to analyses
    z = grid.extract_dim_coord(basis_cube, 'z')

    # Define attributes of custom variables by stash mapping
    for stash_map in stash_maps:
        stash_map.remap_cubelist(cubes)

    newcubelist = CubeList()
    for cube in cubes:
        # Remove unneccessary time coordinates
        for coord in ['forecast_period', 'forecast_reference_time']:
            try:
                cube.remove_coord(coord)
            except iris.exceptions.CoordinateNotFoundError:
                pass

        if cube.ndim == 3:
            # Use the hybrid height coordinate as the main vertical coordinate
            try:
                cube.remove_coord('model_level_number')
            except iris.exceptions.CoordinateNotFoundError:
                pass
            cube.coord('level_height').rename(z.name())
            iris.util.promote_aux_coord_to_dim_coord(cube, z.name())

            # Remap the cubes to theta points
            newcube = interpolate.remap_3d(cube, basis_cube, z.name())

        # Convert the main time coordinate
        if time is not None:
            newcube.coord('time').convert_units(time)

        newcubelist.append(newcube)

    return newcubelist


def derived(cubes):
    # Extract variables
    u = cubes.extract('x_wind')[0]
    v = cubes.extract('y_wind')[0]
    w = cubes.extract('upward_air_velocity')[0]
    theta = cubes.extract('air_potential_temperature')[0]
    rho = cubes.extract('air_density')[0]

    # Vorticity
    xi_i, xi_j, xi_k = variable.vorticity(u, v, w)

    # Divergence
    div = calculus.div(u, v, w)
    div.rename('divergence')

    # PV using different calculation
    pv = variable.calc_pv(u, v, w, theta, rho)
    pv.rename('derived_pv')

    for cube in [xi_i, xi_j, xi_k, div, pv]:
        cubes.append(cube)

    return
