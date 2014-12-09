import numpy.f2py as f2py

# Source File Name
fname = 'fortran/grid.f'
# Output Module Name
mname = 'fgrid'
# Compiler Flages
flags = ''

# Open Source File
fid = open(fname)
source = fid.read()
fid.close()

# Compile Fortran Code Into Python Module
f2py.compile(source, modulename=mname, extra_args=flags)


