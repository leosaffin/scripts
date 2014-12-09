import numpy as np
import iris
import matplotlib.pyplot as plt
import iris.plot as iplt
import time

# Single Height Level Plot
# kwargs [z,pv,title]
def horizontal(cube,cscale,**kwargs):
    # Extract the defined model level if a multi-level cube is supplied
    if 'z' in kwargs:
        cube = cube.extract(iris.Constraint(model_level_number = kwargs['z']))
        if 'pv' in kwargs:
            kwargs['pv'] = kwargs['pv'].extract(iris.Constraint(
                                        model_level_number = kwargs['z']))
    elif 'p' in kwargs:
        cube = cube.extract(iris.Constraint(pressure = kwargs['p']))
        if 'pv' in kwargs:
            kwargs['pv'] = kwargs['pv'].extract(iris.Constraint(pressure = 
                                                                kwargs['p']))
    # Plot the cube
    main(cube,cscale,**kwargs)
    # Add coastlines
    plt.gca().coastlines()
    return

# Vertical cross section plot
def main(cube,cscale,**kwargs):
    # Set the colorscale between +/- cscale with 9 blocks and one block
    # over the zero point
    levels=np.arange(-cscale,cscale+(cscale/5.0),cscale/4.5)
    plt.clf()
    # Plot the cube
    figure = iplt.contourf(cube,levels,extend='both',cmap='bwr')
    # Add a colorbar
    plt.colorbar(figure,drawedges='true',shrink=0.75)
    # Contour the 2PVU tropopause if pv is supplied
    if 'pv' in kwargs:
        iplt.contour(kwargs['pv'],[2],colors='g')
    # Add a title to the figure
    if 'title' in kwargs:
        plt.title(kwargs['title']) #+ '\n' + time.strftime("%Y/%m/%d"))
    # If no title is supplied use the cube's name
    else:
        plt.title(cube.name())#+ '\n' + time.strftime("%Y/%m/%d"))
    return

#Accumulation plot
def qqadv(xt,bins,count,cscale):
    levels=np.arange(-cscale,cscale+(cscale/5.0),cscale/4.5)
    plt.clf()
    plt.contourf(xt,bins,count,levels,cmap='bwr')
    plt.xlabel('Time (hours)')
    plt.ylabel('Advection Only PV (PVU)')
    plt.colorbar(drawedges='true')
    plt.show()
