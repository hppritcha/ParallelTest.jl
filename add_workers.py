#!/usr/bin/env python

# Lets add workers programatically, and see if they distribute to different cores.

import multiprocessing as mp
import numpy as np
import subprocess

import argparse
parser = argparse.ArgumentParser(prog="add_workers.py", description="Test workers.")
parser.add_argument("-p", "--p", help="Number of workers to add.", type=int)
args = parser.parse_args()

p = args.p

def print_cpus():
    subprocess.call("ps -eo pid,psr,pcpu,cmd | grep python", shell=True)

print("Before map")
print_cpus()


def pcpus(mat):
    print("During map")
    print_cpus()
    return mat**2

pool = mp.Pool(args.p)

M = [np.random.rand(10000,1000) for i in range(p)]

pool.map(pcpus, M)

print("After map.")
print_cpus()
