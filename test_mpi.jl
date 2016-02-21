using MPI
import MPI

MPI.Init()
rank = MPI.Comm_rank(MPI.COMM_WORLD)
size = MPI.Comm_size(MPI.COMM_WORLD)

manager = MPI.start_main_loop(MPI_TRANSPORT_ALL)

println("Hello from rank $rank")
println("Size $size")

@everywhere function print_cpus()
    run(pipeline(`ps -eo pid,psr,pcpu,cmd`, `grep julia`))
end

println("Before map")
print_cpus()

@everywhere function pcpus(mat)
    println("In map")
    print_cpus()
    svd(mat)
end

M = [rand(1000,1000) for i=1:3]

pmap(pcpus, M)

println("After map.")
print_cpus()

MPI.stop_main_loop(manager)
