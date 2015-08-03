import numpy.f2py as f2py

# Source File Name
filename = 'fronts.f'
# Output Module Name
modulename = 'ffronts'
# Compiler Flags
flags = ''

# Open Source File
with open(filename) as code:
    source = code.read()


# Compile Fortran Code Into Python Module
f2py.compile(source, modulename=modulename, extra_args=flags)
