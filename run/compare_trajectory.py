# Find the difference in trajectories 
# calculated with high and low resolution data
import cPickle as pickle
import load
import trajectories

# Load the two trajectories
high_res = load.lagranto('/home/lsaffi/data/out.1')
low_res = load.lagranto('/home/lsaffi/data/out_3h.1')

# Compare the two trajectories
diffs = trajectories.compare(high_res,low_res)

# Save as pkl files
filename = '/home/lsaffi/data/3h_vs_1h_trajectories.pkl'
with open(filename,'wb') as output:
    pickle.dump(diffs,output)

