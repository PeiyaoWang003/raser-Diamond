#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@Description: Signal re-formation for events of great amount
@Date       : 2025/04/09 15:24:27
@Author     : Chenxi Fu
@version    : 1.0
'''
import os
from array import array

import ROOT

from device.build_device import Detector
from current.cross_talk import cross_talk
from afe.readout import Amplifier

def main(amp_name, det_name, file, tct=None):    
    my_d = Detector(det_name)
    file_pointer = ROOT.TFile(file, "READ")
    tree = file_pointer.Get("tree")
    n = tree.GetEntries()
    waveforms = [[] for _ in range(n)]
    tree.GetEntry(0)
    time = tree.time
    for i in range(n):
        tree.GetEntry(i)
        for j in range(my_d.read_ele_num):
            cu = eval(f"tree.data_cu_{j}")
            waveforms[i].append(ROOT.TH1F("original current entry {n} electrode {e}".format(n=i, e=str(j+1)), "original current",
                                len(time),0,time[-1]))
            waveforms[i][j].SetDirectory(0)
            for k in range(1, len(time)-1):
                waveforms[i][j].SetBinContent(k, cu[k-1])

    # if you define TH1F during TFile opened, after TFile closed TH1F will become None
    # SetDirectory(0) is needed to prevent this

    print("read {n} events from {file}".format(n=n,file=file))
    file_pointer.Close()

    length = 1000 # time length of the signal
    time = array('d', [0. for _ in range(length)])
    amp_length = 20000 # time length of amplified signal
    time_amp = array('d', [0. for _ in range(amp_length)])

    if "strip" in my_d.det_model:
        # record signal only
        tree_ct = ROOT.TTree("tree", "Waveform Data")
        tree_ct.Branch("time", time, "time[{length}]/D".format(length=length))
        data_ct = []
        for i in range(my_d.read_ele_num):
            data_ct.append(array('d', [0. for _ in range(length)]))
            tree_ct.Branch("data_ct_{i}".format(i=i), data_ct[i], "data_ct_{i}[{length}]/D".format(i=i,length=length))
        
    tree_amp = ROOT.TTree("tree", "Waveform Data")
    tree_amp.Branch("time", time_amp, "time[{length}]/D".format(length=amp_length))
    data_amp = []
    for i in range(my_d.read_ele_num):
        data_amp.append(array('d', [0. for _ in range(amp_length)]))
        tree_amp.Branch("data_amp_{i}".format(i=i), data_amp[i], "data_amp_{i}[{length}]/D".format(i=i,length=amp_length))

    if "strip" in my_d.det_model:
        for i in range(n):
            cross_talk_cu = cross_talk(waveforms[i])
            for j in range(cross_talk_cu[0].GetNbinsX()):
                time[j] = j*cross_talk_cu[0].GetBinWidth(j)
            for i in range(len(cross_talk_cu)):
                for j in range(cross_talk_cu[i].GetNbinsX()):
                    data_ct[i][j] = cross_talk_cu[i].GetBinContent(j)
            tree_ct.Fill()

            amplified_cu = Amplifier(cross_talk_cu, amp_name, seed=i).amplified_currents
            for j in range(amplified_cu[0].GetNbinsX()):
                time_amp[j] = j*amplified_cu[0].GetBinWidth(j)
            for i in range(len(amplified_cu)):
                for j in range(amplified_cu[i].GetNbinsX()):
                    data_amp[i][j] = amplified_cu[i].GetBinContent(j)
            tree_amp.Fill()

        cross_talk_file_name = file.replace("signal_cu", "signal_ct")
        cross_talk_file = ROOT.TFile(cross_talk_file_name, "RECREATE")
        tree_ct.Write()
        cross_talk_file.Close()

        amplified_file_name = file.replace("signal_cu", "signal_amp")
        amplified_file = ROOT.TFile(amplified_file_name, "RECREATE")
        tree_amp.Write()
        amplified_file.Close()

    else:
        for i in range(n):
            amplified_cu = Amplifier(waveforms[i], amp_name, seed=i).amplified_currents
            for j in range(amplified_cu[0].GetNbinsX()):
                time_amp[j] = j*amplified_cu[0].GetBinWidth(j)
            for i in range(len(amplified_cu)):
                for j in range(amplified_cu[i].GetNbinsX()):
                    data_amp[i][j] = amplified_cu[i].GetBinContent(j)
            tree_amp.Fill()

        amplified_file_name = file.replace("signal_cu", "signal_amp")
        amplified_file = ROOT.TFile(amplified_file_name, "RECREATE")
        tree_amp.Write()
        amplified_file.Close()

