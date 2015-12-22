# ParallelTest.jl
How to get parallel Julia programs working on Odyssey

Now that we do have `cpu_list_numa.py` and AffinityManager working properly on a single node, let's try getting things working across nodes.

This means learning from slurm what machines we are able to run on, and feeding this to a machinefile that Julia will load. The machinefile format is

[count*][user@]host[:port] [bind_addr[:port]]


Paul Edmon says:
We have those nodes defined as have 16 cores and 4 sockets.  

That's not strictly true, as the AMD chips have 2 IC for every FPU.  So in reality it is more like 8 FPUS, 16 IC's, and 4 sockets.  If we go with the default conf then Slurm wants to do 8 cores, 2 threads per core and 4 sockets. However we found that it was undersubscribing nodes for serial runs. Namely it would only put 32 cores worth of work for serial work, when you could put 64 cores worth of work.  So we faked it out and told it that it had 16 cores, 1 thread, and 4 sockets.  This could certainly have led to a weird enumeration. Though I can't guarantee even if we had the proper configuration that it would be 1-1 in terms of the numbering that slurm gives.  I would naively assume yes as I don't see why they would renumber it.


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

#SBATCH -B 1:4

#SBATCH --verbose

Some minor success, I guess. Worker process still on same as master, but otherwise they didn't conflict.


#SBATCH -N 1 #ensure all jobs are on the same node

#SBATCH -n 8

#SBATCH -B 1:8:1

#SBATCH --verbose

Nope, we had overlap.

#SBATCH -N 1 #ensure all jobs are on the same node

#SBATCH -n 8

#SBATCH -B 1:8:1

#SBATCH --ntasks-per-core 1

#SBATCH --verbose

This actually seemed to work pretty well. Let's test whether we need the 1:8:1 constraint.

#SBATCH --mem 2000 #memory request per node

#SBATCH -N 1 #ensure all jobs are on the same node

#SBATCH -n 8

#SBATCH --ntasks-per-core 1

#SBATCH --verbose

Ok, this didn't work. Let's try with just 1:8 and not 1:8:1

#SBATCH -N 1 #ensure all jobs are on the same node

#SBATCH -n 8

#SBATCH -B 1:1:1

#SBATCH --ntasks-per-core 1

#SBATCH --verbose

We had some overlap, but not drastic.

#SBATCH -N 1 #ensure all jobs are on the same node

#SBATCH -n 4

#SBATCH -B *:*:1

#SBATCH --ntasks-per-core 1

#SBATCH --verbose

This did not work, and resulted in cores on same processors.

#SBATCH -N 1 #ensure all jobs are on the same node

#SBATCH -n 4

#SBATCH -B 1:4:1

#SBATCH --ntasks-per-core 1

#SBATCH --verbose

This seemed to work, but put two processes on the master process.

#SBATCH -N 1 #ensure all jobs are on the same node

#SBATCH -n 4

#SBATCH -B 1:1:1

#SBATCH --ntasks-per-core 1

#SBATCH --verbose

This put two workers on the master process, but otherwise ok.
