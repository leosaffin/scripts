"""
"""

import numpy as np
from scipy.integrate import ode


f = lambda t, y, forecast: y * t

t_0 = 0.0
dt = -1.0
t_f = -10.0
y_0 = np.linspace(-2, 2, 5)

integrator = ode(f).set_integrator('dopri5')
integrator.set_initial_value(y_0, t_0)
integrator.set_f_params(1)

while integrator.successful() and integrator.t > t_f:
    integrator.integrate(integrator.t + dt)

print integrator.t
print integrator.y
