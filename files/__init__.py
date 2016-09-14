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

    for cube in cubes:
        # Squeeze cubes dimensions
        newcube = squeeze(cube)

        # Remove unneccessary time coordinates
        for coord in ['forecast_period', 'forecast_reference_time']:
            cube.remove_coord(coord)

        try:
            # Use the hybrid height coordinate as the main vertical coordinate
            newcube.remove_coord('model_level_number')
            iris.util.promote_aux_coord_to_dim_coord(cube, 'level_height')
            cube.coord('level_height').rename(z.name())

            # Remap the cubes to theta points
            newcube = interpolate.remap_3d(newcube, basis_cube, z.name())

        except iris.exceptions.CoordinateNotFoundError:
            # Coordinate not found for 2d cubes
            pass

        # Convert the main time coordinate
        if time is not None:
            cube.coord('time').convert_units(time)

    return CubeList([cube[slices] for cube in cubes])
