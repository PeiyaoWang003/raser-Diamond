#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import os
import sys
import time
import json
import subprocess
import re

def main():
    args = sys.argv[1:]
    python_file = re.match(r"./python/(.*)",args[0]).group(1)

    create_path("./devsim_output/jobs")
    jobfile_name = "./devsim_output/jobs/"+python_file+".job"
    gen_job(jobfile_name,run_code="raser ./python/"+python_file)
    submit_job(jobfile_name)

def create_path(path):
    """ If the path does not exit, create the path"""
    if not os.access(path, os.F_OK):
        os.makedirs(path, exist_ok=True) 

def runcmd(command):
    ret = subprocess.run([command],shell=True)

def gen_job(jobfile_name,run_code):
    jobfile = open(jobfile_name,"w")
    jobfile.write("source ./run raser \n")
    jobfile.write(run_code)
    jobfile.close()

    print("Generate job file: ", jobfile_name)

def submit_job(jobfile_name):
    print("Submit job file: ", jobfile_name)
    runcmd("chmod u+x {}".format(jobfile_name))
    runcmd("hep_sub -o ./devsim_output/jobs -e ./devsim_output/jobs {} -g physics".format(jobfile_name))


if __name__ == '__main__':
    main()