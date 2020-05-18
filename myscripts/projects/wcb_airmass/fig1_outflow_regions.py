import matplotlib.pyplot as plt
import iris
import iris.plot as iplt
import cartopy.crs as ccrs

from myscripts.projects.wcb_airmass import case_studies, plotdir


def main():
    projection = ccrs.Mollweide()
    fig = plt.figure(figsize=[16, 10])

    for n, case in enumerate(sorted(case_studies.keys())):
        case_study = case_studies[case]

        # Load the forecast (units of PV are a bit mucked up)
        cubes = case_study.load_forecast()
        pv = cubes.extract_strict(iris.Constraint("ertel_potential_vorticity")) * 1e-6
        dtheta = cubes.extract_strict(iris.Constraint("total_minus_adv_only_theta"))

        # Load the isentropic trajectories on the isentropic level of the forecast data
        tr = case_study.load_trajectories("isentropic")
        level = dtheta.coord('air_potential_temperature').points[0]
        tr = tr.select("air_potential_temperature", "==", level,
                       time=[tr.relative_times[0]])

        ax = plt.subplot(2, 2, n+1, projection=projection)
        im = make_plot(ax, dtheta, pv, tr)

        ax.set_title("{}: {} ({}K)".format(case, case_study.storm_name, int(level)),
                     fontsize=16)

    plt.subplots_adjust(bottom=0.2)
    cax = plt.axes([0.1, 0.1, 0.8, 0.05])
    cbar = fig.colorbar(im, cax=cax, orientation="horizontal")
    cbar.set_label(r"$\theta - \theta_{adv}$ (K)", fontsize=16)

    plt.savefig(plotdir + "outflow_regions.png")

    return


def make_plot(ax, dtheta, pv, tr):
    im = iplt.pcolormesh(dtheta, vmin=-30, vmax=30, cmap="seismic")
    print(dtheta.data.min(), dtheta.data.max())
    ax.coastlines()
    ax.gridlines()

    # Add a contour for PV=2 and also shade PV>2
    iplt.contour(pv, [2], colors='k')
    pv.data = (pv.data > 2).astype(float)
    iplt.contourf(pv, [0.9, 1.1], colors="k", alpha=0.25)

    # Need to use the cube's coordinate reference system to properly add regular
    # coordinates on top
    crs = dtheta.coord(axis="x").coord_system.as_cartopy_crs()
    plt.plot(tr.x[:, 0] - 360, tr.y[:, 0], transform=crs, lw=3,
             color='cyan')

    # With the projection the axis limits don't set well, so shrink it down as much as
    # possible
    x, y = pv.coord(axis="x"), pv.coord(axis="y")
    ax.set_extent([x.points.min(), x.points.max(), y.points.min(), y.points.max()],
                  crs=crs)

    return im


if __name__ == '__main__':
    main()
