#!/bin/bash

#SBATCH -J Test #Single job name for the entire JobArray

#SBATCH -o slurm.out #standard output

#SBATCH -e slurm.err #standard error

#SBATCH -p general #partition

#SBATCH -t 00:3:00 #running time

#SBATCH --mail-type=BEGIN

#SBATCH --mail-type=END

#SBATCH --mail-user=iancze@gmail.com

#SBATCH --mem 2000 #memory request per node

#SBATCH -N 1 #ensure all jobs are on the same node

#SBATCH -n 4

#SBATCH -B 1:4:1

#SBATCH --ntasks-per-core 1

#SBATCH --verbose


## Call cpu_list to get the currently running CPUS

# Let's read out the SLURM environment variables
echo "SLURM_CPU_BIND $SLURM_CPU_BIND"
echo "SLURM JOB_NODELIST $SLURM_JOB_NODELIST"
echo "SLURM_TASKS_PER_NODE $SLURM_TASKS_PER_NODE"

echo "SLURM_NTASKS_PER_CODE $SLURM_NTASKS_PER_CORE"
echo "SLURM_NTASKS_PER_SOCKET $SLURM_NTASKS_PER_SOCKET"


# hostlist=$(scontrol show hostname $SLURM_JOB_NODELIST)
# rm -f hosts
#
# for f in $hostlist
#   do
#   echo $f':64' >> hosts
# done

echo "numactl says"
numactl --show

CPUMASTER=$(./cpu_list_numa.py --which first)

CPULIST=$(./cpu_list_numa.py --which rest)

echo "Master CPU is $CPUMASTER"
echo "Worker CPUs are $CPULIST"

#Constrain the brain process to start on CPUMASTER, then add the workers in using AffinityManager.
# taskset -c $CPUMASTER ./add_workers_manager.jl $CPULIST
# numactl -C $CPUMASTER ./add_workers_manager.jl --cpus $CPULIST

./add_workers.jl --p 3
