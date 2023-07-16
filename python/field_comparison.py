#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@Description: compare the difference of the electric field of p-i-n and LGAD
@Date       : 2023/02/14 17:00:00
@Author     : Chenxi Fu
@version    : 1.0

Usage : 
source ./run raser
raser 'python/field_comparison.py'
'''

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import raser
import drawsave
import time
import ROOT

pin_paras = ["det_name=HPK-Si-PIN","parfile=paras/setting.json"]
pin_set = raser.Setting(pin_paras)
my_pin = raser.R3dDetector(pin_set)
my_pin_field = raser.FenicsCal(my_pin,pin_set.fenics)
pin_field_histo=drawsave.fill_his_1D('E',my_pin,my_pin_field)

lgad_paras = ["det_name=HPK-Si-LGAD","parfile=paras/setting.json"]
lgad_set = raser.Setting(lgad_paras)
my_lgad = raser.R3dDetector(lgad_set)
my_lgad_field = raser.FenicsCal(my_lgad,lgad_set.fenics)
lgad_field_histo=drawsave.fill_his_1D('E',my_lgad,my_lgad_field)

now = time.strftime("%Y_%m%d_%H%M")
path = "fig/" + now + "/"
drawsave.create_path(path) 

c1 = ROOT.TCanvas("c", "canvas",1200, 1000)
ROOT.gStyle.SetOptStat(ROOT.kFALSE)
ROOT.gStyle.SetOptFit()
c1.SetLeftMargin(0.18)
c1.SetBottomMargin(0.14)

lgad_field_histo.SetTitle("")
lgad_field_histo.SetLineColor(6)
lgad_field_histo.SetMarkerColor(6)
lgad_field_histo.SetMarkerStyle(20)
lgad_field_histo.Draw("HIST")
lgad_field_histo.Draw("SAME P")
pin_field_histo.SetLineColor(4)
pin_field_histo.SetMarkerColor(4)
pin_field_histo.SetMarkerStyle(22)
pin_field_histo.Draw("SAME HIST")
pin_field_histo.Draw("SAME P")

lgad_field_histo.GetXaxis().SetTitleSize(0.05)
lgad_field_histo.GetXaxis().SetLabelSize(0.05)
lgad_field_histo.GetYaxis().SetTitleSize(0.05)
lgad_field_histo.GetYaxis().SetLabelSize(0.05)

legend = ROOT.TLegend(0.5, 0.6, 0.8, 0.8)
legend.AddEntry(pin_field_histo, "p-i-n", "pl")
legend.AddEntry(lgad_field_histo, "LGAD", "pl")
legend.SetTextSize(0.05)
legend.SetBorderSize(0)
legend.Draw("same")

c1.SaveAs(path+"field_comparison"+".pdf")
c1.SaveAs(path+"field_comparison"+".root")