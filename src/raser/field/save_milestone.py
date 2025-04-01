import os
import pickle

import devsim
import numpy as np

from . import devsim_draw
from .create_parameter import create_parameter, delete_init
from util.output import create_path

def milestone_save_1D(device, region, v, path):
    x = np.array(devsim.get_node_model_values(device=device, region=region, name="x"))
    Potential = np.array(devsim.get_node_model_values(device=device, region=region, name="Potential")) # get the potential dat
    NetDoping= np.array(devsim.get_node_model_values(device=device, region=region, name="NetDoping"))
    PotentialNodeCharge = np.array(devsim.get_node_model_values(device=device, region=region, name="PotentialNodeCharge"))
    Electrons = np.array(devsim.get_node_model_values(device=device, region=region, name="Electrons"))
    Holes = np.array(devsim.get_node_model_values(device=device, region=region, name="Holes"))
    devsim.edge_average_model(device=device, region=region, node_model="x", edge_model="xmid")
    x_mid = devsim.get_edge_model_values(device=device, region=region, name="xmid") # get x-node values 
    ElectricField = devsim.get_edge_model_values(device=device, region=region, name="ElectricField") # get y-node values
    TrappingRate_n = np.array(devsim.get_node_model_values(device=device, region=region, name="TrappingRate_n"))
    TrappingRate_p = np.array(devsim.get_node_model_values(device=device, region=region, name="TrappingRate_p"))

    devsim_draw.draw1D(x,Potential,"Potential","Depth[cm]","Potential[V]", v, path)
    devsim_draw.draw1D(x_mid,ElectricField,"Electric Field","Depth[cm]","Electric Field[V/cm]", v, path)
    devsim_draw.draw1D(x,TrappingRate_n,"Electron Trapping Rate","Depth[cm]","Trapping Rate[s]", v, path)
    devsim_draw.draw1D(x,TrappingRate_p,"Hole Trapping Rate","Depth[cm]","Trapping Rate[s]", v, path)

    metadata = {}
    metadata['voltage'] = v
    metadata['dimension'] = 1

    names = ['Potential', 'TrappingRate_p', 'TrappingRate_n']
    if v == 0:
        names.append('NetDoping')

    for name in names: # scalar field on mesh point (instead of on edge)
        with open(os.path.join(path, "{}_{}V.pkl".format(name,v)),'wb') as file:
            data = {}
            data['values'] = eval(name) # refer to the object with given name
            data['points'] = x
            data['metadata'] = metadata
            pickle.dump(data, file)

def milestone_save_wf_1D(device, region, v, path, contact):
    save_wf_path = os.path.join(path, contact)
    create_path(save_wf_path)
    
    x = np.array(devsim.get_node_model_values(device=device, region=region, name="x")) # get x-node values
    Potential = np.array(devsim.get_node_model_values(device=device, region=region, name="Potential")) # get the potential data

    devsim.edge_average_model(device=device, region=region, node_model="x", edge_model="xmid")
    ElectricField=np.array(devsim.get_edge_model_values(device=device, region=region, name="ElectricField"))
    x_mid = np.array(devsim.get_edge_model_values(device=device, region=region, name="xmid")) 

    devsim_draw.draw1D(x,Potential,"Weighting Potential","Depth[cm]","Weighting Potential", v, save_wf_path)
    devsim_draw.draw1D(x_mid,ElectricField,"Weighting Field","Depth[cm]","Weighting Field[1/cm]",v, save_wf_path)

    metadata = {}
    metadata['voltage'] = v
    metadata['dimension'] = 1
    
    for name in ['Potential']: # scalar field on mesh point (instead of on edge)
        with open(os.path.join(save_wf_path, "{}_{}V.pkl".format(name,v)),'wb') as file:
            data = {}
            data['values'] = eval(name) # refer to the object with given name
            data['points'] = x
            data['metadata'] = metadata
            pickle.dump(data, file)

def milestone_save_2D(device, region, v, path):
    x = np.array(devsim.get_node_model_values(device=device, region=region, name="x")) # get x-node values
    y = np.array(devsim.get_node_model_values(device=device, region=region, name="y")) # get y-node values
    Potential = np.array(devsim.get_node_model_values(device=device, region=region, name="Potential")) # get the potential data
    TrappingRate_n = np.array(devsim.get_node_model_values(device=device, region=region, name="TrappingRate_n"))
    TrappingRate_p = np.array(devsim.get_node_model_values(device=device, region=region, name="TrappingRate_p"))
    NetDoping= np.array(devsim.get_node_model_values(device=device, region=region, name="NetDoping"))

    devsim.element_from_edge_model(edge_model="ElectricField",   device=device, region=region)
    devsim.edge_average_model(device=device, region=region, node_model="x", edge_model="xmid")
    devsim.edge_average_model(device=device, region=region, node_model="y", edge_model="ymid")
    ElectricField=np.array(devsim.get_edge_model_values(device=device, region=region, name="ElectricField"))
    x_mid = np.array(devsim.get_edge_model_values(device=device, region=region, name="xmid")) 
    y_mid = np.array(devsim.get_edge_model_values(device=device, region=region, name="ymid")) 

    devsim_draw.draw2D(x,y,Potential,"Potential",v, path)
    devsim_draw.draw2D(x_mid,y_mid,ElectricField,"ElectricField",v, path)
    devsim_draw.draw2D(x,y,TrappingRate_n,"TrappingRate_n",v, path)
    devsim_draw.draw2D(x,y,TrappingRate_p,"TrappingRate_p",v, path)

    metadata = {}
    metadata['voltage'] = v
    metadata['dimension'] = 2

    names = ['Potential', 'TrappingRate_p', 'TrappingRate_n']
    if v == 0:
        names.append('NetDoping')

    for name in names: # scalar field on mesh point (instead of on edge)
        with open(os.path.join(path, "{}_{}V.pkl".format(name,v)),'wb') as file:
            data = {}
            data['values'] = eval(name) # refer to the object with given name
            merged_list = [x, y]
            transposed_list = list(map(list, zip(*merged_list)))
            data['points'] = transposed_list
            data['metadata'] = metadata
            pickle.dump(data, file)


def milestone_save_wf_2D(device, region, v, path, contact):
    save_wf_path = os.path.join(path,contact)
    create_path(save_wf_path)

    x = np.array(devsim.get_node_model_values(device=device, region=region, name="x")) # get x-node values
    y = np.array(devsim.get_node_model_values(device=device, region=region, name="y")) # get y-node values
    Potential = np.array(devsim.get_node_model_values(device=device, region=region, name="Potential")) # get the potential data

    devsim.element_from_edge_model(edge_model="ElectricField",   device=device, region=region)
    devsim.edge_average_model(device=device, region=region, node_model="x", edge_model="xmid")
    devsim.edge_average_model(device=device, region=region, node_model="y", edge_model="ymid")
    ElectricField=np.array(devsim.get_edge_model_values(device=device, region=region, name="ElectricField"))
    x_mid = np.array(devsim.get_edge_model_values(device=device, region=region, name="xmid")) 
    y_mid = np.array(devsim.get_edge_model_values(device=device, region=region, name="ymid")) 

    devsim_draw.draw2D(x, y, Potential, "Potential", v, save_wf_path)
    devsim_draw.draw2D(x_mid, y_mid, ElectricField, "ElectricField", v, save_wf_path)

    metadata = {}
    metadata['voltage'] = v
    metadata['dimension'] = 2

    for name in ['Potential']: # scalar field on mesh point (instead of on edge)
        with open(os.path.join(save_wf_path, "{}_{}V.pkl".format(name,v)),'wb') as file:
            data = {}
            data['values'] = eval(name) # refer to the object with given name
            merged_list = [x, y]
            transposed_list = list(map(list, zip(*merged_list)))
            data['points'] = transposed_list
            data['metadata'] = metadata
            pickle.dump(data, file)

def milestone_save_3D(device, region, v, path):
    # not finished
    pass

def milestone_save_wf_3D(device, region, v, path,contact):
    # not finished
    pass

def save_milestone(device, region, v, path, dimension, contact, is_wf):
    if dimension ==1 :
        if is_wf == True:
            milestone_save_wf_1D(device, region, v, path, contact)
        elif is_wf == False:
            milestone_save_1D(device, region, v, path)
        else:
            print("==========RASER info ==========\nis_wf only has 2 values, True or False\n==========Error=========")
    if dimension == 2:
        if is_wf == True:
            milestone_save_wf_2D(device, region, v, path, contact)
        elif is_wf == False:
            milestone_save_2D(device, region, v, path)
        else:
            print("==========RASER info ==========\nis_wf only has 2 values, True or False\n==========Error=========")
    if dimension == 3:
        if is_wf == True:
            milestone_save_wf_3D(device, region, v, path, contact)
        elif is_wf == False:
            milestone_save_3D(device, region, v, path)
        else:
            print("==========RASER info ==========\nis_wf only has 2 values, True or False\n==========Error=========")

