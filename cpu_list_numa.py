#!/usr/bin/env python

import argparse

parser = argparse.ArgumentParser(description="Print out the CPUS that our SLURM job has been given.")
parser.add_argument("--which", choices=["all", "first", "rest"], default="all", help="Which CPS to print out.")
args = parser.parse_args()


import re

import subprocess

text = subprocess.check_output(["numactl --show"], universal_newlines=True, shell=True)

# text = '''
# policy: default
# preferred node: current
# physcpubind: 10 36 43 59
# cpubind: 1 2 3 7
# nodebind: 1 2 3 7
# membind: 0 1 2 3 4 5 6 7
# '''

# Now scrape the value of CPU_IDs using a regex
# Indexed from 0

# First, just find CPU id.
p = re.compile(r"physcpubind: ([\d\s]*)")

m = p.search(text)

if m:
    CPU_IDs = m.group(1)
    # print("Found CPU_IDs ", CPU_IDs)
else:
    # print("No match to CPU_IDs, exiting.")
    import sys
    sys.exit()

# Now parse the various possible CPU lists

cpus = []

# 1. Separate ranges based upon whitespace
for group in CPU_IDs.split(" "):
    group = group.strip()
    if group.isdigit():
        cpus.append(int(group))

# Concatenate all together and literally print a list of the IDs
cpu_strs = ["{}".format(cpu) for cpu in cpus]

if args.which == "first":
    # Print only the cpu integer
    print(cpus[0])
elif args.which == "rest":
    # Print the rest of the values like [1,2,3] NOT [1, 3, 4]
    cpulist = ",".join(cpu_strs[1:])
    print("[{}]".format(cpulist))

elif args.which == "all":
    # Print the values however you want
    print(cpus)
