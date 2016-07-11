# Mapping of cube name to colourscale
cmaps = {}
cmaps['total_minus_advection_only_pv'] = 'coolwarm'
cmaps['sum_of_physics_pv_tracers'] = 'coolwarm'
cmaps['dynamics_tracer_inconsistency'] = 'coolwarm'
cmaps['residual_pv'] = 'coolwarm'
cmaps['short_wave_radiation_pv'] = 'coolwarm'
cmaps['long_wave_radiation_pv'] = 'coolwarm'
cmaps['gravity_wave_drag_pv'] = 'coolwarm'
cmaps['convection_pv'] = 'coolwarm'
cmaps['boundary_layer_pv'] = 'coolwarm'

# Mapping of cube name to linestyle
linestyles = {}
linestyles['total_minus_advection_only_pv'] = '-xk'
linestyles['sum_of_physics_pv_tracers'] = '--xk'
linestyles['dynamics_tracer_inconsistency'] = ':xk'
linestyles['residual_pv'] = '-.xk'
linestyles['short_wave_radiation_pv'] = '--xr'
linestyles['long_wave_radiation_pv'] = ':xr'
linestyles['gravity_wave_drag_pv'] = '-xg'
linestyles['convection_pv'] = '--xb'
linestyles['boundary_layer_pv'] = ':xb'

# Mapping of cube name to label
labels = {}
labels['air_potential_temperature'] = r'$\theta$'
labels['total_minus_advection_only_pv'] = r'$q-q_{adv}$'
labels['sum_of_physics_pv_tracers'] = r'$\sum q_{phys}$'
labels['dynamics_tracer_inconsistency'] = r'$\varepsilon_{I}$'
labels['residual_pv'] = r'$\varepsilon_{r}$'
labels['short_wave_radiation_pv'] = r'$q_{sw}$'
labels['long_wave_radiation_pv'] = r'$q_{lw}$'
labels['gravity_wave_drag_pv'] = r'$q_{gwd}$'
labels['convection_pv'] = r'$q_{con}$'
labels['boundary_layer_pv'] = r'$q_{bl}$'
