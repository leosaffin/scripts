import numpy as np

def get_kernel(nx,ny,name):
    kernel = np.zeros((nx,ny))
    if(name is 'mean'):
        kernel[:,:] = 1.0/(nx*ny)
    elif(name is 'gauss'):
        kernel[:,:] = 1.0
    else:
        print('Kernel not available')
    return kernel

def smooth2d(field, kernel):
    [nx,ny] = field.shape
    smoothed_field = np.zeros((nx,ny))
    [kx,ky] = kernel.shape
    kx = (kx-1)/2
    ky = (ky-1)/2
    for i in xrange(kx,nx-kx):
        for j in xrange(ky,ny-ky):
            smoothed_field[i,j] = np.sum(kernel*field[i-kx:i+kx+1,
                                                      j-ky:j+ky+1])
    return smoothed_field

def smooth3d(field, kernel):
    [nx,ny,nz] = field.shape
    smoothed_field = field.copy()
    [kx,ky,kz] = kernel.shape
    kx = (kx-1)/2
    ky = (ky-1)/2
    kz = (kz-1)/2
    for i in xrange(kx,nx-kx):
        for j in xrange(ky,ny-ky):
            for k in xrange(kz,nz-kz):
                smoothed_field[i,j,k] = np.sum(kernel*field[i-kx:i+kx+1,
                                                            j-ky:j+ky+1,
                                                            k-kz:k+kz+1])
    return smoothed_field
