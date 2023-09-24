#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2013 DEVSIM LLC
#
# SPDX-License-Identifier: Apache-2.0

from devsim import *
from raser.raser.field.cal.si_simple_physics import *
import si_diode_common


import matplotlib.pyplot

import matplotlib.pyplot as plt
import matplotlib.tri as tri
import numpy as np
import pickle
from scipy.interpolate import griddata
# dio1
#
# Make doping a step function
# print dat to text file for viewing in grace
# verify currents analytically
# in dio2 add recombination
#

device="MyDevice"
region="MyRegion"

si_diode_common.Create2DMesh(device, region)

si_diode_common.SetParameters(device=device, region=region)

si_diode_common.SetNetDoping(device=device, region=region)

si_diode_common.InitialSolution(device, region)

# Initial DC solution
solve(type="dc", absolute_error=1e10, relative_error=1e-7, maximum_iterations=1000)
#solve(type="dc", absolute_error=1.0, relative_error=1e-12, maximum_iterations=30)

si_diode_common.DriftDiffusionInitialSolution(device, region)
###
### Drift diffusion simulation at equilibrium
###
solve(type="dc", absolute_error=1e10, relative_error=1e-7, maximum_iterations=1000)

####
#### Ramp the bias to 0.5 Volts
####
v = 0.0
delete_node_model(device=device, region=region, name="IntrinsicElectrons")
delete_node_model(device=device, region=region, name="IntrinsicHoles")
while v < 200:
    set_parameter(device=device, name=GetContactBiasName("bot"), value=v)
    solve(type="dc", absolute_error=1e10, relative_error=3e-1, maximum_iterations=1500)
    PrintCurrents(device, "bot")
    v += 1

"""
#irradiation
Holes_values = get_node_model_values(device=device, region=region, name="Holes")
Electrons_values = get_node_model_values(device=device, region=region, name="Electrons")

Holes_before=np.array(Holes_values)
Electrons_before=np.array(Electrons_values)
print(Electrons_values)
print(Holes_values)
for i in range(len(Holes_values)):
    USRH=1.5e3*(Electrons_values[i]*Holes_values[i]-1.0e20+1e16)/(1.5e-5*(Electrons_values[i]+1e10+Holes_values[i]+1e10))
    Holes_values[i]=(Holes_values[i]-USRH)/100
    Electrons_values[i]=(Electrons_values[i]+USRH)/100
    if(Holes_values[i]<0):
        Holes_values[i]=1
    if(Electrons_values[i]<0):
        Electrons_values[i]=1
Holes_after=np.array(Holes_values)
Electrons_after=np.array(Electrons_values)

#set_node_values(device=device, region=region,name="Holes",values=Holes_values)
#set_node_values(device=device, region=region,name="Electrons",values=Electrons_values)
set_node_values(device=device, region=region,name="Acceptors",values=Holes_values)
set_node_values(device=device, region=region,name="Donors",values=Electrons_values)
solve(type="dc", absolute_error=1e10, relative_error=1e-3, maximum_iterations=1500)
PrintCurrents(device, "top")
PrintCurrents(device, "bot")
"""

"""val = 10
for i in range(2):
    set_parameter(device=device, name=GetContactBiasName("top"), value=val)
    data = solve(type="dc", absolute_error=1e10, relative_error=1e-10, maximum_iterations=30, info=True)
    print(data['converged'])
    if not data['converged']:
      val = 0.6

print(data)
for i in data['iterations']:
    for d in i['devices']:
        for r in d['regions']:
            for e in r['equations']:
                print(e)"""

x = np.array(get_node_model_values(device=device, region=region, name="x")) # get x-node values
y = np.array(get_node_model_values(device=device, region=region, name="y")) # get y-node values
potential = np.array(get_node_model_values(device=device, region=region, name="Potential")) # get the potential dat

target_x = np.linspace(min(x), max(x), len(x))# Set grid x-value based on x-distances defined by the project
target_y = np.linspace(min(y), max(y), len(y))# Set grid y-value based on y-distances defined by the project
target_X, target_Y = np.meshgrid(target_x, target_y) # define the grid
# 进行插值
target_Z = griddata((x, y), potential, (target_X, target_Y), method='linear')
plt.contourf(target_x, target_y, target_Z, cmap='viridis')
plt.colorbar()
plt.xlabel('X')
plt.ylabel('Y')
plt.title('potential')
plt.savefig('fig/potential.png')
plt.close()


"""
target_HA=griddata((x, y), Holes_after, (target_X, target_Y), method='linear')
target_HB=griddata((x, y), Holes_before, (target_X, target_Y), method='linear')
target_EA=griddata((x, y), Electrons_after, (target_X, target_Y), method='linear')
target_EB=griddata((x, y), Electrons_before, (target_X, target_Y), method='linear')
target_DE=griddata((x, y), -Electrons_before+Electrons_after, (target_X, target_Y), method='linear')
target_DH=griddata((x, y), -Holes_before+Holes_after, (target_X, target_Y), method='linear')



plt.contourf(target_x, target_y, target_HA, cmap='viridis')
plt.colorbar()
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Holes_after')
plt.savefig('fig/Holes_after.png')
plt.close()

plt.contourf(target_x, target_y, target_HB, cmap='viridis')
plt.colorbar()
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Holes_before')
plt.savefig('fig/Holes_before.png')
plt.close()

plt.contourf(target_x, target_y, target_DE, cmap='viridis')
plt.colorbar()
plt.xlabel('X')
plt.ylabel('Y')
plt.title('DE')
plt.savefig('fig/DE.png')
plt.close()


plt.contourf(target_x, target_y, target_DH, cmap='viridis')
plt.colorbar()
plt.xlabel('X')
plt.ylabel('Y')
plt.title('DH')
plt.savefig('fig/DH.png')
plt.close()

plt.contourf(target_x, target_y, target_EA, cmap='viridis')
plt.colorbar()
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Electrons_after')
plt.savefig('fig/Electrons_after.png')
plt.close()

plt.contourf(target_x, target_y, target_EB, cmap='viridis')
plt.colorbar()
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Electrons_before')
plt.savefig('fig/Electrons_before.png')
plt.close()
"""


delete_node_model(device=device, region=region, name="IntrinsicElectrons:Potential")
delete_node_model(device=device, region=region, name="IntrinsicHoles:Potential")

write_devices(file="./output/testdiode/final_9", type="tecplot")