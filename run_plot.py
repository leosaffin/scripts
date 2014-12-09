import numpy as np
import matplotlib.pyplot as plt
import iris
import iris.plot as iplt

import load
import interpolate
import grid
import convert
import plot

# Define Diagnostics
names = ['Total minus Advection Only PV',
         'Sum of PV Tracers',
         'Residual Error',
         'Short Wave Radiation PV',
         'Long Wave Radiation PV',
         'Radiation PV',
         'Microphysics PV',
         'Gravity Wave Drag PV',
         'Convection PV',
         'Boundary Layer PV',
         'Advection Inconsistency PV',
         'Total PV']
short_names = ['diff','sum','res','sw','lw','rad','micro',
               'gwd','conv','bl','err','tot']
prange = np.arange(50,1000,50)       # Pressure levels to interpolate to
plevels = [300,500,700]              # Pressure levels to plot
theta_levels = np.arange(250,400,10) # Theta levels to plot
job = 'xkcqa'                        # IOP8 job
#job = 'xjjho'                        # IOP5 Job

# Dropsonde Run 1
#start_x = 353.84311
#start_y = 55.50189
#end_x = 353.94075
#end_y = 58.41798
#p_track = 398
#lead_time = 24

# Dropsonde Run 2
start_x = 353.65896
start_y = 58.49295
end_x = 349.57327
end_y = 56.37439
p_track = 398
lead_time = 25

# Rotate dropsonde runs to grid co-ordinates
start = np.array(grid.rotate(start_x,start_y,177.5,37.5))
end = np.array(grid.rotate(end_x,end_y,177.5,37.5))
start[0] = start[0] + 360.
end[0] = end[0] + 360.

# Extend the line from the dropsonde run
diff = end - start
start_e = start - diff
end_e = end + diff


# Load Tracers
cubes = load.all(job,lead_time)
adv = cubes.extract('Advection Only PV')[0]
pressure = cubes.extract('air_pressure')[1]
temperature = cubes.extract('air_temperature')[0]
vapour = cubes.extract('specific_humidity')[0]

theta = convert.T_to_theta(temperature,pressure=pressure)
relative_humidity = convert.rh(pressure,temperature,vapour)
# Calculate the cross section for advection-only PV

p_adv = interpolate.any_to_pressure(adv,pressure,prange)
v_adv = interpolate.oblique(p_adv,start_e,end_e,100)
p_rh = interpolate.any_to_pressure(relative_humidity,pressure,prange)
v_rh = interpolate.oblique(p_rh,start_e,end_e,100)
p_theta = interpolate.any_to_pressure(theta,pressure,prange)
v_theta = interpolate.oblique(p_theta,start_e,end_e,100)

# Loop over diagnostics
for i,name in enumerate(names):
    print name
    # Set color axis higher for total PV
    if name == 'Total PV':
        caxis = 5
    else:
        caxis = 2.5

    # Explicitly calculate selected diagnostics
    cube = load.extract(cubes,name)

    # Interpolate to pressure levels
    tracer = interpolate.any_to_pressure(tracer,pressure,prange)

    # Loop over pressure levels
    for p in plevels:
        title = name + ' at T+' + str(lead_time) + 'H at ' + str(p) + 'hPa' 
        # Plot Tracer
        plot.horizontal(tracer,caxis,pv=p_adv,p=p,title=title)
        # Plot other variables
        plot_rh = p_rh.extract(iris.Constraint(pressure=p))
        iplt.contour(plot_rh,[0.85],colors='y')
        plot_theta = p_theta.extract(iris.Constraint(pressure=p))
        cs = iplt.contour(plot_theta,theta_levels,
                          linestyles='--',colors='k')
        plt.clabel(cs,fontsize=8)
        # Add the flight track
        plt.plot([start[0]-360,end[0]-360],[start[1],end[1]],'x',color='k')
        plt.plot([start_e[0]-360,end_e[0]-360],
                 [start_e[1],end_e[1]],color='k')
        plt.savefig('IOP8_' + short_names[i] + '_' + str(lead_time) + 
                    '_' + str(p) + '.png')

    # Interpolate to cross-section
    tracer = interpolate.oblique(tracer,start_e,end_e,100)
    title = name + ' at T+' + str(lead_time) + 'H'
    # Plot Tracer
    plot.main(tracer,caxis,pv=v_adv,title=title)
    # Plot other variables
    iplt.contour(v_rh,[0.85],colors='y')
    cs = iplt.contour(v_theta,theta_levels,linestyles='--',colors='k')
    plt.clabel(cs,fontsize=8)
    # Add the flight track
    plt.plot([start[0],end[0]],[p_track,p_track],'x',color='k')
    # Set the axis to pressure decreasing
    plt.axis([start_e[0],end_e[0],prange[-1],prange[0]])
    plt.savefig('IOP8_vert_' + short_names[i] + '_' + str(lead_time) + '.png')


