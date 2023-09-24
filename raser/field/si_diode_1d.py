#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2013 DEVSIM LLC
#
# SPDX-License-Identifier: Apache-2.0

from devsim import *
from .si_simple_physics import *
from . import si_diode_common
import matplotlib.pyplot as plt
import numpy as np
import os
#####
# dio1
#
# Make doping a step function
# print dat to text file for viewing in grace
# verify currents analytically
# in dio2 add recombination
#
def main():
    device="MyDevice"
    region="MyRegion"

    si_diode_common.CreateMesh(device=device, region=region)

    si_diode_common.SetParameters(device=device, region=region)

    si_diode_common.SetNetDoping(device=device, region=region)

    si_diode_common.InitialSolution(device, region)

    # Initial DC solution
    solve(type="dc", absolute_error=1.0, relative_error=1e-7, maximum_iterations=1000)

    si_diode_common.DriftDiffusionInitialSolution(device, region)
    ###
    ### Drift diffusion simulation at equilibrium
    ###
    solve(type="dc", absolute_error=1e10, relative_error=1e-7, maximum_iterations=1000)


    ####
    #### Ramp the bias to 0.5 Volts
    ####
    reverse_bot_current=[]
    v = 0.0
    delete_node_model(device=device, region=region, name="IntrinsicElectrons")
    delete_node_model(device=device, region=region, name="IntrinsicHoles")
    while v < 300:
        set_parameter(device=device, name=GetContactBiasName("bot"), value=v)
        solve(type="dc", absolute_error=1e10, relative_error=1e-3, maximum_iterations=1500)
        PrintCurrents(device, "top")
        PrintCurrents(device, "bot")
        reverse_top_electron_current= get_contact_current(device=device, contact="bot", equation="ElectronContinuityEquation")
        reverse_top_hole_current    = get_contact_current(device=device, contact="bot", equation="HoleContinuityEquation")
        reverse_top_total_current   = reverse_top_electron_current + reverse_top_hole_current
        reverse_bot_current.append(abs(reverse_top_total_current))
        v += 1


    x = np.array(get_node_model_values(device=device, region=region, name="x"))
    potential = np.array(get_node_model_values(device=device, region=region, name="Potential")) # get the potential dat
    NetDoping= np.array(get_node_model_values(device=device, region=region, name="NetDoping"))
    PotentialNodeCharge = np.array(get_node_model_values(device=device, region=region, name="PotentialNodeCharge"))
    Electrons = np.array(get_node_model_values(device=device, region=region, name="Electrons"))
    Holes = np.array(get_node_model_values(device=device, region=region, name="Holes"))

    if not os.access('output/testdiode', os.F_OK):
            os.makedirs('output/testdiode', exist_ok=True)

    plt.plot(x,potential)
    plt.xlabel('X')
    plt.ylabel('potential')
    plt.title('potential')
    plt.savefig('output/testdiode/potential_1d.png')
    plt.close()

    plt.plot(x,NetDoping)
    plt.xlabel('X')
    plt.ylabel('NetDoping')
    plt.title('NetDoping')
    plt.savefig('output/testdiode/NetDoping_1d.png')
    plt.close()

    plt.plot(x,PotentialNodeCharge)
    plt.xlabel('X')
    plt.ylabel('PotentialNodeCharge')
    plt.title('PotentialNodeCharge')
    plt.savefig('output/testdiode/PotentialNodeCharge_1d.png')
    plt.close()

    plt.plot(x,Electrons)
    plt.xlabel('X')
    plt.ylabel('Electrons')
    plt.title('Electrons')
    plt.savefig('output/testdiode/Electrons_1d.png')
    plt.close()

    plt.plot(x,Holes)
    plt.xlabel('X')
    plt.ylabel('Holes')
    plt.title('Holes')
    plt.savefig('output/testdiode/Holes_1d.png')
    plt.close()
    edge_average_model(device=device, region=region, node_model="x", edge_model="xmid")
    x_mid = get_edge_model_values(device=device, region=region, name="xmid") # get x-node values 
    ElectricField = get_edge_model_values(device=device, region=region, name="ElectricField") # get y-node values
    plt.plot(x_mid,ElectricField)
    plt.xlabel('X')
    plt.ylabel('ElectricField')
    plt.title('ElectricField')
    plt.savefig('output/testdiode/ElectricField_1d.png')
    plt.close()

    delete_node_model(device=device, region=region, name="IntrinsicElectrons:Potential")
    delete_node_model(device=device, region=region, name="IntrinsicHoles:Potential")
    write_devices(file="./output/testdiode/si_ir_1d", type="tecplot")

    
if __name__ == "__main__":
    main()    