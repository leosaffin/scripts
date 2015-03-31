#!/usr/env/bin python
'''
Script for calculating, saving and plotting pv on theta
'''
import cPickle as pickle
import numpy as np
import matplotlib.pyplot as plt
import iris
from mymodule import load
from mymodule import convert
from mymodule import plot
from mymodule import interpolation
from iris.analysis import Linear

def main(filename,theta_level):
    '''
    ARGS:
        filename:
        
        theta_level:
            Potential temperature level in Kelvin on which to put PV
    '''
    # Load Cubes
    cubes = load.full(filename)
    # Extract variables
    pv = cubes.extract('total_pv')[0]
    temperature = cubes.extract('air_temperature')[0]
    pressure = cubes.extract('air_pressure')[1]
    
    # Calculate Potential Temperature
    theta = convert.calc_theta(temperature,pressure.data)
    
    (nz,ny,nx) = pv.shape
    # TODO - Below does not work for non-monotonic theta, need a way
    #        round this
    '''
    pv_on_theta = np.zeros((ny,nx))
    
    # Add theta as a co-ordinate
    newcoord = iris.coords.AuxCoord(points=theta.data,
                                    long_name='potential_temperature')
    pv.add_aux_coord(newcoord,[0,1,2])
    
    
    # Calculate PV on theta
    for j in xrange(ny):
        for i in xrange(nx):
            subcube = pv[:,j,i]
            
            pv_on_theta[j,i] = subcube.interpolate([('potential_temperature',
                                                     theta_level)],
                                                   Linear()).data
    '''
    pv_on_theta = interpolation.to_level_3d(pv.data,theta.data,theta_level)

    # Save PV on theta
    with open('/home/lsaffi/pv_on_theta.pkl','wb') as output:
        pickle.dump(pv_on_theta,output)
        
    # Plot PV on theta
    levels = np.arange(0,10.1,0.25)
    plot.polar(pv_on_theta[:,(nx/2)::],'north',levels,cmap='cubehelix_r')
    plt.savefig('pv_on_theta.png')
    return
    
if __name__=='__main__':
    filename = ['/projects/diamet/lsaffi/xjjhz/xjjhza_pa035',
                '/projects/diamet/lsaffi/xjjhz/xjjhza_pb035']
    main(filename,315)
