import numpy as np

#This script searches downward from the top of the domain to locate the
#tropopause elevation. A 3-d mask is then generated which has value 1 if a
#grid point lies within a distance dthresh of the tropopause and is zero
#otherwise.
def tropopause(pv,altitude,res=2500):
    [nz,ny,nx] = pv.shape
    mask = np.zeros(((nz,ny,nx)))
    pvtrop=2
    #Search downward for tropopause
    for j in xrange(0,ny):
        for i in xrange(0,nx):
            k=nz-1
            [test, k, mask[:,j,i]] = search(pv[:,j,i],pvtrop,
                                            altitude[:,j,i],k,
                                            mask[:,j,i],res)
            if(test==1):
                #search for folded tropopause points
                [test, k, mask[:,j,i]] = search(-pv[:,j,i],-pvtrop,
                                                altitude[:,j,i],k,
                                                mask[:,j,i],res)
                if(test==1):
                    #search for bottom elevation of fold
                    [test, k, mask[:,j,i]] = search(pv[:,j,i],pvtrop,
                                                    altitude[:,j,i],k,
                                                    mask[:,j,i],res)
    return mask        

# Perform a downward search for tropopause
def search(pv,pvtrop,z,k,zmask,res):
    test = 0
    while(test==0 and z[k]>2e3):
        k -= 1
        if (pv[k]<pvtrop):
            test=1
    if(test==1):
        ztrop = z[k+1]-((z[k+1]-z[k])/(pv[k+1]-pv[k]))*(pv[k+1]-pvtrop)
        zmask = np.logical_or(np.abs(z-ztrop)<=res, zmask==1).astype(int)
    return[test, k, zmask]

def dipole(cube,pv,bins,weights):
    # Calculate the weighted average for each bin
    mean = np.zeros(len(bins))
    # Loop over bins
    for n,[bin_min,bin_max] in enumerate(bins):
        # Mask for PV not in bin
        weight_mask = np.ma.masked_where(pv<bin_min, weights)
        weight_mask = np.ma.masked_where(pv>bin_max, weight_mask)
        mean[n] = np.ma.average(cube.data,weights=weight_mask)
    return mean
