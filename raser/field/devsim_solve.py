#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
import devsim 
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from . import model_create
from . import physics_drift_diffusion
from . import initial
# import Setting

from .build_device import Detector

import matplotlib 
import matplotlib.pyplot
import ROOT
import numpy as np
import csv
import pickle
import math

if not (os.path.exists("./output/devsim")):
    os.makedirs("./output/devsim")

def main(label=None,v_max = 400):
    devsim.open_db(filename="./output/field/SICARDB.db", permission="readonly")
    if label=='sicar1.1.8_cv_v1':
        device = "SICAR-1.1.8"
        region = "SICAR-1.1.8"
        area_factor = 100.0
        set_mesh(device,region)
        extend_set()
        para_dict = []
        initial_solution(device,region,para_dict)  
        solve_cv(device,region,v_max,para_dict,area_factor,frequency=1e3)
    elif label=='sicar1.1.8_iv_v1':
        area_factor=1.0/(0.1*0.1)
        v_max=510
        device = "SICAR-1.1.8"
        region = "SICAR-1.1.8"
        para_dict=[]
        set_mesh(device,region)
        # devsim.set_parameter(device=device,   name="tau_n",  value=2.5e-6)
        # devsim.set_parameter(device=device,   name="tau_p",  value=0.5e-6)
        extend_set()
        initial_solution(device,region,para_dict)
        solve_iv(device,region,v_max,para_dict,area_factor)
    elif label=='1d_njupin_1.5mm_cv':
        area_factor=44.44
        device = "NJU-PIN"
        region = "NJU-PIN"
        para_dict=[]
        set_mesh(device,region)
        extend_set()
        initial_solution(device,region,para_dict)
        solve_cv(device,region,v_max,para_dict,area_factor,frequency=1.0)    
    elif label=='itkmd8_cv_v1':
        area_factor=1.0/(0.76*0.76)
        device = "ITk-md8"
        region = "ITk-md8"
        para_dict=[]
        set_mesh(device,region)
        extend_set()
        initial_solution(device,region,para_dict)
        solve_cv(device,region,v_max,para_dict,area_factor,frequency=1.0)
        return
    elif label=='itkmd8_iv_v1':
        area_factor=1.0/(0.76*0.76)
        v_max=700
        device = "ITk-md8"
        region = "ITk-md8"
        para_dict=[]
        devsim.set_parameter(device=device,   name="tau_n",  value=3e-2)
        devsim.set_parameter(device=device,   name="tau_p",  value=3e-2)
        set_mesh(device,region)
        extend_set()
        initial_solution(device,region,para_dict)
        solve_iv(device,region,v_max,para_dict,area_factor)
    elif label=='itkatlas18_iv_v1':
        area_factor=1.0/(10.0*10.0)
        v_max=700
        device = "ITk-Si-strip"
        region = "ITk-Si-strip"
        para_dict=[]
        set_mesh(device,region)
        devsim.set_parameter(device=device,   name="tau_n",  value=3e-2)
        devsim.set_parameter(device=device,   name="tau_p",  value=3e-2)
        extend_set()
        initial_solution(device,region,para_dict)
        solve_iv(device,region,v_max,para_dict,area_factor)
    elif label=='njupin_cv_v1':
        device = "NJU-PIN"
        region = "NJU-PIN"
        area_factor = 4
        set_mesh(device,region)
        extend_set()
        para_dict = []
        initial_solution(device,region,para_dict)  
        solve_cv(device,region,v_max,para_dict,area_factor,frequency=1)
    elif label == "si_ir_1d":
        v=v_max
        device = 'HPK-Si-PIN'
        region = 'HPK-Si-PIN'
        area_factor = 1
        set_mesh(device,region)
        extend_set()
        para_dict = []
        initial_solution(device,region,para_dict)
        devsim.delete_node_model(device=device, region=region, name="IntrinsicElectrons")
        devsim.delete_node_model(device=device, region=region, name="IntrinsicHoles")  
        solve_iv(device,region,v_max,para_dict,area_factor)
        
        x = np.array(devsim.get_node_model_values(device=device, region=region, name="x"))
        potential = np.array(devsim.get_node_model_values(device=device, region=region, name="Potential")) # get the potential dat
        NetDoping= np.array(devsim.get_node_model_values(device=device, region=region, name="NetDoping"))
        PotentialNodeCharge = np.array(devsim.get_node_model_values(device=device, region=region, name="PotentialNodeCharge"))
        Electrons = np.array(devsim.get_node_model_values(device=device, region=region, name="Electrons"))
        Holes = np.array(devsim.get_node_model_values(device=device, region=region, name="Holes"))
        devsim.edge_average_model(device=device, region=region, node_model="x", edge_model="xmid")
        x_mid = devsim.get_edge_model_values(device=device, region=region, name="xmid") # get x-node values 
        ElectricField = devsim.get_edge_model_values(device=device, region=region, name="ElectricField") # get y-node values
        TrappingRate_n = np.array(devsim.get_node_model_values(device=device, region=region, name="TrappingRate_n"))
        TrappingRate_p = np.array(devsim.get_node_model_values(device=device, region=region, name="TrappingRate_p"))

        if not os.access('output/testdiode', os.F_OK):
                os.makedirs('output/testdiode', exist_ok=True)

        draw1D(x,potential,"Potential","Depth[cm]","Potential[V]",v)
        draw1D(x_mid,ElectricField,"ElectricField","Depth[cm]","ElectricField[V/cm]",v)
        draw1D(x,TrappingRate_n,"TrappingRate_n","Depth[cm]","TrappingRate_n[s]",v)
        draw1D(x,TrappingRate_p,"TrappingRate_p","Depth[cm]","TrappingRate_p[s]",v)

        devsim.delete_node_model(device=device, region=region, name="IntrinsicElectrons:Potential")
        devsim.delete_node_model(device=device, region=region, name="IntrinsicHoles:Potential")
        devsim.write_devices(file="./output/testdiode/si_diode_1d", type="tecplot")

    elif label == "si_ir_2d":
        v=v_max
        device='ITk-Si-strip'
        region='ITk-Si-strip'
        area_factor = 1
        set_mesh(device,region)
        extend_set()
        para_dict = []
        initial_solution(device,region,para_dict)
        devsim.delete_node_model(device=device, region=region, name="IntrinsicElectrons")
        devsim.delete_node_model(device=device, region=region, name="IntrinsicHoles")  
        solve_iv(device,region,v_max,para_dict,area_factor)
        if not os.access('output/strip', os.F_OK):
            os.makedirs('output/strip', exist_ok=True)
        
        x = np.array(devsim.get_node_model_values(device=device, region=region, name="x")) # get x-node values
        y = np.array(devsim.get_node_model_values(device=device, region=region, name="y")) # get y-node values
        potential = np.array(devsim.get_node_model_values(device=device, region=region, name="Potential")) # get the potential data
        TrappingRate_n = np.array(devsim.get_node_model_values(device=device, region=region, name="TrappingRate_n"))
        TrappingRate_p = np.array(devsim.get_node_model_values(device=device, region=region, name="TrappingRate_p"))

        devsim.element_from_edge_model(edge_model="ElectricField",   device=device, region=region)
        devsim.edge_average_model(device=device, region=region, node_model="x", edge_model="xmid")
        devsim.edge_average_model(device=device, region=region, node_model="y", edge_model="ymid")
        ElectricField=np.array(devsim.get_edge_model_values(device=device, region=region, name="ElectricField"))
        x_mid = np.array(devsim.get_edge_model_values(device=device, region=region, name="xmid")) 
        y_mid = np.array(devsim.get_edge_model_values(device=device, region=region, name="ymid")) 

        draw2D(x,y,potential,"potential",v)
        draw2D(x_mid,y_mid,ElectricField,"ElectricField",v)
        draw2D(x,y,TrappingRate_n,"TrappingRate_n",v)
        draw2D(x,y,TrappingRate_p,"TrappingRate_p",v)

        devsim.delete_node_model(device=device, region=region, name="IntrinsicElectrons:Potential")
        devsim.delete_node_model(device=device, region=region, name="IntrinsicHoles:Potential")

        devsim.write_devices(file="./output/strip/si_diode_2d", type="tecplot")

        with open("./output/strip/potential_{}_1e15_.pkl".format(v),'wb') as file:
            pickle.dump(potential, file)
        with open("./output/strip/x.pkl",'wb') as file:
            pickle.dump(x, file)
        with open("./output/strip/y.pkl",'wb') as file:
            pickle.dump(y, file)
        with open("./output/strip/TrappingRate_p_1e15_{}.pkl".format(v),'wb') as file:
            pickle.dump(TrappingRate_p, file)
        with open("./output/strip/TrappingRate_n_1e15_{}.pkl".format(v),'wb') as file:
            pickle.dump(TrappingRate_n, file)
    else:
        raise KeyError
        

def set_para(para_list):
    para_dict={}
    for para in para_list:
        key,_,value=para.rpartition('=')
        para_dict[key]=value
    return para_dict

def set_mesh(device,region):
    if device == "SICAR-1.1.8" or device == "NJU-PIN":
        MyDetector = Detector(device, 1)
    elif device == "ITk-md8" or device == "HPK-Si-PIN":
        MyDetector = Detector(device, 1)
    else:
        MyDetector = Detector(device, 2)

def extend_set():
    devsim.set_parameter(name = "extended_solver", value=True)
    devsim.set_parameter(name = "extended_model", value=True)
    devsim.set_parameter(name = "extended_equation", value=True)
    devsim.circuit_element(name="V1", n1=physics_drift_diffusion.GetContactBiasName("top"), n2=0, value=0.0, acreal=1.0, acimag=0.0)

def initial_solution(device,region,para_dict):
    # Initial DC solution
    initial.InitialSolution(device, region, circuit_contacts="top")
    devsim.solve(type="dc", absolute_error=1.0, relative_error=1e-10, maximum_iterations=50)

    if "irradiation" in para_dict:
        if device == "ITk-md8":
            initial.DriftDiffusionInitialSolutionSiIrradiated(
                device, region, circuit_contacts="top")
            devsim.set_parameter(device=device, 
            name=physics_drift_diffusion.GetContactBiasName("top"), value=0)
        else:
            initial.DriftDiffusionInitialSolutionIrradiated(
                device, region, circuit_contacts="top")
    else:
    ### Drift diffusion simulation at equilibrium
        initial.DriftDiffusionInitialSolution(device, region, circuit_contacts="top")
        devsim.solve(type="dc", absolute_error=1e10, relative_error=1e-10, maximum_iterations=50)
        
def set_defect(paras):
    #Z_1/2
    devsim.add_db_entry(material="global",   parameter="sigma_n",     value=float(paras["sigma_n"]),   unit="s/cm^2",     description="sigma_n")
    devsim.add_db_entry(material="global",   parameter="sigma_p",     value=float(paras["sigma_p"]),   unit="s/cm^2",     description="sigma_p")
    devsim.add_db_entry(material="global",   parameter="N_t",     value=float(paras["N_t"]),   unit="cm^(-3)",     description="N_t")
    #EH_6/7
    devsim.add_db_entry(material="global",   parameter="sigma_n_HS6",     value=float(paras["sigma_n_HS6"]),   unit="s/cm^2",     description="sigma_n_HS6")
    devsim.add_db_entry(material="global",   parameter="sigma_p_HS6",     value=float(paras["sigma_p_HS6"]),   unit="s/cm^2",     description="sigma_p_HS6")
    devsim.add_db_entry(material="global",   parameter="N_t_HS6",     value=float(paras["N_t_HS6"]),   unit="cm^(-3)",     description="N_t_HS6")

def solve_iv(device,region,v_max,para_dict,area_factor):
    condition = ""
    if "irradiation" in para_dict:
        condition += "_irradiation"
    if "defect" in para_dict:
        condition += "_defect"
        for key in ["N_t","sigma_n","sigma_p","N_t_HS6","sigma_n_HS6","sigma_p_HS6"]:
            condition += "_{}={}".format(key,para_dict[key])
    reverse_v = 0.0
    reverse_voltage = []
    reverse_top_current = []
    reverse_bot_current = []

    v_max_field=v_max

    f_iv = open("./output/devsim/{}_reverse_iv.csv".format(device+condition), "w")
    header_iv = ["Voltage","Current"]
    writer_iv = csv.writer(f_iv)
    writer_iv.writerow(header_iv)

    positions_mid = []
    intensities = []
    bias_voltages = []

    positions = []
    electrons = []
    holes = []

    while reverse_v < v_max:
        reverse_top_total_current = solve_iv_single_point(device,region,reverse_v)
        reverse_top_current.append(abs(reverse_top_total_current))

        writer_iv.writerow([0-reverse_v,abs(reverse_top_total_current/area_factor)])       

        voltage_step = 100
        if(reverse_v%voltage_step==0.0 and reverse_v<=v_max_field):
            devsim.edge_average_model(device=device, region=region, node_model="x", edge_model="xmid")
            x_mid = devsim.get_edge_model_values(device=device, region=region, name="xmid") # get x-node values 
            E = devsim.get_edge_model_values(device=device, region=region, name="ElectricField") # get y-node values
            V = reverse_v

            x = devsim.get_node_model_values(device=device, region=region, name="x") # get x-node values 
            n = devsim.get_node_model_values(device=device, region=region, name="Electrons")
            p = devsim.get_node_model_values(device=device, region=region, name="Holes")

            positions_mid.append(x_mid)
            intensities.append(E)
            bias_voltages.append(V)

            positions.append(x)
            electrons.append(n)
            holes.append(p)

        reverse_voltage.append(0-reverse_v)
        reverse_v += 1


    f_iv.close()
    devsim.close_db()

    draw_iv(reverse_voltage, reverse_top_current, device, condition)
    draw_ele_field(device, positions_mid, intensities, bias_voltages, condition)
    draw_electrons(device, positions, electrons, bias_voltages, condition)
    draw_holes(device, positions, holes, bias_voltages, condition)
    save_ele_field(device, positions, intensities, bias_voltages, condition)
    

def solve_iv_backtest(device,region,v_max,para_dict,backthickness,back_doping):
    condition = ""
    if "irradiation" in para_dict:
        condition += "_irradiation"
    if "defect" in para_dict:
        condition += "_defect"
        for key in ["N_t","sigma_n","sigma_p","N_t_HS6","sigma_n_HS6","sigma_p_HS6"]:
            condition += "_{}={}".format(key,para_dict[key])
    reverse_v = 0.0
    reverse_voltage = []
    reverse_top_current = []
    reverse_bot_current = []

    v_max_field=v_max

    f_iv = open("./output/devsim/{}_reverse_iv.csv".format(device+condition), "w")
    header_iv = ["Voltage","Current"]
    writer_iv = csv.writer(f_iv)
    writer_iv.writerow(header_iv)

    positions_mid = []
    intensities = []
    bias_voltages = []

    positions = []
    electrons = []
    holes = []

    while reverse_v < v_max:
        reverse_top_total_current = solve_iv_single_point(device,region,reverse_v)
        reverse_top_current.append(abs(reverse_top_total_current))

        writer_iv.writerow([0-reverse_v,abs(reverse_top_total_current/area_factor)])

        voltage_step = 100
        if(reverse_v%voltage_step==0.0 and reverse_v<=v_max_field):
            devsim.edge_average_model(device=device, region=region, node_model="x", edge_model="xmid")
            x_mid = devsim.get_edge_model_values(device=device, region=region, name="xmid") # get x-node values 
            E = devsim.get_edge_model_values(device=device, region=region, name="ElectricField") # get y-node values
            V = reverse_v

            x = devsim.get_node_model_values(device=device, region=region, name="x") # get x-node values 
            n = devsim.get_node_model_values(device=device, region=region, name="Electrons")
            p = devsim.get_node_model_values(device=device, region=region, name="Holes")

            positions_mid.append(x_mid)
            intensities.append(E)
            bias_voltages.append(V)

            positions.append(x)
            electrons.append(n)
            holes.append(p)


        if device == "ITk-md8":
            reverse_voltage.append(reverse_v)
        else:
            reverse_voltage.append(0-reverse_v)
        reverse_v += 1


    f_iv.close()
    devsim.close_db()

    draw_iv(reverse_voltage, reverse_top_current, device, condition)
    draw_ele_field(device, positions_mid, intensities, bias_voltages, condition)
    draw_electrons(device, positions, electrons, bias_voltages, condition)
    draw_holes(device, positions, holes, bias_voltages, condition)
    save_ele_field(device, positions, intensities, bias_voltages, condition)


def solve_iv_Rirr(device,region,Rirr,v_max,area_factor,para_dict):
    condition = ""
    if "irradiation" in para_dict:
        condition += "_irradiation"
    if "defect" in para_dict:
        condition += "_defect"
        for key in ["N_t","sigma_n","sigma_p","N_t_HS6","sigma_n_HS6","sigma_p_HS6"]:
            condition += "_{}={}".format(key,para_dict[key])
    reverse_v = 0.0
    reverse_voltage = []
    reverse_top_current = []
    reverse_bot_current = []

    v_max_field=v_max

    f_iv = open("./output/devsim/{}_reverse_iv.csv".format(device+condition), "w")
    header_iv = ["Voltage","Current"]
    writer_iv = csv.writer(f_iv)
    writer_iv.writerow(header_iv)

    positions_mid = []
    intensities = []
    bias_voltages = []

    positions = []
    electrons = []
    holes = []

    while reverse_v < v_max:
        reverse_top_total_current = solve_iv_single_point(device,region,reverse_v)
        reverse_top_current.append(abs(reverse_top_total_current))

        writer_iv.writerow([0-reverse_v,abs(reverse_top_total_current/area_factor)])

        voltage_step = 100
        if(reverse_v%voltage_step==0.0 and reverse_v<=v_max_field):
            devsim.edge_average_model(device=device, region=region, node_model="x", edge_model="xmid")
            x_mid = devsim.get_edge_model_values(device=device, region=region, name="xmid") # get x-node values 
            E = devsim.get_edge_model_values(device=device, region=region, name="ElectricField") # get y-node values
            V = reverse_v

            x = devsim.get_node_model_values(device=device, region=region, name="x") # get x-node values 
            n = devsim.get_node_model_values(device=device, region=region, name="Electrons")
            p = devsim.get_node_model_values(device=device, region=region, name="Holes")

            positions_mid.append(x_mid)
            intensities.append(E)
            bias_voltages.append(V)

            positions.append(x)
            electrons.append(n)
            holes.append(p)


        if device == "ITk-md8":
            reverse_voltage.append(reverse_v)
        else:
            reverse_voltage.append(0-reverse_v)
        reverse_v += 1


    f_iv.close()
    devsim.close_db()

    draw_iv(reverse_voltage, reverse_top_current, device, condition)
    draw_ele_field(device, positions_mid, intensities, bias_voltages, condition)
    draw_electrons(device, positions, electrons, bias_voltages, condition)
    draw_holes(device, positions, holes, bias_voltages, condition)
    save_ele_field(device, positions, intensities, bias_voltages, condition)

def solve_cv(device,region,v_max,para_dict,area_factor, frequency):
    condition = ""
    if "irradiation" in para_dict:
        condition += "_irradiation"
    if "defect" in para_dict:
        condition += "_defect"
        for key in ["N_t","sigma_n","sigma_p","N_t_HS6","sigma_n_HS6","sigma_p_HS6"]:
            condition += "_{}={}".format(key,para_dict[key])
    reverse_v = 0.0
    reverse_voltage = []
    ssac_top_cap = []

    f_cv = open("./output/devsim/{0}_reverse_cv.csv".format(device+condition), "w")
    header_cv = ["Voltage","Capacitance"]
    writer_cv = csv.writer(f_cv)
    writer_cv.writerow(header_cv)

    while reverse_v < v_max:
        capacitance = solve_cv_single_point(device,region,reverse_v,frequency)
        ssac_top_cap.append(capacitance*(1e12)/area_factor)

        writer_cv.writerow([0-reverse_v,capacitance*(1e12)/area_factor])
        reverse_voltage.append(0-reverse_v)
        reverse_v += 1

    f_cv.close()
    devsim.close_db()
    draw_cv(reverse_voltage, ssac_top_cap, device,condition)

def solve_iv_single_point(device,region,reverse_v):
    devsim.set_parameter(device=device, name=physics_drift_diffusion.GetContactBiasName("top"), value=0-reverse_v)
    devsim.solve(type="dc", absolute_error=1e10, relative_error=1e-5, maximum_iterations=1000)
    physics_drift_diffusion.PrintCurrents(device, "top")
    physics_drift_diffusion.PrintCurrents(device, "bot")
    reverse_top_electron_current= devsim.get_contact_current(device=device, contact="top", equation="ElectronContinuityEquation")
    reverse_top_hole_current    = devsim.get_contact_current(device=device, contact="top", equation="HoleContinuityEquation")
    reverse_top_total_current   = reverse_top_electron_current + reverse_top_hole_current

    return reverse_top_total_current

def solve_cv_single_point(device,region,reverse_v,frequency):
    devsim.circuit_alter(name="V1", value=0-reverse_v)
    devsim.solve(type="dc", absolute_error=1e10, relative_error=1e-5, maximum_iterations=1000)
    physics_drift_diffusion.PrintCurrents(device, "bot")
    devsim.solve(type="ac", frequency=frequency)
    cap=devsim.get_circuit_node_value(node="V1.I", solution="ssac_imag")/ (-2*math.pi*frequency)
    print("capacitance {0} {1}".format(reverse_v, cap))
    return cap

def draw_iv(V,I,device,condition):
    fig2=matplotlib.pyplot.figure()
    matplotlib.pyplot.semilogy(V,I)
    matplotlib.pyplot.xlabel('Voltage (V)')
    matplotlib.pyplot.ylabel('Current (A)')
    fig2.savefig("./output/devsim/{}_reverse_iv.png".format(device+condition))
    fig2.clear()

def draw_cv(V,C,device,condition):
    fig3=matplotlib.pyplot.figure(num=4,figsize=(4,4))
    matplotlib.pyplot.plot(V, C)
    matplotlib.pyplot.xlabel('Voltage (V)')
    matplotlib.pyplot.ylabel('Capacitance (pF)')
    #matplotlib.pyplot.axis([-200, 0, 0, 20])
    fig3.savefig("./output/devsim/{0}_reverse_cv.png".format(device+condition))
    fig3.clear()

    fig4=matplotlib.pyplot.figure(num=4,figsize=(4,4))
    C_minus2 = []
    for c in C:
        C_minus2.append(1/c**2)
    matplotlib.pyplot.plot(V, C_minus2)
    matplotlib.pyplot.xlabel('Voltage (V)')
    matplotlib.pyplot.ylabel('1/C^2 (pF^{-2})')
    #matplotlib.pyplot.axis([-200, 0, 0, 20])
    fig4.savefig("./output/devsim/{0}_reverse_c^-2v.png".format(device+condition))
    fig4.clear()

def draw_ele_field(device, positions,intensities, bias_voltages,condition):
    fig1=matplotlib.pyplot.figure()
    ax1 = fig1.add_subplot(111)
    for (x,E,V) in zip(positions,intensities, bias_voltages):
        matplotlib.pyplot.plot(x,E,label="%s"%(str(V)))
    matplotlib.pyplot.xlabel('Depth [cm]')
    matplotlib.pyplot.ylabel('E (V/cm)')
    matplotlib.pyplot.ticklabel_format(axis="y", style="sci", scilimits=(0,0))
    ax1.legend(loc='upper right')
    if device == "SICAR-1.1.8":
        ax1.set_xlim(0,5e-4)
    fig1.show()
    fig1.savefig("./output/devsim/{}_reverse_electricfield.png".format(device+condition))
    fig1.clear()

def draw_electrons(device, positions, electrons, bias_voltages, condition):
    fig1=matplotlib.pyplot.figure()
    ax1 = fig1.add_subplot(111)
    for (x,n,V) in zip(positions, electrons, bias_voltages):
        matplotlib.pyplot.plot(x,n,label="%s"%(str(V)))
    matplotlib.pyplot.xlabel('Depth [cm]')
    matplotlib.pyplot.ylabel('Electron Density [cm^{-3}]')
    matplotlib.pyplot.ticklabel_format(axis="y", style="sci", scilimits=(0,0))
    ax1.legend(loc='upper right')
    if device == "SICAR-1.1.8":
        ax1.set_xlim(0,5e-4)
    fig1.show()
    fig1.savefig("./output/devsim/{}_reverse_electrons.png".format(device+condition))
    fig1.clear()

def draw_holes(device, positions, holes, bias_voltages, condition):
    fig1=matplotlib.pyplot.figure()
    ax1 = fig1.add_subplot(111)
    for (x,p,V) in zip(positions, holes, bias_voltages):
        matplotlib.pyplot.plot(x,p,label="%s"%(str(V)))
    matplotlib.pyplot.xlabel('Depth [cm]')
    matplotlib.pyplot.ylabel('Hole Density [cm^{-3}]')
    matplotlib.pyplot.ticklabel_format(axis="y", style="sci", scilimits=(0,0))
    ax1.legend(loc='upper right')
    if device == "SICAR-1.1.8":
        ax1.set_xlim(0,5e-4)
    fig1.show()
    fig1.savefig("./output/devsim/{}_reverse_holes.png".format(device+condition))
    fig1.clear()

def save_ele_field(device, positions,intensities, bias_voltages,condition):
    if not (os.path.exists("./output/devsim/{}/".format(device+condition))):
        os.makedirs("./output/devsim/{}/".format(device+condition))
    for (x,E,V) in zip(positions,intensities, bias_voltages):
        header_iv = ["Depth [cm]","E (V/cm)"]
        f=open("./output/devsim/{}/".format(device+condition)+str(V)+'V_x_E.csv','w')
        writer_E = csv.writer(f)
        writer_E.writerow(header_iv)
        for (per_x,per_E) in zip(x,E):
            writer_E.writerow([float(per_x),float(per_E)])

def draw1D(x,y,title,xtitle,ytitle,v):
    graph = ROOT.TGraph()
    for i in range(len(x)):
        graph.SetPoint(i, x[i],y[i])
    graph.SetTitle(title)
    canvas = ROOT.TCanvas("canvas", title, 1900, 600)
    graph.Draw("AL") 
    graph.GetXaxis().SetTitle(xtitle)
    graph.GetYaxis().SetTitle(ytitle)
    canvas.Draw()
    canvas.SaveAs("output/testdiode/"+title+"{}_1d.png".format(v))

def draw2D(x,y,value,title,v):
    graph = ROOT.TGraph2D()
    for i in range(len(x)):
        graph.SetPoint(i, y[i], x[i], value[i]) 
    canvas = ROOT.TCanvas("canvas", title, 1500, 1000)
    graph.Draw("CONT4Z")
    canvas.Draw()
    graph.GetXaxis().SetTitle("x[um]")
    graph.GetYaxis().SetTitle("z[um]")
    graph.SetTitle(title)
    canvas.SaveAs("output/strip/"+title+"{}_1e15_2d.png".format(v))
    canvas.SaveAs("output/strip/"+title+"{}_1e15_2d.root".format(v))

if __name__ == "__main__":
    main()