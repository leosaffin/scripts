import matplotlib.pyplot as plt
import iris.quickplot as qplt
import iris.analysis.maths as imath
from iris.cube import CubeList
from scripts.season.second_analysis import load_all


def main(variables, domains, t_indices):
    data = load_all()
    for variable in variables:
        for domain in domains:
            for t_index in t_indices:
                subdata = extract(data, variable, domain, t_index)
                result = analyse(subdata)
                plotfig(result[0], variable, domain, t_index)
            plt.legend(loc='best')
            plt.savefig('/home/lsaffi/plots/season/' +
                        result[0].name() + '.png')
            plt.clf()


def extract(data, variable, domain, t_index):
    subdata = CubeList()
    for forecast in data:
        subdata.append(forecast[domain].extract(variable)[0][t_index])

    return subdata


def analyse(subdata):
    """Calculate the mean and standard deviation of the variable over the many
    forecasts
    """
    mean = sum(subdata) / len(subdata)
    diffs = [cube - mean for cube in subdata]
    sq_diffs = [imath.exponentiate(diff, 2) for diff in diffs]
    stdev = imath.exponentiate(sum(sq_diffs), 0.5)

    return mean, stdev


def plotfig(result, variable, domain, t_index):
    result.rename(variable + '_in_' + domain + '_domain')
    qplt.plot(result, label=str(t_index))


if __name__ == '__main__':
    variables = ['mean_of_total_minus_advection_only_pv']
    domains = ['full', 'north', 'south']
    t_indices = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    main(variables, domains, t_indices)
