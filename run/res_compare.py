import numpy as np
import load
import grid
import convert

cubes = load.all('xjjho',36)

pressure = cubes.extract('air_pressure')[1]
temperature = cubes.extract('air_temperature')[0]

volume = grid.volume(temperature)

rho = convert.density(pressure,temperature)

mass = volume*rho.data

mask = np.logical_and(temperature.coord('altitude')>3000,
                      cubes.extract('Advection Only PV').data<2)

masked_mass = mass*mask

res1 = (cubes.extract('Total PV') - 
        cubes.extract('Atmospheric Physics 1 PV') - 
        cubes.extract('Atmospheric Physics 2 PV') - 
        cubes.extract('Cloud Rebalancing PV') - 
        cubes.extract('Advection Only PV')).data

res2 = res1 - cubes.extract('Advection Inconsistency PV').data

integrated_res1 = np.sum(np.abs(res1)*masked_mass)/np.sum(masked_mass)
integrated_res2 = np.sum(np.abs(res2)*masked_mass)/np.sum(masked_mass)


ratio = integrated_res1/integrated_res2
