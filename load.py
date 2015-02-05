import iris
from constants import directory,names
# Load Tracers and Prognostics in one cubelist
def all(job,lead_time,**kwargs):
    # Load prognostics
    progs = prognostics(job,lead_time)
    # Load tracers
    if 'coord_cube' in kwargs:
        tracer_cubes = tracers(job,lead_time,
                               coord_cube = progs[kwargs['coord_cube']])
    else:
        tracer_cubes = tracers(job,lead_time)
    return tracer_cubes + progs

# Load tracers in cubelist
def tracers(job,lead_time,**kwargs):
    tstep = str(lead_time-1).zfill(3)
    filename = directory + job + '/' + job + 'a_pa' + tstep
    cubes = iris.load(filename)

    if lead_time == 1:
    # First File Contains 0th Timestep
    # Only Take 1st Timestep
        time_coord = cubes[0].coord('time').points[1]
        cubes = cubes.extract(iris.Constraint(time = time_coord))

    if 'coord_cube' in kwargs:
        cubes = replace_coords(cubes,kwargs['coord_cube'])
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
def replace_coords(cubelist,coord_cube):
    # Loop over cubes to be substituted
    for n in xrange(len(cubelist)):
        # Make a new cube with the old cube information and new cube data
        cubelist[n] = coord_cube.copy(data=cubelist[n].data)
    return cubelist

# Same as replace coords but for a single cube
def replace_coord(cube,coord_cube):
    return coord_cube.copy(data=cube.data)

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
