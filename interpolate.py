import numpy as np
import iris

# Interpolate {field} to pressure levels defined in {prange}
# {field} and {pressure} are defined on the same levels
# Pressure is assumed to vary logarithmically with height
# consistent with interpolation in NDdiag 
def any_to_pressure(field,pressure,prange):
    # Catch the excepting situation where prange is just a single level
    try:
        npres = len(prange)
    except TypeError:
        npres = 1
        prange = [prange]

    # Extract data from cubes if the input is defined that way
    try:
        is_cube = field.is_compatible(field)
        cube = field
        field = field.data
        pressure = pressure.data
    except AttributeError:
        is_cube = False

    # Allocate the output field
    [nz,ny,nx] = field.shape
    newfield = np.zeros(((npres,ny,nx)))
    for l,p in enumerate(prange):
        for j in xrange(0,ny):
            for i in xrange(0,nx):
                # Leave field as zero if the pressure level 
                # is outside the boundary 
                if(p>pressure[-1,j,i] and p<pressure[0,j,i]):
                    # Find the index of the nearest pressure point
                    # greater than the pressure level
                    k = (pressure[:,j,i] - prange[l]).clip(0).argmin()
                    # Determine the weighting coefficient between the bounding
                    # levels
                    alpha = (np.log(prange[l]      /pressure[k-1,j,i])/
                             np.log(pressure[k,j,i]/pressure[k-1,j,i]))
                    # Interpolate to find the new value
                    newfield[l,j,i] = (alpha*field[k,j,i] + 
                                       (1-alpha)*field[k-1,j,i])
    # If input was defined as cubes copy across metadata
    if is_cube:
        newfield = iris.cube.Cube(newfield)
        newfield.rename(cube.name())
        newfield._units = cube._units
        # Add Co-ordinates to cube
        for i,coord in enumerate(cube.dim_coords):
            try:
                newfield.add_dim_coord(coord,i)
            # Excepting situation is for the new vertical co-ordinate
            except ValueError:
                newfield.add_dim_coord(iris.coords.DimCoord(prange,
                                       long_name='pressure',units='hPa'),0)
    return newfield

# Interpolate field onto a vertical cross section defined by start/end
# args x and y define the coordinates of field
def oblique(field,start,end,npts,*args):
    # If input is a cube extract the data
    try:
        is_cube = field.is_compatible(field)
        cube = field
        field = field.data
        x = cube.coord('grid_longitude').points
        y = cube.coord('grid_latitude').points
    except AttributeError:
        x = args[0]
        y = args[1]
        is_cube = False

    # Allocate the output field
    [nz,ny,nx] = field.shape
    newfield = np.zeros((nz,npts))
    # Calculate the lat and lon point
    xp = np.linspace(start[0] ,end[0], npts, endpoint='true')
    yp = np.linspace(start[1] ,end[1], npts, endpoint='true')
    # Loop over output points
    for n in xrange(0,npts):
        # find the nearest index
        i = ((xp[n] - x).clip(0)).argmin()
        j = ((yp[n] - y).clip(0)).argmin()

        # Calculate the distance from each gridpoint
        dist1 = np.sqrt((xp[n]-x[i])**2 + (yp[n]-y[j])**2)
        dist2 = np.sqrt((xp[n]-x[i+1])**2 + (yp[n]-y[j])**2)
        dist3 = np.sqrt((xp[n]-x[i])**2 + (yp[n]-y[j+1])**2)
        dist4 = np.sqrt((xp[n]-x[i+1])**2 + (yp[n]-y[j+1])**2)
        totdist = dist1 + dist2 + dist3 + dist4
        if (totdist==0):
            newfield[:,n] = field[:,j,i]
        else:
            # Calculate Interpolation Weights
            w1=np.abs((1/3.0)*(1-dist1/totdist))
            w2=np.abs((1/3.0)*(1-dist2/totdist))
            w3=np.abs((1/3.0)*(1-dist3/totdist))
            w4=np.abs((1/3.0)*(1-dist4/totdist))
            # Calculate values at points
            newfield[:,n] = (w1*field[:,j,i]   + w2*field[:,j,i+1] +
                             w3*field[:,j+1,i] + w4*field[:,j+1,i+1])

    # If input was defined as cubes copy across metadata
    if is_cube:
        newfield = iris.cube.Cube(newfield)
        newfield.rename(cube.name())
        newfield._units = cube._units
        # Add Co-ordinates to cube
        newfield.add_dim_coord(cube.dim_coords[0],0)
        newfield.add_dim_coord(iris.coords.DimCoord(xp,
                               long_name='grid_longitude'),1)
        newfield.add_aux_coord(iris.coords.DimCoord(yp,
                               long_name='grid_latitude'),1)
    return newfield

#
def grid_to_column(cube,xpoint,ypoint):
    x = cube.coords('grid_longitude')[0].points
    y = cube.coords('grid_latitude')[0].points
    i = ((xpoint - x).clip(0)).argmin()
    j = ((ypoint - y).clip(0)).argmin()
    dist1 = np.sqrt((xpoint - x[i])**2   + (ypoint - y[j])**2)
    dist2 = np.sqrt((xpoint - x[i])**2   + (ypoint - y[j+1])**2)
    dist3 = np.sqrt((xpoint - x[i+1])**2 + (ypoint - y[j])**2)
    dist4 = np.sqrt((xpoint - x[i+1])**2 + (ypoint - y[j+1])**2)
    totdist = dist1 + dist2 + dist3 + dist4
    if totdist==0:
        column = cube.data[:,j,i]
    else:
        w1=np.abs((1/3.0)*(1-dist1/totdist))
        w2=np.abs((1/3.0)*(1-dist2/totdist))
        w3=np.abs((1/3.0)*(1-dist3/totdist))
        w4=np.abs((1/3.0)*(1-dist4/totdist))
        column = (w1*cube.data[:,j,i]   + w2*cube.data[:,j,i+1] +
                  w3*cube.data[:,j+1,i] + w4*cube.data[:,j+1,i+1])
    
    return column

# Linear Vertical Interpolation
# Theta points model levels zp
# Rho points are boundaries zb, set as halfway between theta points
# The k'th element of a rho array is below the k'th element in a theta array
# X_rho[0] = X_theta[0]

# V points are defined inside rho points so
# there is one less point in the y-direction

# u points are defined inside rho points so
# there should be one less point in the x-direction
# but there is an extra on the east side

# Theta to rho points
def theta_to_rho(field):
    size = field.shape
    newfield = np.zeros(((size)))
    for k in xrange(1,size[0]):
        newfield[k,:,:] = 0.5*(field[k,:,:] + field[k-1,:,:])
    newfield[0,:,:] = field[0,:,:]
    return newfield

# Rho to theta points
def rho_to_theta(field,z_theta):
    size = field.shape
    newfield = np.zeros(((size)))
    for k in xrange(1,size[0]-1):
        newfield[k,:,:] = field[k,:,:] + (
                          ((field[k+1,:,:] - field[k,:,:])/
                           (z_theta[k+1,:,:] - z_theta[k-1,:,:]))
                          *(z_theta[k,:,:] - z_theta[k-1,:,:]) )
    newfield[0,:,:] = field[0,:,:]
    newfield[-1,:,:] = 2*field[-1,:,:] - newfield[-2,:,:]
    return newfield

# rho to u points

# u to rho points
def u_to_rho(field_u):
    [nz,ny,nx] = field_u.shape
    field_rho = np.zeros(((nz,ny,nx)))
    for i in xrange(1,nx):
        field_rho[:,:,i] = 0.5*(field_u[:,:,i] + field_u[:,:,i-1])
    field_rho[:,:,0] = 2*field_u[:,:,0] - field_rho[:,:,1]
    return field_rho
        
# rho to v points

# v to rho points
def v_to_rho(field_v):
    [nz,ny,nx] = field_v.shape
    ny += 1
    field_rho = np.zeros(((nz,ny,nx)))
    for j in xrange(1,ny-1):
        field_rho[:,j,:] = 0.5*(field_v[:,:,i] + field_v[:,:,i-1])
    field_rho[:,0,:] = 2*field_v[:,0,:] - field_rho[:,1,:]
    field_rho[:,ny,:] = 2*field_v[:,ny-1,:] - field_rho[:,ny,:]
    return field_rho
