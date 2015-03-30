# Find the difference in trajectories 
# calculated with high and low resolution data
import cPickle as pickle
import load
import trajectories
import numpy as np
import matplotlib.pyplot as plt

directory = '/home/lsaffi/data/'
def run_compare(high_res_file,low_res_file,output_file):
    # Load the two trajectories
    high_res = load.lagranto(directory + high_res_file)
    low_res = load.lagranto(directory + low_res_file)

    # Compare the two trajectories
    diffs = trajectories.compare(high_res,low_res)

    # Save as pkl files
    with open(directory + output_file,'wb') as output:
        pickle.dump(diffs,output)
    return

#if __name__ == '__main__':
#    compare

def plot_compare(input_file):
    # Load previously calculated data
    with open(directory + input_file,'rb') as infile:
        diffs = pickle.load(infile)

    times = diffs[0]
    positions = diffs[1].keys()

    # Plot data
    for i,name in enumerate(positions):
        plt.clf()
        plt.plot(times,diffs[1][name])
        plt.xlabel('Time (Hours)')
        plt.ylabel(name)
        plt.savefig(name + '_traj_err.png')

