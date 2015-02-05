# Define the directory with output data
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

