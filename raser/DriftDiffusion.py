'''
Description:  DriftDiffusion.py
@Date       : 2022/10/25 16:40:46
@Author     : Tao Yang
@version    : 1.0
'''

import devsim
from raser.Node import *

#add defect parameters
N_c=3.25e15 #effective density of states in conduction band
N_v=4.8e15 #effective density of states in valence band
k=1.3806503e-23 
T0=300
#Z1/2
E_t11=-0.67*1.6e-19 #J
E_t12=-2.56*1.6e-19
n_11=N_c*math.exp(E_t11/(k*T0))
p_11=N_v*math.exp(E_t12/(k*T0))
devsim.set_parameter(device=device,region=region,name="N_t1",value=0)#density of Z1/2,4.1e13 from paper
devsim.set_parameter(device=device,region=region,name="r_n1",value=2e-7)#electron capture constant of Z1/2
devsim.set_parameter(device=device,region=region,name="r_p1",value=3e-7)#hole capture constant of Z1/2
devsim.set_parameter(device=device,region=region,name="E_t11",value=E_t11)#Z1/2 Et-Ec
devsim.set_parameter(device=device,region=region,name="E_t12",value=E_t12)#Z1/2 -(Et-Ev)
devsim.set_parameter(device=device,region=region,name="n_11",value=n_11)#n1 of Z1/2
devsim.set_parameter(device=device,region=region,name="p_11",value=p_11)#p1 of Z1/2
#EH6/7
E_t21=-1.65*1.6e-19 #J
E_t22=-1.58*1.6e-19
n_12=N_c*math.exp(E_t21/(k*T0))
p_12=N_v*math.exp(E_t22/(k*T0))
devsim.set_parameter(device=device,region=region,name="N_t2",value=0)#density of EH6/7,3.9e13 from paper
devsim.set_parameter(device=device,region=region,name="r_n2",value=2.4e-7)#electron capture constant of EH6/7
devsim.set_parameter(device=device,region=region,name="r_p2",value=5e-11)#hole capture constant of EH6/7
devsim.set_parameter(device=device,region=region,name="E_t21",value=E_t21)#EH6/7 Et-Ec
devsim.set_parameter(device=device,region=region,name="E_t22",value=E_t22)#EH6/7 -(Et-Ev)
devsim.set_parameter(device=device,region=region,name="n_12",value=n_12)#n1 of EH6/7
devsim.set_parameter(device=device,region=region,name="p_12",value=p_12)#p1 of EH6/7

def CreateBernoulli (device, region):
    '''
    Creates the Bernoulli function for Scharfetter Gummel
    '''
    #### test for requisite models here
    EnsureEdgeFromNodeModelExists(device, region, "Potential")
    vdiffstr="(Potential@n0 - Potential@n1)/V_T0"
    CreateEdgeModel(device, region, "vdiff", vdiffstr)
    CreateEdgeModel(device, region, "vdiff:Potential@n0",  "V_T0^(-1)")
    CreateEdgeModel(device, region, "vdiff:Potential@n1",  "-vdiff:Potential@n0")
    CreateEdgeModel(device, region, "Bern01",              "B(vdiff)")
    CreateEdgeModel(device, region, "Bern01:Potential@n0", "dBdx(vdiff) * vdiff:Potential@n0")
    CreateEdgeModel(device, region, "Bern01:Potential@n1", "-Bern01:Potential@n0")


def CreateElectronCurrent(device, region, mu_n):
    '''
    Electron current
    '''
    EnsureEdgeFromNodeModelExists(device, region, "Potential")
    EnsureEdgeFromNodeModelExists(device, region, "Electrons")
    EnsureEdgeFromNodeModelExists(device, region, "Holes")
    # Make sure the bernoulli functions exist
    if not InEdgeModelList(device, region, "Bern01"):
        CreateBernoulli(device, region)

    Jn = "q*{0}*EdgeInverseLength*V_T0*kahan3(Electrons@n1*Bern01,  Electrons@n1*vdiff,  -Electrons@n0*Bern01)".format(mu_n)
    #Jn = "q*ElectronMobility*EdgeInverseLength*V_T0*kahan3(Electrons@n1*Bern01,  Electrons@n1*vdiff,  -Electrons@n0*Bern01)"

    CreateEdgeModel(device, region, "ElectronCurrent", Jn)
    for i in ("Electrons", "Potential", "Holes"):
        CreateEdgeModelDerivatives(device, region, "ElectronCurrent", Jn, i)


def CreateHoleCurrent(device, region, mu_p):
    '''
    Hole current
    '''
    EnsureEdgeFromNodeModelExists(device, region, "Potential")
    EnsureEdgeFromNodeModelExists(device, region, "Holes")
    # Make sure the bernoulli functions exist
    if not InEdgeModelList(device, region, "Bern01"):
        CreateBernoulli(device, region)
    
    #define electrons accumulated in the traps
    #parameter of first trap Z1/2
    Dn_t1="N_t1*r_n1*(r_n1*n_11+r_p1*Acceptors@n1)*Electrons@n1/(r_n1*(Donors@n1+n_11)+r_p1*(Acceptors@n1+p_11))^2"
    #parameter of second trap EH6/7
    Dn_t2="N_t2*r_n2*(r_n2*n_12+r_p2*Acceptors@n1)*Electrons@n1/(r_n2*(Donors@n1+n_12)+r_p2*(Acceptors@n1+p_12))^2"
    CreateEdgeModel(device,region,"Dn_t1",Dn_t1)
    CreateEdgeModel(device,region,"Dn_t2",Dn_t2)
    
    Jp ="-q*mu_p*ElectricField*(Dn_t1+Dn_t2)-q*{0}*EdgeInverseLength*V_T0*kahan3(Holes@n1*Bern01, -Holes@n0*Bern01, -Holes@n0*vdiff)".format(mu_p)
    #Jp ="-q*HoleMobility*EdgeInverseLength*V_T0*kahan3(Holes@n1*Bern01, -Holes@n0*Bern01, -Holes@n0*vdiff)"

    CreateEdgeModel(device, region, "HoleCurrent", Jp)
    for i in ("Holes", "Potential", "Electrons"):
        CreateEdgeModelDerivatives(device, region, "HoleCurrent", Jp, i)