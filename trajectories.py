import numpy as np
from scipy.interpolate import griddata
import load
import interpolate
import grid

# Reads information from lagranto output given the filename and
# number of timesteps in the trajectories
def load_traj(trajectory_file,nt,**kwargs):
    lon_start = []         # Longitude at Trajectory Start
    lat_start = []         # Latitude at Trajectory Start
    p_start = []           # Pressure at Trajectory Start
    lon_end = []           # Longitude at Trajectory End
    lat_end = []           # Latitude at Trajectory End
    p_end = []             # Pressure at Trajectory End
    t_end = []             # Time at Trajectory End

    #Open File
    traj_file = open(trajectory_file,'r')
    #Ignore Header
    for i in xrange(0,5):
        skip = traj_file.readline()

    t=0
    n=0
    end=0
    # Loop through file lines
    for line in traj_file:
        # Skip gap line between trajectories
        if (t==nt):
            t=-1
            n+=1
            end=0
        elif (t==nt-1):
            t_end.append(t_prev)
            lon_end.append(lon_prev)
            lat_end.append(lat_prev)
            p_end.append(p_prev)
        # If trajectory hasn't exited load next line
        elif end!=1:
            line = line.strip()
            columns = line.split()
            time = float(columns[0])
            lon = float(columns[1])
            lat = float(columns[2])
            p = float(columns[3])
            if t==0:
                lon_start.append(lon)
                lat_start.append(lat)
                p_start.append(p)
                t_prev = 0
                lon_prev = 0
                lat_prev = 0
                p_prev = 0
            if 'domain' in kwargs:
                if outside(lon,lat,**kwargs):
                    p = -1000
            if p!=-1000:
                t_prev = time
                lon_prev = lon
                lat_prev = lat
                p_prev = p
            else:
                end=1
        t+=1

    traj_file.close()
    # Convert data to numpy arrays in dictionary
    output = {}
    output['lat_start'] = np.array(lat_start)
    output['lon_start'] = np.array(lon_start)
    output['p_start'] = np.array(p_start)
    output['lat_end'] = np.array(lat_end)
    output['lon_end'] = np.array(lon_end)
    output['p_end'] = np.array(p_end)
    output['t_end'] = np.array(t_end) + nt - 1
    return output

def outside(x,y,**kwargs):
    if 'polelat' in kwargs and 'polelon' in kwargs:
        [x,y] = grid.rotate(x,y,kwargs['polelon'],kwargs['polelat'])
        x = (x+180)%360 + 180
    [xmin,xmax,ymin,ymax] = kwargs['domain']
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

# Reverse domain fills using trajectory information
def gather_ends(data,nt,job,**kwargs):

    x_f = data['lon_end']
    y_f = data['lat_end']
    p_f = data['p_end']
    t_f = data['t_end']

    ntra = len(t_f)            # Number of Trajectories
    loaded = set()             # Flag on whether a file has already been loaded
    pv_start = np.zeros(ntra)  # PV at the start of the trajectory
    tracer = {}                # Dictionary of loaded tracer cubes by time
    pressure = {}              # Dictionary of loaded pressure cubes by time

    for n in xrange(0,ntra):
        time = int(t_f[n])
        # Rotate Trajectory points to model grid
        if 'polelat' in kwargs and 'polelon' in kwargs:
            [grid_x,grid_y] = grid.rotate(x_f[n],y_f[n],
                                          kwargs['polelon'],kwargs['polelat'])
        else:
            [grid_x,grid_y] = [x_f[n],y_f[n]]
        # Irritating dependency on current data
        grid_x = (grid_x + 180)%360 + 180
        # Load Unloaded cubes
        if time not in loaded:
            cubes = load.all(job,time)
            tracer[str(time)] = cubes.extract('Advection Only PV')[0]
            pressure[str(time)] = cubes.extract('air_pressure')[1]
            loaded.add(time)
        if 'grid' not in loaded:
            [nz,ny,nx] = cubes[0].data.shape
            pv_temp = np.zeros(((nz,1,1)))
            p_temp = np.zeros(((nz,1,1)))
            loaded.add('grid')
        # Interpolate Tracer and Pressure to lat,lon points
        pv_temp[:,0,0] = interpolate.grid_to_column(tracer[str(time)],
                                                    grid_x,grid_y)
        p_temp[:,0,0] = interpolate.grid_to_column(pressure[str(time)],
                                                   grid_x,grid_y)
        # Interpolate single column to single pressure level
        pv_start[n] = interpolate.any_to_pressure(pv_temp,p_temp,p_f[n])
    return pv_start

# Interpolate field defined at trajectory points to model grid
def regular_grid(data,field,x_p,y_p):
    x_s = data['lon_start']
    y_s = data['lat_start']
    points = [x_s,y_s]
    points = np.transpose(np.array(points))
    return griddata(points,field,(x_p,y_p),method='linear')
    

    
    
