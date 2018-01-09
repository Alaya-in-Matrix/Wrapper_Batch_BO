#!/usr/bin/python
import GPy
import GPyOpt
import numpy as np
import subprocess, shlex
import matplotlib
import os, sys
import toml
import obj
from math import *
from multiprocessing import Process, Queue



argv = sys.argv[1:]
conf = toml.load(argv[0])

batch_size = conf["batch_size"]
bounds     = np.array(conf["bounds"])
max_iter   = conf["max_iter"]
num_cores  = conf["num_cores"]
num_init   = conf["num_init"]
var_name   = conf["var_name"]

os.system("rm -rf work")
os.system("mkdir work")

for i in xrange(batch_size):
    copy_cmd = "cp -r ./circuit work/%d" % i
    os.system(copy_cmd)


dim    = len(var_name)
domain = []
for i in xrange(dim):
    domain.append({'name': 'var1', 'type': 'continuous', 'domain': (bounds[i][0],bounds[i][1])})

obj_f  = obj.Obj(bounds, num_init)

def obj_func_batch(xs):
    ys = []
    for id, x in enumerate(xs):
        ys.append(obj_f.evaluate(id % batch_size, x))
    return np.array(ys)



X_init = np.random.uniform(bounds[:, 0], bounds[:, 1], (num_init, dim))
Y_init = obj_func_batch(X_init)

iter_count   = max_iter
current_iter = 0
X_step       = X_init
Y_step       = Y_init

while current_iter < iter_count:
    bo_step = GPyOpt.methods.BayesianOptimization(
            f                  = None,
            domain             = domain,
            acquisition_type   = 'EI',
            exact_feval        = True,
            X                  = X_step,
            Y                  = Y_step,
            evaluator_type     = 'local_penalization',
            batch_size         = batch_size,
            num_cores          = num_cores,
            eps                = 0,
            ARD                = True, 
            kernel             = GPy.kern.RBF(dim, variance=1., ARD=True),
            )
    print "Iter %d" % current_iter
    x_next = bo_step.suggest_next_locations()
    y_next = obj_func_batch(x_next)
    X_step = np.vstack((X_step, x_next))
    Y_step = np.vstack((Y_step, y_next))
    print x_next
    print y_next
    print 'Curr best: %.18g' % min(Y_step)
    print '--------------------'
    current_iter += 1
