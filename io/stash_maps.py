from iris.fileformats.pp import STASH


class StashMap(dict):
    """
    """

    def remap_cube(self, cube):
        stash = cube.attributes['STASH']
        self[stash].modify_cube(cube)

    def remap_cubelist(self, cubelist):
        for cube in cubelist:
            stash = cube.attributes['STASH']
            if stash in self:
                self[stash].modify_cube(cube)


class CustomStash(object):
    """Defines attributes to add to a cube based on the STASH attribute

    Attributes:
        name

        units
    """

    def __init__(self, name=None, units=None):
        self.name = name
        self.units = units

    def modify_cube(self, cube):
        # Change Units
        cube.convert_units(self.units)

        # Change name
        cube.rename(self.name)


# Potential temperature tracers at vn7.3
theta_tracers = StashMap(
    [(STASH(1, 0, 321), CustomStash(name='advection_only_theta',
                                   units='K')),
     (STASH(1, 0, 322), CustomStash(name='short_wave_radiation_theta',
                                   units='K')),
     (STASH(1, 0, 323), CustomStash(name='long_wave_radiation_theta',
                                   units='K')),
     (STASH(1, 0, 324), CustomStash(name='radiation_theta',
                                   units='K')),
     (STASH(1, 0, 325), CustomStash(name='microphysics_theta',
                                   units='K')),
     (STASH(1, 0, 326), CustomStash(name='long_wave_radiation_theta',
                                   units='K')),
     (STASH(1, 0, 327), CustomStash(name='convection_theta',
                                   units='K')),
     (STASH(1, 0, 328), CustomStash(name='short_wave_radiation_theta',
                                   units='K')),
     (STASH(1, 0, 329), CustomStash(name='long_wave_radiation_theta',
                                   units='K')),
     (STASH(1, 0, 330), CustomStash(name='boundary_layer_latent_heating_theta',
                                   units='K')),
     (STASH(1, 0, 331), CustomStash(name='boundary_layer_theta',
                                   units='K')),
     (STASH(1, 0, 332), CustomStash(name='atmospheric_physics_1_theta',
                                   units='K')),
     (STASH(1, 0, 333), CustomStash(name='atmospheric_physics_2_theta',
                                   units='K')),
     (STASH(1, 0, 334), CustomStash(name='diffusion_theta',
                                   units='K')),
     (STASH(1, 0, 335), CustomStash(name='time_filtering_theta',
                                   units='K')),
     (STASH(1, 0, 336), CustomStash(name='update_fields_theta',
                                   units='K')),
     (STASH(1, 0, 337), CustomStash(name='advection_theta',
                                   units='K')),
     (STASH(1, 0, 338), CustomStash(name='lateral_boundary_theta',
                                   units='K')),
     (STASH(1, 0, 339), CustomStash(name='cloud_rebalancing_theta',
                                   units='K')),
     (STASH(1, 0, 340), CustomStash(name='polar_filtering_theta',
                                   units='K')),
     (STASH(1, 0, 342), CustomStash(name='pressure_gradient_theta',
                                   units='K')),
     (STASH(1, 0, 343), CustomStash(name='pressure_solver_theta',
                                   units='K')),
     (STASH(1, 0, 344), CustomStash(name='continuity_theta',
                                   units='K')),
     (STASH(1, 0, 345), CustomStash(name='idealised_pressure_forcing_theta',
                                   units='K')),
     (STASH(1, 0, 346), CustomStash(name='barotropic_friction_theta',
                                   units='K')),
     (STASH(1, 0, 347), CustomStash(name='baroclinic_friction_theta',
                                   units='K')),

     ])

# PV tracers at vn7.3
pv_tracers = StashMap(
    [(STASH(1, 0, 321), CustomStash(name='advection_only_pv',
                                   units='PVU')),
     (STASH(1, 0, 322), CustomStash(name='short_wave_radiation_pv',
                                   units='PVU')),
     (STASH(1, 0, 323), CustomStash(name='long_wave_radiation_pv',
                                   units='PVU')),
     (STASH(1, 0, 324), CustomStash(name='radiation_pv',
                                   units='PVU')),
     (STASH(1, 0, 325), CustomStash(name='microphysics_pv',
                                   units='PVU')),
     (STASH(1, 0, 326), CustomStash(name='gravity_wave_drag_pv',
                                   units='PVU')),
     (STASH(1, 0, 327), CustomStash(name='convection_pv',
                                   units='PVU')),
     (STASH(1, 0, 328), CustomStash(name='',
                                   units='PVU')),
     (STASH(1, 0, 329), CustomStash(name='',
                                   units='PVU')),
     (STASH(1, 0, 330), CustomStash(name='boundary_layer_pv',
                                   units='PVU')),
     (STASH(1, 0, 331), CustomStash(name='advection_only_theta',
                                   units='K')),
     (STASH(1, 0, 332), CustomStash(name='atmospheric_physics_1_pv',
                                   units='PVU')),
     (STASH(1, 0, 333), CustomStash(name='atmospheric_physics_2_pv',
                                   units='PVU')),
     (STASH(1, 0, 334), CustomStash(name='pressure_solver_pv',
                                   units='PVU')),
     (STASH(1, 0, 335), CustomStash(name='',
                                   units='PVU')),
     (STASH(1, 0, 336), CustomStash(name='dynamics_tracer_inconsistency',
                                   units='PVU')),
     (STASH(1, 0, 337), CustomStash(name='',
                                   units='PVU')),
     (STASH(1, 0, 338), CustomStash(name='',
                                   units='K')),
     (STASH(1, 0, 339), CustomStash(name='cloud_rebalancing_pv',
                                   units='PVU')),
     (STASH(1, 0, 340), CustomStash(name='ertel_potential_vorticity',
                                   units='PVU')),
     ])
