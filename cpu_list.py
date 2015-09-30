#!/usr/bin/env python

import re

import subprocess

text = subprocess.check_output(["scontrol -dd show job $SLURM_JOB_ID"], universal_newlines=True, shell=True)

# This command is run
# scontrol -dd show job $SLURM_CPU_BIND

# This is the output
# text = '''JobId=48834041 JobName=bash
#    UserId=iczekala(50009) GroupId=oberg_lab(403153)
#    Priority=119953191 Nice=0 Account=oberg_lab QOS=normal
#    JobState=RUNNING Reason=None Dependency=(null)
#    Requeue=1 Restarts=0 BatchFlag=0 Reboot=0 ExitCode=0:0
#    DerivedExitCode=0:0
#    RunTime=00:03:35 TimeLimit=01:00:00 TimeMin=N/A
#    SubmitTime=2015-09-30T11:22:22 EligibleTime=2015-09-30T11:22:22
#    StartTime=2015-09-30T11:22:22 EndTime=2015-09-30T12:22:22
#    PreemptTime=None SuspendTime=None SecsPreSuspend=0
#    Partition=interact AllocNode:Sid=rclogin07:29288
#    ReqNodeList=(null) ExcNodeList=(null)
#    NodeList=holy2a18308
#    BatchHost=holy2a18308
#    NumNodes=1 NumCPUs=1 CPUs/Task=1 ReqB:S:C:T=0:0:*:*
#    Socks/Node=* NtasksPerN:B:S:C=0:0:*:* CoreSpec=*
#      Nodes=holy2a18308 CPU_IDs=17 Mem=500
#    MinCPUsNode=1 MinMemoryNode=500M MinTmpDiskNode=0
#    Features=(null) Gres=(null) Reservation=(null)
#    Shared=OK Contiguous=0 Licenses=(null) Network=(null)
#    Command=/bin/bash
#    WorkDir=/n/home07/iczekala
# '''

# text = '''JobId=48725299
# JobName=2092_pbe_6-31gs_opt_qchem_flow_batt-CMEAGUKNRRSGPV-MHTXFSSINA-M_conformer_9
#     UserId=rgbombarelli(555495) GroupId=aspuru-guzik_lab(33108)
#     Priority=10000000 Nice=0 Account=aspuru-guzik_lab QOS=normal
#     JobState=RUNNING Reason=None Dependency=(null)
#     Requeue=0 Restarts=0 BatchFlag=1 Reboot=0 ExitCode=0:0
#     DerivedExitCode=0:0
#     RunTime=09:45:15 TimeLimit=3-03:00:00 TimeMin=N/A
#     SubmitTime=2015-09-29T00:26:46 EligibleTime=2015-09-29T00:26:46
#     StartTime=2015-09-29T00:28:39 EndTime=2015-10-02T03:28:43
#     PreemptTime=None SuspendTime=None SecsPreSuspend=0
#     Partition=eldorado AllocNode:Sid=rclogin05:2899
#     ReqNodeList=(null) ExcNodeList=(null)
#     NodeList=eldorado23
#     BatchHost=eldorado23
#     NumNodes=1 NumCPUs=8 CPUs/Task=1 ReqB:S:C:T=0:0:*:*
#     Socks/Node=* NtasksPerN:B:S:C=0:0:*:* CoreSpec=*
#       Nodes=eldorado23 CPU_IDs=0-3,6-9 Mem=16000
#     MinCPUsNode=1 MinMemoryCPU=2000M MinTmpDiskNode=0
#     Features=(null) Gres=(null) Reservation=(null)
#     Shared=OK Contiguous=0 Licenses=(null) Network=(null)
# Command=/n/home05/rgbombarelli/quinone_jobs/pending/2092_pbe_6-31gs_opt_qchem_flow_batt-CMEAGUKNRRSGPV-MHTXFSSINA-M_conformer_9/job.sh
# WorkDir=/n/home05/rgbombarelli/quinone_jobs/pending/2092_pbe_6-31gs_opt_qchem_flow_batt-CMEAGUKNRRSGPV-MHTXFSSINA-M_conformer_9
# StdErr=/n/home05/rgbombarelli/quinone_jobs/pending/2092_pbe_6-31gs_opt_qchem_flow_batt-CMEAGUKNRRSGPV-MHTXFSSINA-M_conformer_9/slurm-48725299.out
#     StdIn=/dev/null
# StdOut=/n/home05/rgbombarelli/quinone_jobs/pending/2092_pbe_6-31gs_opt_qchem_flow_batt-CMEAGUKNRRSGPV-MHTXFSSINA-M_conformer_9/slurm-48725299.out
#     BatchScript='''


# Now scrape the value of CPU_IDs using a regex
# Indexed from 0

# First, just find CPU id.
p = re.compile(r"CPU_IDs=(\S+)")

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

# 1. Separate ranges based upon comma (there may not be a comma)
for group in CPU_IDs.split(","):
    hyphens = group.split("-")
    # 1.1 If it includes a hyphen, expand into a range
    if len(hyphens) > 1:
        low, high = hyphens
        low = int(low)
        high = int(high)
        cpus += list(range(low, high+1))
    # If it doesn't include a hyphen just append it
    else:
        cpus.append(int(group))

# Concatenate all together and literally print a list of the IDs
cpu_strs = ["{}".format(cpu) for cpu in cpus]
cpulist = ",".join(cpu_strs)

# Truncate the last comma, if we had more than one cpu
if len(cpus) > 1:
    cpulist = cpulist[:-1]

print(cpulist)
