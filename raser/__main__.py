#!/usr/bin/env python3
# Main driver to run raser    
# Author FU Chenxi <1256257282@qq.com>, SHI Xin <shixin@ihep.ac.cn>
# Created [2023-08-29 Tue 11:48] 

import sys 
import argparse
import importlib

VERSION = 4.1

parser = argparse.ArgumentParser(prog='raser')
parser.add_argument('--version', action='version', 
                    version='%(prog)s {}'.format(VERSION))
parser.add_argument('-b', '--batch', help='submit BATCH job to cluster', action='count', default=0)
parser.add_argument('-t', '--test', help='TEST', action="store_true")

subparsers = parser.add_subparsers(help='sub-command help', dest="subparser_name")

parser_asic = subparsers.add_parser('asic', help='ASIC design')
parser_asic.add_argument('label', help='LABEL to identify ASIC design')

parser_bmos = subparsers.add_parser('bmos', help='Beam Monitor Online System')
parser_bmos.add_argument('label', help='LABEL to identify BMOS simulations')
parser_bmos.add_argument('-v', '--verbose', help='VERBOSE level', 
                          action='count', default=0)

parser_cce = subparsers.add_parser('cce', help='Charge Collection Efficiency')
parser_cce.add_argument('label', help='LABEL to identify CCE experiment')

parser_cflm = subparsers.add_parser('cflm', help='CEPC Fast Luminosity Measurement')
parser_cflm.add_argument('label', help='LABEL to identify CFLM simulations')
parser_cflm.add_argument('-v', '--verbose', help='VERBOSE level', 
                          action='count', default=0)

parser_draw = subparsers.add_parser('current', help='calculate drift current')
parser_draw.add_argument('label', help='LABEL to identify root files')

parser_elec = subparsers.add_parser('elec', help='electronic readout')
parser_elec.add_argument('label', help='LABEL to identify electronics operations')
parser_elec.add_argument('name', help='LABEL to identify electronics files')
parser_elec.add_argument('-tct', help='signal from TCT')

parser_field = subparsers.add_parser('field', help='calculate field/weight field and iv/cv')
parser_field.add_argument('label', help='LABEL to identify operation')
parser_field.add_argument('-v', '--verbose', help='VERBOSE level', 
                          action='count', default=0)
parser_field.add_argument('-cv', help='CV simulation', action="store_true")
parser_field.add_argument("-wf", help="WeightField Simulation", action="store_true")
parser_field.add_argument("-v_current", help="Current voltage for step-by-step simulation", type=float)
parser_field.add_argument("-noise", help="Detector Noise simulation", action="store_true")
parser_field.add_argument('-umf', help='use umf solver', action="store_true")

parser_fpga = subparsers.add_parser('fpga', help='FPGA design')
parser_fpga.add_argument('label', help='LABEL to identify FPGA design')

parser_gen_signal = subparsers.add_parser('gen_signal', help='generate signal')
parser_gen_signal.add_argument('det_name', help='name of the detector')
parser_gen_signal.add_argument('-l','--label', help='LABEL to identify signal generation method', default='signal')
parser_gen_signal.add_argument('-vol', '--voltage', type=str, help='bias voltage')
parser_gen_signal.add_argument('-abs', '--absorber', type=str, help='model of particle energy absorber')
parser_gen_signal.add_argument('-amp', '--amplifier', type=str, help='amplifier')
parser_gen_signal.add_argument('-s', '--scan', type=int, help='instance number for scan mode')
parser_gen_signal.add_argument('--job', type=int, help='flag of run in job')

parser_telescope = subparsers.add_parser('resolution', help='resolution calculation for time, space and energy')
parser_telescope.add_argument('det_name', help='name of the detector')
parser_telescope.add_argument('-tct', type=str, help='specify TCT signal class')

parser_telescope = subparsers.add_parser('telescope', help='telescope')
parser_telescope.add_argument('label', help='LABEL to identify telescope files')

parser_tct = subparsers.add_parser('tct', help='TCT simulation')
parser_tct.add_argument('label', help='LABEL to identify TCT options')
parser_tct.add_argument('det_name', help='name of the detector')
parser_tct.add_argument('laser', help='name of the laser')
parser_tct.add_argument('-vol', '--voltage', type=str, help='bias voltage')
parser_tct.add_argument('-amp', '--amplifier', type=str, help='amplifier')
parser_tct.add_argument('-s', '--scan', type=int, help='instance number for scan mode')
parser_tct.add_argument('--job', type=int, help='flag of run in job')


args = parser.parse_args()

if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(1)

kwargs = vars(args)

submodule = kwargs['subparser_name']

if kwargs['batch'] != 0:
    batch_level = kwargs['batch']
    import re
    from util import batchjob
    destination = submodule
    command = ' '.join(sys.argv[1:])
    command = command.replace('--batch ', '')
    for bs in re.findall('-b* ', command):
        command = command.replace(bs, '')
    is_test = vars(args)['test'] 
    batchjob.main(destination, command, batch_level, is_test)
else:
    submodule = importlib.import_module(submodule)
    submodule.main(kwargs)
    