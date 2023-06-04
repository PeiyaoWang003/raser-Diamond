# -*- encoding: utf-8 -*-
import os
import csv
from scipy.interpolate import interp1d
import math


class DevsimCal:
    def __init__(self, filepath, my_d, dev_dic):
        self.elefield = []
        self.protential = []
        self.gradu = []
        self.lz = []
        self.l_z = my_d.l_z
        self.det_model = dev_dic['det_model']
        self.fl_x=my_d.l_x/dev_dic['xyscale']  
        self.fl_y=my_d.l_y/dev_dic['xyscale']
        self.readfile(filepath)
        self.tol_elenumber=dev_dic["tol_elenumber"]

    def readfile(self, filepath):
        i = 0
        with open(filepath, 'r') as f:
            for line in f.readlines():
                try:
                    fargs = list(map(float, 
                                     line.strip('\n').strip().split(',')))
                    self.lz.append(fargs[0]*1e4) #cm->um
                    self.elefield.append(fargs[1]/1e4) #V/cm -> V/um         
                except Exception as e:
                    pass
        for i in range(len(self.elefield)):
            self.gradu.append(sum(self.elefield[:i+1])*(self.lz[2]-self.lz[1]))

    def get_e_field(self, x, y, depth):
        f_ef = interp1d(self.lz, self.elefield, 
                        kind='linear', fill_value="extrapolate")
        #print(depth)        
        #print(f_ef(depth))
        return 0, 0, f_ef(depth) #x, y方向为0
    
    def get_w_p(self, x, y, depth, i):
        """
        threeD_out_column = self.threeD_out_column
        if threeD_out_column:   
            f_w_p = 1.0
        else:
            scale_px=x%self.fl_x
            scale_py=y%self.fl_y
            scale_pz=depth
            try:
                f_w_p = self.u_w(scale_px,scale_py,scale_pz)
            except RuntimeError:
                f_w_p = 0.0
        return f_w_p
        """
        f_p = 1 - (1/self.l_z) * depth
        return f_p
    
    def get_potential(self, x, y, depth):
        f_p = 1 - (1/self.l_z) * depth
        return f_p
    
    def getgradu(self, depth):
        f_u = interp1d(self.lz, self.gradu, kind = 'linear')
        return f_u(depth)

    def threeD_out_column(self,px,py,pz):
        """
        @description: 
           Judge whether (x,y,z) position is in sensor fenics range
        @reture:
            False: not
            True:  in
        @Modify:
            2021/08/31
        """
        if "plugin3D" in self.det_model:
            if (px < self.sx_l or px > self.sx_r
                or py < self.sy_l or py > self.sy_r):
                threeD_out_column=True
            else:
                threeD_out_column=False
        elif "planar3D" or "lgad3D" or "planarRing" in self.det_model:
            threeD_out_column=False
        return threeD_out_column
