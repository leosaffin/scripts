import datetime
from mymodule.user_variables import datadir
from lagranto import trajectory


def main():
    job = 'iop5_extended'
    name = 'forward_trajectories_from_low_levels'
    filename = datadir + job + '/' + name + '.pkl'

    trajectories = select_wcb(filename)
    trajectories.save(datadir + job + '/' + name + '_gt600hpa.pkl')

    return


def select_wcb(filename):
    # Load the trajectories
    trajectories = trajectory.load(filename)
    print len(trajectories)

    # Select trajectories that stay in the domain
    trajectories = trajectories.select('air_pressure', '>', 0)
    print len(trajectories)

    # Select trajectories that fulfill the ascent criteria
    dt1 = datetime.timedelta(hours=0)
    dt2 = datetime.timedelta(hours=48)
    trajectories = trajectories.select('air_pressure', '>', 60000,
                                       time=[dt1, dt2])
    print len(trajectories)

    return trajectories


if __name__ == '__main__':
    main()
