import iris
directory='/projects/diamet/lsaffi/'

# Define the List of Names in the Tracer Files for Each Run
names = {}

# IOP5 - NAE
names['xjjho'] = ['Advection Only PV',
                  'Short Wave Radiation PV',
                  'Long Wave Radiation PV',
                  'Radiation PV',
                  'Microphysics PV',
                  'Gravity Wave Drag PV',
                  'Convection PV',
                  'Boundary Layer PV',
                  'Atmospheric Physics 1 PV',
                  'Atmospheric Physics 2 PV',
                  'Pressure Solver PV',
                  'Advection Inconsistency PV',
                  'Cloud Rebalancing PV',
                  'Total PV']

# IOP5 - Global
names['xjjhz'] = names['xjjho']
# Debug
names['xjjhb'] = names['xjjho']
# IOP8 - NAE
names['xkcqa'] = ['Advection Only PV',
                  'Short Wave Radiation PV',
                  'Long Wave Radiation PV',
                  'Radiation PV',
                  'Microphysics PV',
                  'Gravity Wave Drag PV',
                  'Convection PV',
                  'Boundary Layer PV',
                  'Boundary Layer and Radiation PV'
                  'Atmospheric Physics 1 PV',
                  'Atmospheric Physics 2 PV',
                  'Pressure Solver PV',
                  'Advection Inconsistency PV',
                  'Update Fields PV'
                  'Cloud Rebalancing PV',
                  'Total PV']


# Load Tracers and Prognostics in one cubelist
def all(job,lead_time,**kwargs):
    # Load tracers
    cubes1 = tracers(job,lead_time)
    # Load prognostics
    cubes2 = prognostics(job,lead_time)
    # Add co-ordinate information from prognostics to tracers
    if 'theta_cube' in kwargs:
        cubes1 = replace_coord(cubes1,cubes2[kwargs['theta_cube']])
    return cubes1+cubes2

# Load tracers in cubelist
def tracers(job,lead_time):
    tstep = str(lead_time-1).zfill(3)
    filename = directory + job + '/' + job + 'a_pa' + tstep
    cubes = iris.load(filename)

    if lead_time == 1:
    # First File Contains 0th Timestep
    # Only Take 1st Timestep
        time_coord = cubes[0].coord('time').points[1]
        cubes = cubes.extract(iris.Constraint(time = time_coord))
    
    for [i,name] in enumerate(names[job]):
        # Convert PV tracers To PVU
        cubes[i] = cubes[i]*1e6
        cubes[i].units = iris.unit.Unit('PVU')
        # Add Names to Traces
        cubes[i].rename(name)
    return cubes

# Load prognostics in cubelist
def prognostics(job,lead_time):
    tstep = str(lead_time-1).zfill(3)
    filename = directory + job + '/' + job + 'a_pb' + tstep
    cubes = iris.load(filename)
    if lead_time == 1:
    # First File Contains 0th Timestep
    # Only Take 1st Timestep
        time_coord = cubes[0].coord('time').points[1]
        cubes = cubes.extract(iris.Constraint(time = time_coord))
    for i,cube in enumerate(cubes):
        if 'pressure' in cube.name():
            cubes[i].convert_units('hPa')
    return cubes

# Add co-ordinate informate from coord_cube to cubes in the cubelist
def replace_coord(cubelist,coord_cube):
    # Load theta-level information from prognostics
    for cube in cubelist:
        # Add extra co-ordinate information
        cube.add_aux_coord(coord_cube.coord('surface_altitude'),[1,2])
        cube.add_aux_factory(coord_cube.aux_factory('altitude'))
    return cubelist

def extract(cubes,name):
    if name == 'Total Minus Advection Only PV':
        cube = (cubes.extract('Total PV')[0] -
                cubes.extract('Advection Only PV')[0])
    elif name == 'Sum of PV Tracers':
        cube = (cubes.extract('Atmospheric Physics 1 PV')[0] +
                cubes.extract('Atmospheric Physics 2 PV')[0])
    elif name == 'Residual Error':
        cube = (cubes.extract('Total PV')[0] -
                cubes.extract('Advection Only PV')[0] -
                cubes.extract('Atmospheric Physics 1 PV')[0] -
                cubes.extract('Atmospheric Physics 2 PV')[0] -
                cubes.extract('Cloud Rebalancing PV')[0] -
                cubes.extract('Pressure Solver PV')[0] -
                cubes.extract('Advection Inconsistency PV')[0])
    elif name == 'Other PV Tracers':
        cube = (cubes.extract('Cloud Rebalancing PV')[0] +
                cubes.extract('Pressure Solver PV')[0])
    elif name == 'Error':
        cube = (cubes.extract('Total PV')[0] -
                cubes.extract('Advection Only PV')[0] -
                cubes.extract('Atmospheric Physics 1 PV')[0] -
                cubes.extract('Atmospheric Physics 2 PV')[0] -
                cubes.extract('Cloud Rebalancing PV')[0] -
                cubes.extract('Pressure Solver PV')[0])
    else:
        cube = cubes.extract(name)[0]
    return cube

import trajectories
# Loads information from a Lagranto output file
def lagranto(filename):
    # Initialise a trajectory list
    trajectories_list = []
    with open(filename,'r') as data:
        # Skip Lines
        data.readline()
        data.readline()
        # Read Header
        header = data.readline().split()
        # Skip Lines
        data.readline()
        # Read main data
        for line in data:
            try:
                trajectories_list[-1].add_data(line.split(),header)
            # Blank Line - Next trajectory
            except IndexError:
                trajectories_list.append(trajectories.Trajectory())
    return trajectories_list
