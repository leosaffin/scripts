import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
from math import sqrt
import interpolate
import grid

class Trajectory:
    def __init__(self):
        self.positions = {}

    # Add data in a dictionary given by names
    def add_data(self,data,names):
        # Convert data to floats
        for i in xrange(len(data)):
            data[i] = float(data[i])

        # Add position data to dictionary
        try:
            for i,name in enumerate(names):
                self.positions[name].append(data[i])
        # Initialise dictionary words if not already
        except KeyError:
            for i,name in enumerate(names):
                self.positions[name] = []
                self.positions[name].append(data[i])

    # Convert positions to numpy arrays
    def vectorise(self):
        for position in self.positions:
            self.positions[position] = np.array(self.positions[position])

    # Mask values leaving the domain
    def mask(self):
        for position in self.positions:
            self.positions[position] = np.ma.masked_where(
                                         self.positions['p'] == -1000,
                                         self.positions[position])
    # Remove mask on array
    def unmask(self):
        for position in self.positions:
            self.positions[position] = self.positions[position].data

    # Reverse domain fill
    def rdf(self,t_ref,data,pressure,**kwargs):
        # Get index of last point in the domain
        try:
            index = self.positions['p'].index(-1000) - 1
        except ValueError:
            index = -1
        # Trajectory start information
        lon = self.positions['lon'][index]
        lat = self.positions['lat'][index]
        p = self.positions['p'][index]
        t = self.positions['time'][index] + t_ref

        # Rotate positions if data is on rotated grid
        if 'polelat' in kwargs and 'polelon' in kwargs:
            [lon,lat] = grid.rotate(lon,lat,kwargs['polelon'],
                                            kwargs['polelat'])
            lon = (lon+180)%360 + 180

        # Interpolate Tracer and Pressure to lat,lon points
        [nz,ny,nx] = data[t].data.shape
        col_data = np.zeros(((nz,1,1)))
        col_data[:,0,0] = interpolate.grid_to_column(data[t],lon,lat)
        col_pressure = np.zeros(((nz,1,1)))
        col_pressure[:,0,0] = interpolate.grid_to_column(pressure[t],lon,lat)
        # Interpolate single column to single pressure level
        self.rdf_pv = interpolate.any_to_pressure(col_data,col_pressure,p)
        

    # Plot two positions along the trajectory against each other
    def plot(self,xaxis,yaxis,*args,**kwargs):
        plt.plot(self.positions[xaxis],self.positions[yaxis],*args,**kwargs)
        plt.xlabel(xaxis)
        plt.ylabel(yaxis)

def outside(x,y,domain):
    xmin,xmax,ymin,ymax = domain
    if xmin<xmax:
        if x<xmin or x>xmax:
            return True
    else:
        if x<xmin and x>xmax:
            return True
    if ymin<ymax:
        if y<ymin or y>ymax:
            return True
    else:
        if y<ymin and y>ymax:
            return True
    return False

# Interpolate field defined at trajectory points to model grid
def regular_grid(field,x_points,y_points,x_grid,y_grid):
    points = [x_points,y_points]
    points = np.transpose(np.array(points))
    return griddata(points,field,(x_grid,y_grid),method='linear')

def compare(high_res,low_res):
    times = low_res[0].positions['time']
    nt = len(times)
    keys = low_res[0].positions.keys()
    
    index = []
    counted = np.zeros(nt)
    
    # Find the indicies of the times from 
    # low res data in high res data
    for time in times:
        index.append(high_res[0].positions['time'].index(time))

    # Initialise difference arrays
    diffs = {}
    for key in keys:
        diffs[key] = np.zeros(nt)

    # Loop over trajectories
    for n in xrange(len(low_res)):
        # Loop over low resolution times
        for i in xrange(nt):
            # Check neither trajectory has left domain
            if (high_res[n].positions['p'][index[i]] != -1000 and
                 low_res[n].positions['p'][i]        != -1000):
                # Accumulate Squared Differences
                counted[i] += 1
                for key in keys:
                    diffs[key][i] += (high_res[n].positions[key][index[i]] - 
                                       low_res[n].positions[key][i])**2

    # Loop over low_res times
    for i in xrange(nt):
        for key in keys:
            # Calculate RMS differences
            diffs[key][i] = sqrt(diffs[key][i]/counted[i])

    return[times,diffs]
    
