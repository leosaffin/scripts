import numpy as np
import iris
import iris.analysis.maths as imath
import interpolate

# Constants
R = 287.058       # Ideal Gas Constant for air
R_v = 461.5       # Ideal Gas Constant for water vapour
c_p = 1006        # Heat capacity at constant pressure
p_0 = 1000        # Typical surface pressure (hPa)

# Temperature (K) from potential temperature and pressure
def theta_to_T(theta,**kwargs):
    # Use either form of pressure
    if 'exner' in kwargs:
        exner = kwargs['exner']
    if 'pressure' in kwargs:
        exner = pressure_to_exner(**kwargs)
    # pressure defined at rho points
    exner = interpolate.rho_to_theta(exner)
    return theta*exner

# Potential temperature from temperature (K) and pressure
def T_to_theta(temperature,**kwargs):
    # Use either form of pressure
    if 'exner' in kwargs:
        exner = kwargs['exner']
    if 'pressure' in kwargs:
        exner = pressure_to_exner(**kwargs)
    return temperature/exner

# Exner function from pressure (pa)
def pressure_to_exner(pressure):
    return (pressure/p_0)**(R/c_p)

# Pressure (pa) from exner function
def exner_to_pressure(exner):
    return p_0*exner**(c_p/R)

# Saturated Vapour pressure (hPa) from temperature (K)
def tetens(T):
    return 6.1094*imath.exp(17.625*(T-273)/(T - 30))

# Calculate Relative Humidity
def rh(pressure,temperature,vapour):
    e_s = tetens(temperature)
    return pressure*vapour*(R_v/R)/e_s

# Calculate dry density
def density(pressure,temperature):
    return pressure/(R*temperature)
