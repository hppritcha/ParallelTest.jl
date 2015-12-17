# ParallelTest.jl
How to get parallel Julia programs working on Odyssey

Now that we do have `cpu_list_numa.py` and AffinityManager working properly on a single node, let's try getting things working across nodes.


Now, let's try a number of different submission options using SLURM


#SBATCH -N 1 #ensure all jobs are on the same node

###SBATCH -n 4

#SBATCH --sockets-per-node=4

#SBATCH --cores-per-socket=1

#SBATCH --threads-per-core=1

#SBATCH --ntasks-per-core=4

#SBATCH --ntasks-per-socket=1

This didn't work, allocated 4 processes, but workers stuck one on master process and one on another worker.


#SBATCH -N 1 #ensure all jobs are on the same node

###SBATCH -n 4

#SBATCH --sockets-per-node=4

#SBATCH --cores-per-socket=1

#SBATCH --threads-per-core=1

#SBATCH --ntasks-per-core=1

#SBATCH --ntasks-per-socket=1

Still the same crap


#SBATCH -N 1 #ensure all jobs are on the same node

###SBATCH -n 4

#SBATCH --sockets-per-node=1

#SBATCH --cores-per-socket=4

#SBATCH --threads-per-core=1

#SBATCH --ntasks-per-core=1

#SBATCH --ntasks-per-socket=4

Ended up landing completely on the same core.


#SBATCH -N 1 #ensure all jobs are on the same node

#SBATCH -n 4

#SBATCH --sockets-per-node=1

#SBATCH --cores-per-socket=4

#SBATCH --threads-per-core=1

#SBATCH --ntasks-per-core=1

#SBATCH --ntasks-per-socket=4
