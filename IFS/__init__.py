from mymodule.user_variables import datadir

datadir = datadir + 'openIFS/'

tendencies = {
    'var91': {'name': 'u tendency due to dynamics', 'units': 'm s-1'},
    'var92': {'name': 'v tendency due to dynamics', 'units': 'm s-1'},
    'var93': {'name': 'T tendency due to dynamics', 'units': 'K'},
    'var94': {'name': 'q tendency due to dynamics', 'units': ''},
    'var95': {'name': 'T tendency due to radiation', 'units': 'K'},
    'var96': {'name': 'u tendency due to orographic gravity wave drag',
              'units': 'm s-1'},
    'var97': {'name': 'v tendency due to orographic gravity wave drag',
              'units': 'm s-1'},
    'var98': {'name': 'u tendency due to vertical diffusion',
              'units': 'm s-1'},
    'var99': {'name': 'v tendency due to vertical diffusion',
              'units': 'm s-1'},
    'var100': {'name': 'T tendency due to vertical diffusion',
               'units': 'K'},
    'var101': {'name': 'q tendency due to vertical diffusion',
               'units': ''},
    'var102': {'name': 'u tendency due to convection', 'units': 'm s-1'},
    'var103': {'name': 'v tendency due to convection', 'units': 'm s-1'},
    'var104': {'name': 'T tendency due to convection', 'units': 'K'},
    'var105': {'name': 'q tendency due to convection', 'units': ''},
    'var106': {'name': 'u tendency due to spectral backscatter',
               'units': 'm s-1'},
    'var107': {'name': 'v tendency due to spectral backscatter',
               'units': 'm s-1'},
    'var108': {'name': 'T tendency due to cloud', 'units': 'K'},
    'var109': {'name': 'q tendency due to cloud', 'units': ''},
    'var110': {'name': 'u tendency due to non orographic gravity wave drag',
               'units': 'm s-1'},
    'var111': {'name': 'v tendency due to non orographic gravity wave drag',
               'units': 'm s-1'},
    'var112': {'name': 'u tendency due to sppt', 'units': 'm s-1'},
    'var113': {'name': 'v tendency due to sppt', 'units': 'm s-1'},
    'var114': {'name': 'T tendency due to sppt', 'units': 'K'},
    'var116': {'name': 'q tendency due to sppt', 'units': ''},
    'var117': {'name': 'T tendency due to adjustments', 'units': 'K'},
    'var118': {'name': 'q tendency due to adjustments', 'units': ''},
}


def replace_names(cubes):
    for cube in cubes:
        name = cube.name()
        if name in tendencies:
            cube.units = tendencies[name]['units']
            cube.rename(tendencies[name]['name'])

    return
