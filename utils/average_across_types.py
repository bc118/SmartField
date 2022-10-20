#!/usr/bin/env python3

import numpy as np
np.seterr(divide='ignore', invalid='ignore')

def get_one_hot(values, indexes):
    one_hot = np.eye(np.max(indexes) + 1)[indexes]
    counts = np.sum(one_hot, axis=0)
    average = np.sum((one_hot.T * values), axis=1) / counts
    average = average[~np.isnan(average)]             # Remove NaN 
    return average

def reduce_bond_list(bond_list):
    splitted = list()
    [ splitted.append(i.split()) for i in bond_list]
    data = { (tuple(sorted(item))) for item in splitted}
    new = list(map(list, data))
    reduced = list(' '.join(item) for item in new)
    return reduced

def reduce_angle_list(angle_list, k_angles):
    splitted = [ i.split() for i in angle_list]
    res_bonds = splitted.copy()
    indexes = [i for i in range(len(splitted))]
    for i in range(len(splitted[:])-1):
        for j in range(i+1,len(splitted[:])):
            if (splitted[i] == splitted[j][::-1]) and (i !=j) :
                print(i,j)
                res_bonds.pop(i)
                indexes[j] = indexes[i]
                break
    reduced = list(' '.join(item) for item in res_bonds)

    indexes = np.array(indexes)
    k_angles_ave = get_one_hot(k_angles, indexes)

    return reduced, k_angles_ave



