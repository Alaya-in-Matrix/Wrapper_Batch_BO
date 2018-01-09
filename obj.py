import conf
import numpy
import numpy as np
import os

class Obj(object):
    def __init__(self, bounds, num_init):
        self._dim           = len(bounds)
        self._search_domain = bounds
        self._num_init_pts  = num_init
        self._sample_var    = 0.0
        self._observations  = []
        self._num_fidelity  = 0
        self.curr_best_y    = np.inf
        self.curr_best_x    = []

    def evaluate_true(self, id, x):
        work_dir   = "work/%d"  % id
        param_file = "%s/param" % work_dir
        f = open(param_file, 'w')
        for i in xrange(len(x)):
            var_name = conf.var_name[i]
            var_val  = x[i]
            f.write(".param %s = %.18g\n" % (var_name, var_val))
        f.close()
        run_cmd = "cd %s; perl run.pl" % work_dir
        os.system(run_cmd)
        fom = np.loadtxt("%s/result.po" % work_dir)
        if(fom < self.curr_best_y):
            self.curr_best_y = fom
            self.curr_best_x = x
        return np.array([fom])

    def evaluate(self, id, x):
        return self.evaluate_true(id, x)
