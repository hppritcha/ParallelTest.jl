#!/usr/bin/env julia

# Lets add workers programatically, and see if they distribute to different cores.

p = nworkers()
println("Workers allocated ", p)
println("Total workers ", workers())

println("Total processes ", nprocs())

@everywhere function print_cpus()
    run(`ps -eo pid,psr,pcpu,cmd` |> `grep julia`)
end

println("Before map")
print_cpus()

@everywhere function pcpus(mat)
    println("In map")
    print_cpus()
    svd(mat)
end

M = {rand(1000,1000) for i=1:p}

pmap(pcpus, M)

println("After map.")
print_cpus()
