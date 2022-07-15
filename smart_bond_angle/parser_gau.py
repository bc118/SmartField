#!/usr/bin/env python3

import numpy as np

def range2(start, end):
     return range(start, end+1)

def flat_list(lis):
    flatList = []
    # Iterate with outer list
    for element in lis:
        if type(element) is list:
            # Check if type is list than iterate through the sublist
            for item in element:
                flatList.append(item)
        else:
            flatList.append(element)
    return flatList
 
def store_any_file(fname):
    """ 
    Reading Any file 
    """
    with open(fname, 'r') as f:
        all_lines = []
        for line in f:
            all_lines.append(line.strip())

    return all_lines

def read_XYZ(all_lines):
    """ 
    Reading CC XYZ from fchk file 
    """
    # with open(fname, 'r') as f:
    #     all_lines = []
    #     for line in f:
    #         all_lines.append(line.strip())

    for s in range(len(all_lines)):                          # Get no of Atoms
        if 'Number of atoms' in all_lines[s]:
            Natom = int(all_lines[s][-10:])  
        
    No_cc = 3* Natom
    nlines = int(No_cc/5.0) + 1
    cc_xyz_list = []
    for s in range(len(all_lines)):                          #  Get CC Coordinates
        if 'Current cartesian coordinates' in all_lines[s]:                              #Reads the Input orientation information
            start = s
            for e in range2(start + 1, start + nlines):
                cc_xyz_list.append(all_lines[e].split() )
    
    cc_xyz_flat = flat_list(cc_xyz_list)
    cc_xyz_1D = np.array(cc_xyz_flat, float)

    # Take out Garbage Strings
    if len(cc_xyz_flat) != No_cc:
        diff = abs(len(cc_xyz_flat) - No_cc)
        cc_xyz_flat_mod = cc_xyz_flat[:-diff]
        cc_xyz_1D = np.array(cc_xyz_flat_mod, float)
    else:
        cc_xyz_1D = np.array(cc_xyz_flat, float)

    cc_xyz_arr = np.reshape(cc_xyz_1D, (Natom,3))
    cc_xyz_arr = cc_xyz_arr*0.529177                          # Convert from Bohr to Ang.
    
    return Natom, cc_xyz_arr

def read_RicDim_Grad(all_lines):
    """ 
    Reading Redundant Internal Dimension &
    Gradient from fchk file 
    """

    for s in range(len(all_lines)):                          # Get no of Atoms
        if 'Redundant internal dimensions' in all_lines[s]:
            tmp_list = all_lines[s+1].split()
            ric_list = list(map(int,tmp_list))

    force_list = []
    for s in range(len(all_lines)):                          # Get no of Atoms
        if 'Internal Forces' in all_lines[s]:
            N_force = int(all_lines[s][-10:])
            nlines = int(N_force/5.0) + 1
            start = s
            for e in range2(start + 1, start + nlines):
                force_list.append(all_lines[e].split() )
    
    
    force_flat = flat_list(force_list)

    # Take out Garbage Strings
    if len(force_flat) != N_force:
        diff = abs(len(force_flat) - N_force)
        force_flat_mod = force_flat[:-diff]
        force_1D = np.array(force_flat_mod, float)
    else:
        force_1D = np.array(force_flat,float)

    return ric_list, force_1D


def symmetricize(arr1D):
    ID = np.arange(arr1D.size)
    return arr1D[np.abs(ID - ID[:,None])]


def fill_lower_diag(a):
    n = int(np.sqrt(len(a)*2))+1
    mask = np.tri(n,dtype=bool, k=-1) # or np.arange(n)[:,None] > np.arange(n)
    out = np.zeros((n,n),dtype=int)
    out[mask] = a
    return out

def read_Hess(all_lines, ric_list):
    """ 
    Reading Internal Hessian from fchk file:
    all_lines : text file
    ric_list = [RICs, BONDs, ANGLEs, DIHEs]  
    """

    hess_list = []
    for s in range(len(all_lines)):                          # Get no of Atoms
        if 'Internal Force Constants' in all_lines[s]:
            N_hess = int(all_lines[s][-10:])
            nlines = int(N_hess/5.0) + 1
            start = s
            for e in range2(start + 1, start + nlines):
                hess_list.append(all_lines[e].split() )
    
    hess_flat = flat_list(hess_list)

    # Take out Garbage Strings
    if len(hess_flat) != N_hess:
        diff = abs(len(hess_flat)-N_hess)
        # print('diff = ', diff)
        hess_flat_mod = hess_flat[:-diff]
        hess_1D = np.array(hess_flat_mod, float)
    else:
        hess_1D = np.array(hess_flat,float)

    hess_1D_mod = np.append(hess_1D, [0])
    # print(hess_1D_mod)

    # print(len(hess_1D))
    ric_len = ric_list[0]
    # print(ric_len)
    hess_arr = np.zeros((ric_len, ric_len))
    # print(hess_arr.shape, hess_arr.size)
    mylist = []
    for i in range(ric_len+1):
        # i_low = int( 0.5 * i * (i - 1) + -1 )           # Adding n(n+1)/2 elements in up/low triangular matrix
        i_low = int( 0.5 * i * (i - 1)  )           # Adding n(n+1)/2 elements in up/low triangular matrix
        # i_up = int( 0.5 * i *  (i + 1) + 1 )
        i_up = int( 0.5 * i *  (i + 1)   )
        # print(i, i_low, i_up, hess_1D[i_low:i_up])
        hess_arr[i-1,0:i] =  hess_1D[i_low: i_up]
        hess_arr[0:i,i-1] =  hess_1D[i_low: i_up]

    return hess_arr
    # np.set_printoptions(precision=3)
    # for i in hess_arr:
    #     print(f'{i}')


def read_NamesTypes(all_lines, N_atoms):
    """ 
    Reading Aom Names from log file:
    """
    ele_list = []
    type_list = []
    for s in range(len(all_lines)):                          # Get no of Atoms
        if 'Symbolic Z-matrix' in all_lines[s]:
            start = s
            for e in range(start+2, start + N_atoms+1):
                ele_list.append(all_lines[e][:1].split() )
                type_list.append(all_lines[e][2:5].split() )

    return ele_list, type_list
    

def read_Top(all_lines, ric_list):
    """ 
    Reading Topology from RIC:
    """
    tmp_list = []
    ric_tot = ric_list[0]
    for s in range(len(all_lines)):                          # Get no of Atoms
        if 'Name' in all_lines[s]:
            start = s
            # print(all_lines[s])
            for e in range(start+2, start + ric_tot+2):
                tmp_list.append(all_lines[e][8:25].strip())
            break
   

    n_bonds = 0
    n_angles = 0
    n_dihe = 0
    bond_list = []
    angle_list = []
    dihe_list = []
    for i in range(len(tmp_list)):
        if tmp_list[i][0] == 'R':
           n_bonds += 1 
           bond_list.append(tmp_list[i][2 : -1].replace(','," ").split())
        elif tmp_list[i][0] == 'A':
           n_angles += 1 
           angle_list.append(tmp_list[i][2 : -1].replace(','," ").split())
        elif tmp_list[i][0] == 'D':
           n_dihe += 1 
           dihe_list.append(tmp_list[i][2 : -1].replace(','," ").split())

    bond_list = [list(map(int, x)) for x in bond_list]
    angle_list = [list(map(int, x)) for x in angle_list]
    dihe_list = [list(map(int, x)) for x in dihe_list]

    return bond_list, angle_list, dihe_list
    

   
