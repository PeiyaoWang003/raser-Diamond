#Xray_energy_resolution
#!/usr/bin/env python3
# -*- encoding: utf-8 -*-


import sys
import os
from array import array
import time
import subprocess
import json
import random
from scipy.stats import norm
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

import ROOT
ROOT.gROOT.SetBatch(True)
from ..device import build_device as bdv
from ..util.output import output

def read_events(event_folder_path, electrode_index=0):
    #read file
    waveforms = None
    for file in os.listdir(event_folder_path):

        file_path = os.path.join(event_folder_path, file)
        f = ROOT.TFile(file_path)
        tree = f.Get("tree")
        branches = tree.GetListOfBranches()
        branch_name = f"amplified_waveform_{electrode_index}"
        print(file_path)
        for event in range(tree.GetEntries()):
            tree.GetEntry(event)
            hist = getattr(tree, branch_name)
            n_bins = hist.GetNbinsX()
            waveform = np.zeros(n_bins)
            for j in range(n_bins):
                waveform[j] = hist.GetBinContent(j + 1)
            if waveforms is None:
                waveforms = waveform
            else:
                waveforms = np.vstack((waveforms, waveform))
        f.Close()
    print(waveforms)

    return waveforms



def Energy_resolution(waveforms, my_d):
    peaks = []
    for i in range(waveforms.shape[0]):
        peak_i = max(waveforms[i,:])
        peaks.append(peak_i)
        peaks.sort()
    print(peaks)
    peaks_len = len(peaks)
    extreme_num = int(peaks_len * 0.05)
    peaks = peaks[extreme_num:peaks_len-extreme_num]
    sep=50
    mu, sigma = norm.fit(peaks)
    fwhm= 2 * np.sqrt(2 * np.log(2)) * sigma
    if hasattr(my_d, 'sweep') ==False or my_d.sweep == None:
        print("draw fit curve for single energy test...")
        now = time.strftime("%Y_%m%d_%H%M%S")
        path = output(__file__, my_d.det_name, now)
        #画拟合图，暂时未写入命令行参数，后续再完善
        draw_fit_curve(peaks,mu,sigma,path,sep,my_d.det_name)
    energy_resolution = fwhm / mu
    print(f"Energy resolution: {energy_resolution:.2%}")
    return energy_resolution


    # Draw Gaussian distribution fit curve
def draw_fit_curve(peaks, mu, sigma, path, bins, det_model):
    fig, ax1 = plt.subplots(figsize=(8, 5))

    # 左轴：频数直方图
    ax1.hist(peaks, bins=bins, density=False, alpha=0.6, color='steelblue',
             edgecolor='black', linewidth=0.5, label='peaks')
    ax1.set_xlabel('current')
    ax1.set_ylabel('Frequency', color='steelblue')
    ax1.tick_params(axis='y', labelcolor='steelblue')
    ax1.grid(alpha=0.3)

    # 右轴：概率密度曲线
    ax2 = ax1.twinx()
    x = np.linspace(min(peaks), max(peaks), 200)
    pdf = stats.norm.pdf(x, mu, sigma)
    ax2.plot(x, pdf, 'r-', lw=2.5, label=f'fit_curve $N({mu:.2f}, {sigma:.2f}^2)$')
    ax2.set_ylabel('Probability density', color='red')
    ax2.tick_params(axis='y', labelcolor='red')

    # 合并图例
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='best')

    ax1.set_title('fit curve')
    fig.savefig(os.path.join(path, f"{det_model}_fit_curve.pdf"))
    print(f"Fit curve saved to {os.path.join(path, f'{det_model}_fit_curve.pdf')}")
    plt.close(fig)


def main(kwargs):
    #设置部分
    det_name = kwargs['det_name']
    my_d = bdv.Detector(det_name)
    
    my_d = bdv.Detector(det_name)
    if kwargs['voltage'] != None:
        my_d.voltage = kwargs['voltage']

    if kwargs['irradiation'] != None:
        my_d.irradiation_flux = float(kwargs['irradiation'])

    if kwargs['g4experiment'] != None:
        my_d.g4experiment = kwargs['g4experiment']

    if kwargs['amplifier'] != None:
        my_d.amplifier = kwargs['amplifier']

    if 'subfile_path' in kwargs:
        if kwargs['subfile_path'] != None:
            my_d.subfile_path = kwargs['subfile_path']

    if 'sweep' in kwargs:
        if kwargs['sweep'] != None:
            my_d.sweep = kwargs['sweep']


    
    #events_path = "/afs/ihep.ac.cn/users/s/shaochangpu/raser/output/sweep/NJU-PiN/par_energy_2026-03-28-19-02-50/par_energy_4sweep0-500.0time_resolutionucsc.root"
    event_folder_path = "/afs/ihep.ac.cn/users/w/wangpeiyao/raser/output/signal/MIM-Diamond/batch"
    # if hasattr(my_d, 'subfile_path') and my_d.subfile_path != None:
    #     events_path = my_d.subfile_path
    # print(events_path)
    # if not os.path.exists(events_path):
    #     print(f"Error: {events_path} does not exist.")
    #     return
    if hasattr(my_d, 'sweep') and my_d.sweep != None:
        print("sweep mode, skip energy resolution calculation.")
        amplified_waveforms = read_events(events_path)
        energy_resolution = energy_resolution(amplified_waveforms, my_d)
        return energy_resolution

    else:
        print("single energy test mode, calculate energy resolution...")
            #单能量测试 
        amplified_waveforms = read_events(event_folder_path)
        energy_resolution = Energy_resolution(amplified_waveforms, my_d)

