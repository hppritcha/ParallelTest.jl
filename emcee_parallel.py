#!/usr/bin/env python

# Does the same CPU affinity fail with a python program?

import numpy as np
import emcee

def lnprob(p, ivar):

    #Add a significant computational component that may require launching command line scripts.
    for i in range(2000):
        a = i*10

    return -0.5 * np.sum(ivar * p ** 2)

ndim, nwalkers = 4, 16
ivar = 1. / np.random.rand(ndim)
p0 = [np.random.rand(ndim) for i in range(nwalkers)]

sampler = emcee.EnsembleSampler(nwalkers, ndim, lnprob, args=[ivar], threads=int(nwalkers/2))

sampler.run_mcmc(p0, 1000)
