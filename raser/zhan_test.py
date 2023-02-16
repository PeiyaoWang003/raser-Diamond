#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
import geant4_pybind as g4b
import sys
import numpy as np
import raser


class MyDetectorConstruction(g4b.G4VUserDetectorConstruction):
    def __init__(self,my_d,my_f,sensor_model,maxStep=0.5):
        g4b.G4VUserDetectorConstruction.__init__(self)
        self.solid = {}
        self.logical = {}
        self.physical = {}
        self.checkOverlaps = True
        self.create_world(my_d)
        #3D source order: beta->sic->si
        #2D source order: beta->Si->SiC
        tx_all = my_d.l_x/2.0*g4b.um
        ty_all = my_d.l_y/2.0*g4b.um


    def create_world(self,my_d):

        self.nist = g4b.G4NistManager.Instance()
        material = self.nist.FindOrBuildMaterial("G4_AIR")  
        self.solid['world'] = g4b.G4Box("world",
                                        25000*g4b.um,
                                        25000*g4b.um,
                                        25000*g4b.um)
        self.logical['world'] = g4b.G4LogicalVolume(self.solid['world'], 
                                                    material, 
                                                    "world")
        self.physical['world'] = g4b.G4PVPlacement(None, 
                                                   g4b.G4ThreeVector(0,0,0), 
                                                   self.logical['world'], 
                                                   "world", None, False, 
                                                   0,self.checkOverlaps)
        visual = g4b.G4VisAttributes()
        visual.SetVisibility(False)
        self.logical['world'].SetVisAttributes(visual)


    def create_si_box(self, **kwargs):
        name = 'Si_chip'
        material_si = self.nist.FindOrBuildElement(kwargs['material_Si'],False)
        si_density = 2.32*g4b.g/g4b.cm3
        #a=28.0855*g4b.g/g4b.mole
        #Si = g4b.G4Material("Si",z=14., a, si_density) 
        Si = g4b.G4Material("Si",si_density,1)
        SiC.AddElement(material_si,100*g4b.perCent)
        
        translation = g4b.G4ThreeVector(0,0,0)
        visual = g4b.G4VisAttributes(g4b.G4Color([1,0,0]))

        sidex = 10000*g4b.um
        sidey = 10000*g4b.um
        sidez = 300*g4b.um

        self.solid[name] = g4b.G4Box(name, sidex/2., sidey/2., sidez/2.)
        
        self.logical[name] = g4b.G4LogicalVolume(self.solid[name], 
                                                 Si, 
                                                 name)
        self.physical[name] = g4b.G4PVPlacement(None,translation,                                                
                                                name,self.logical[name],
                                                mother, False, 
                                                0,self.checkOverlaps)
        self.logical[name].SetVisAttributes(visual)
        print("Si_Box")


class MyPrimaryGeneratorAction(g4b.G4VUserPrimaryGeneratorAction):
    def __init__(self,par_in,par_out):
        g4b.G4VUserPrimaryGeneratorAction.__init__(self)
        par_direction = [ par_out[i] - par_in[i] for i in range(3) ]  
        particle_table = g4b.G4ParticleTable.GetParticleTable()
        electron = particle_table.FindParticle("e-") # define the beta electron
        beam = g4b.G4ParticleGun(1)
        beam.SetParticleEnergy(2.28*g4b.MeV)
        # beam.SetParticleEnergy(0.546*g4b.MeV)
        beam.SetParticleMomentumDirection(g4b.G4ThreeVector(par_direction[0],
                                                            par_direction[1],
                                                            par_direction[2]))
        beam.SetParticleDefinition(electron)
        beam.SetParticlePosition(g4b.G4ThreeVector(par_in[0]*g4b.um,
                                                   par_in[1]*g4b.um,
                                                   par_in[2]*g4b.um))  

        beam2 = g4b.G4ParticleGun(1)
        beam2.SetParticleEnergy(0.546*g4b.MeV)
        beam2.SetParticleMomentumDirection(g4b.G4ThreeVector(par_direction[0],
                                                             par_direction[1],
                                                             par_direction[2]))
        beam2.SetParticleDefinition(electron)
        beam2.SetParticlePosition(g4b.G4ThreeVector(par_in[0]*g4b.um,
                                                    par_in[1]*g4b.um,
                                                    par_in[2]*g4b.um))  
        self.particleGun = beam
        self.particleGun2 = beam2

    def GeneratePrimaries(self, event):
        self.particleGun.GeneratePrimaryVertex(event)
        self.particleGun2.GeneratePrimaryVertex(event)

class MyRunAction(g4b.G4UserRunAction):
    def __init__(self):
        g4b.G4UserRunAction.__init__(self)
        milligray = 1.e-3*g4b.gray
        microgray = 1.e-6*g4b.gray
        nanogray = 1.e-9*g4b.gray
        picogray = 1.e-12*g4b.gray

        g4b.G4UnitDefinition("milligray", "milliGy", "Dose", milligray)
        g4b.G4UnitDefinition("microgray", "microGy", "Dose", microgray)
        g4b.G4UnitDefinition("nanogray", "nanoGy", "Dose", nanogray)
        g4b.G4UnitDefinition("picogray", "picoGy", "Dose", picogray)
      
    def BeginOfRunAction(self, run):
        g4b.G4RunManager.GetRunManager().SetRandomNumberStore(False)
   
    def EndOfRunAction(self, run):
        nofEvents = run.GetNumberOfEvent()
        if nofEvents == 0:
            print("nofEvents=0")
            return

class MyEventAction(g4b.G4UserEventAction):
    "My Event Action"
    def __init__(self, runAction, point_in, point_out):
        g4b.G4UserEventAction.__init__(self)
        self.fRunAction = runAction
        self.point_in = point_in
        self.point_out = point_out

    def BeginOfEventAction(self, event):
        self.edep_device=0.
        self.event_angle = 0.
        self.p_step = []
        self.energy_step = []
        

    def EndOfEventAction(self, event):
        eventID = event.GetEventID()
        #print("eventID:%s"%eventID)
        if len(self.p_step):
            point_a = [ b-a for a,b in zip(self.point_in,self.point_out)]
            point_b = [ c-a for a,c in zip(self.point_in,self.p_step[-1])]
            self.event_angle = cal_angle(point_a,point_b)
        else:
            self.event_angle = None
        save_geant4_events(eventID,self.edep_device,
                           self.p_step,self.energy_step,self.event_angle)

    def RecordDevice(self, edep,point_in,point_out):
        self.edep_device += edep
        self.p_step.append([point_in.getX()*1000,
                           point_in.getY()*1000,point_in.getZ()*1000])
        self.energy_step.append(edep)
 





class MySteppingAction(g4b.G4UserSteppingAction):
    "My Stepping Action"
    def __init__(self, eventAction):
        g4b.G4UserSteppingAction.__init__(self)
        self.fEventAction = eventAction

    def UserSteppingAction(self, step):
        edep = step.GetTotalEnergyDeposit()
        point_pre  = step.GetPreStepPoint()
        point_post = step.GetPostStepPoint() 
        point_in   = point_pre.GetPosition()
        point_out  = point_post.GetPosition()
        volume = step.GetPreStepPoint().GetTouchable().GetVolume().GetLogicalVolume()
        volume_name = volume.GetName()
        if(volume_name == "Device"):
            self.fEventAction.RecordDevice(edep,point_in,point_out)


class MyActionInitialization(g4b.G4VUserActionInitialization):
    def __init__(self,par_in,par_out):
        g4b.G4VUserActionInitialization.__init__(self)
        self.par_in = par_in
        self.par_out = par_out

    def Build(self):
        self.SetUserAction(MyPrimaryGeneratorAction(self.par_in,
                                                    self.par_out))
        # global myRA_action
        myRA_action = MyRunAction()
        self.SetUserAction(myRA_action)
        myEA = MyEventAction(myRA_action,self.par_in,self.par_out)
        self.SetUserAction(myEA)
        self.SetUserAction(MySteppingAction(myEA))

