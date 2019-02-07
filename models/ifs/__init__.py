from myscripts import datadir, plotdir
from irise.plot.util import PlotParameter

datadir = datadir + 'openIFS/'
plotdir = plotdir + 'openIFS/'

physics_schemes = {
    'Physics':
        PlotParameter(color='k', linestyle='-',  idx=0),
    'Short-Wave Radiation':
        PlotParameter(color='r', linestyle=':',  idx=1),
    'Long-Wave Radiation':
        PlotParameter(color='r', linestyle='--', idx=2),
    'Radiation':
        PlotParameter(color='r', linestyle='-',  idx=3),
    'Vertical Diffusion':
        PlotParameter(color='g', linestyle='-',  idx=4),
    'Orographic Gravity-Wave Drag':
        PlotParameter(color='g', linestyle='--', idx=5),
    'Non-Orographic Gravity-Wave Drag':
        PlotParameter(color='g', linestyle=':',  idx=6),
    'Convection':
        PlotParameter(color='b', linestyle='--', idx=7),
    'Precipitation':
        PlotParameter(color='b', linestyle='-',  idx=8),
    'SPPT':
        PlotParameter(color='k', linestyle='--', idx=9),
}

tendencies = {
    'var91': {'name': 'u_tendency_due_to_dynamics', 'units': 'm s-1'},
    'var92': {'name': 'v_tendency_due_to_dynamics', 'units': 'm s-1'},
    'var93': {'name': 'T_tendency_due_to_dynamics', 'units': 'K'},
    'var94': {'name': 'q_tendency_due_to_dynamics', 'units': ''},
    'var95': {'name': 'T_tendency_due_to_radiation', 'units': 'K'},
    'var96': {'name': 'u_tendency_due_to_orographic_gravity_wave_drag',
              'units': 'm s-1'},
    'var97': {'name': 'v_tendency_due_to_orographic_gravity_wave_drag',
              'units': 'm s-1'},
    'var98': {'name': 'u_tendency_due_to_vertical_diffusion',
              'units': 'm s-1'},
    'var99': {'name': 'v_tendency_due_to_vertical_diffusion',
              'units': 'm s-1'},
    'var100': {'name': 'T_tendency_due_to_vertical_diffusion',
               'units': 'K'},
    'var101': {'name': 'q_tendency_due_to_vertical_diffusion',
               'units': ''},
    'var102': {'name': 'u_tendency_due_to_convection', 'units': 'm s-1'},
    'var103': {'name': 'v_tendency_due_to_convection', 'units': 'm s-1'},
    'var104': {'name': 'T_tendency_due_to_convection', 'units': 'K'},
    'var105': {'name': 'q_tendency_due_to_convection', 'units': ''},
    'var106': {'name': 'u_tendency_due_to_spectral_backscatter',
               'units': 'm s-1'},
    'var107': {'name': 'v_tendency_due_to_spectral_backscatter',
               'units': 'm s-1'},
    'var108': {'name': 'T_tendency_due_to_cloud', 'units': 'K'},
    'var109': {'name': 'q_tendency_due_to_cloud', 'units': ''},
    'var110': {'name': 'u_tendency_due_to_non_orographic_gravity_wave_drag',
               'units': 'm s-1'},
    'var111': {'name': 'v_tendency_due_to_non_orographic_gravity_wave_drag',
               'units': 'm s-1'},
    'var112': {'name': 'u_tendency_due_to_sppt', 'units': 'm s-1'},
    'var113': {'name': 'v_tendency_due_to_sppt', 'units': 'm s-1'},
    'var114': {'name': 'T_tendency_due_to_sppt', 'units': 'K'},
    'var116': {'name': 'q_tendency_due_to_sppt', 'units': ''},
    'var117': {'name': 'T_tendency_due_to_adjustments', 'units': 'K'},
    'var118': {'name': 'q_tendency_due_to_adjustments', 'units': ''},
}


def replace_names(cubes):
    for cube in cubes:
        name = cube.name()
        if name in tendencies:
            cube.units = tendencies[name]['units']
            cube.rename(tendencies[name]['name'])

    return
