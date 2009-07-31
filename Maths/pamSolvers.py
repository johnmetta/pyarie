##################################################################
## Pyarie: Python aids for River/Ecosystem Modeling
## Copyright (C) 2005 John W Metta
##        <kuthu@users.sourceforge.net>    
## See license.txt for a copy of the GNU GPL license
##--------------------------------------------------------------------
## Module:		pamSolvers.py
## Purpose:		Numerical methods for solving ODEs
## Classes:		pamSolver() -> default Euler method
##				pamRungeKutta() -> 4th order RK
##				pamAdaptive() -> Adaptive step method
##
## Notes:
##--------------------------------------------------------------------
## $Id: pamSolvers.py,v 1.1 2005/10/13 01:29:29 kuthu Exp $
###################################################################

from copy import *
from math import *
from Utils.pamGlobals import *
from SimPy.Simulation import now

class pamSolver:
    """
    Solver(function, variables, time, delta_time) -> instance
    Base class for the various ODE solvers. Classes
    should override the step() function to become a new
    solver. Default step() function is Euler ODE solver
    """  
    def __init__(self, name='Euler'):
	self.name = name
	self.logger = logger.getLogger(self.name)
	if self.name == 'Euler': self.log('activated')

    def getName(self):
	    return self.name
	   
    def step(self, f, x, t, dt):
	    new_vals = []
	    for i in range(len(x)):
		    new_vals.append(x[i] + dt * f[i](x,t))
	    return new_vals

    def log(self, msg, lvl=logger.INFO):
	"Log events"
	msg = 'Time ' + `now()` + ': ' + msg
	self.logger.log(lvl, msg)

class pamSimple(pamSolver):
    """
    Simply step through the equations
    """
    def __init__(self):
        pamSolver.__init__(self, 'Simple')
        self.log('activated')
        
    def step(self, f, x, t, delta_t):
        new_vals = []
        for i in range(len(x)):
            new_vals.append(f[i](x,t))
        return new_vals

class pamRungeKutta(pamSolver):
    """
    Runge-Kutta 4th order solver
    """
    def __init__(self):
	    pamSolver.__init__(self, 'RungeKutta')
	    self.log('activated')
	
    def step(self, f, x, t,delta_t):
        # create lists for the constants and new values for the variables
        k1 = []; k2 = []; k3 = []; k4 = []; tmpx = []; newx = []
        for index in range(0,len(x)):
            k1.append(0); k2.append(0); k3.append(0); k4.append(0)
	    tmpx.append(0); newx.append(0);
        # compute the k1's
        for index in range(0,len(x)):
            k1[index] = delta_t*f[index](x,t)
        # compute the k2's
        for index in range(0,len(x)):
            tmpx[index] = x[index] + k1[index]/2
        for index in range(0,len(x)):
            k2[index] = delta_t*f[index](tmpx,t+delta_t/2)
        # compute the k3's
        for index in range(0,len(x)):
            tmpx[index] = x[index] + k2[index]/2 
        for index in range(0,len(x)):
            k3[index] = delta_t*f[index](tmpx,t+delta_t/2)
        # compute the k4's
        for index in range(0,len(x)):
            tmpx[index] = x[index] + k3[index]
        for index in range(0,len(x)):
            k4[index] = delta_t*f[index](tmpx,t+delta_t)
        # compute the new variables
        for index in range(0,len(x)):
            newx[index] = x[index] + ( k1[index]+2*k2[index]+2*k3[index]+k4[index] )/6
        return newx


class pamAdaptive(pamSolver):
    """
    Adaptive solver
    """
    def __init__(self, min_step=1e-6, max_step=1e-1, min_tol=1e-7, max_tol=1e-3, init_time_step=0):
	pamSolver.__init__(self, 'Adaptive')
        self.min_step = min_step
        self.max_step = max_step
        self.min_tol = min_tol
        self.max_tol = max_tol
        self.resultbuffer = 0
        self.timebuffer = 0
        if init_time_step==0:
            self.delta_t = (max_step + min_step)/2.
        else:
            self.delta_t = init_time_step

    def compute_error(self, f, x, t, delta_t):
        # define all the constants for Runge-Kutta of order 4 and 5
        # reference: Numerical Recipes
        a2 = 1/5.; a3 = 3/10.; a4 = 3/5.; a5 = 1.; a6 = 7/8.
        b21 = 1/5.
        b31 = 3/40.; b32 = 9/40.
        b41 = 3/10.; b42 = -9/10.; b43 = 6/5.
        b51 = -11/54.; b52 = 5/2.; b53 = -70/27.; b54 = 35/27.
        b61 = 1631/55296.; b62 = 175/512.; b63 = 575/13824.; b64 = 44275/110592.; b65 = 253/4096.
        c1 = 37/378.; c2 = 0.; c3 = 250/621.; c4 = 125/594.; c5 = 0.; c6 = 512/1771.
        d1 = 2825/27648.; d2 = 0.; d3 = 18575/48384.; d4 = 13525/55296.; d5 = 277/14336.; d6 = 1/4.

        n = len(x)
        # create lists for the constants and new values for the variables
        k1 = []; k2 = []; k3 = []; k4 = []; k5 = []; k6 = []
        tmpx = []; newx4 = []; newx5 = []; errors = []
        for index in range(0,n):
            k1.append(0); k2.append(0); k3.append(0); k4.append(0); k5.append(0); k6.append(0);
            tmpx.append(0); newx4.append(0); newx5.append(0); errors.append(0)
        # compute the k1's
        for index in range(0,n):
            k1[index] = delta_t*f[index](x,t)
        # compute the k2's
        for index in range(0,n):
            tmpx[index] = x[index] + b21*k1[index]
        for index in range(0,n):
            k2[index] = delta_t*f[index](tmpx,t+a2*delta_t)
        # compute the k3's
        for index in range(0,n):
            tmpx[index] = x[index] + b31*k1[index] + b32*k2[index]
        for index in range(0,n):
            k3[index] = delta_t*f[index](tmpx,t+a3*delta_t)
        # compute the k4's
        for index in range(0,n):
            tmpx[index] = x[index] + b41*k1[index] + b42*k2[index] + b43*k3[index]
        for index in range(0,n):
            k4[index] = delta_t*f[index](tmpx,t+a4*delta_t)
        # compute the k5's
        for index in range(0,n):
            tmpx[index] = x[index] + b51*k1[index] + b52*k2[index] + b53*k3[index] + b54*k4[index]
        for index in range(0,n):
            k5[index] = delta_t*f[index](tmpx,t+a5*delta_t)
        # compute the k6's
        for index in range(0,n):
            tmpx[index] = x[index] + b61*k1[index] + b62*k2[index] + b63*k3[index] + b64*k4[index] + b65*k5[index]
        for index in range(0,n):
            k6[index] = delta_t*f[index](tmpx,t+a6*delta_t)
            
        # compute the new variables
        for index in range(0,n):
            newx5[index] = x[index] + c1*k1[index] + c2*k2[index] + c3*k3[index] + c4*k4[index] + c5*k5[index] + c6*k6[index]
            newx4[index] = x[index] + d1*k1[index] + d2*k2[index] + d3*k3[index] + d4*k4[index] + d5*k5[index] + d6*k6[index]

        # compute the errors
        for index in range(0,n):
            errors[index] = abs(newx5[index] - newx4[index])

        self.resultbuffer = deepcopy(newx5)
        self.timebuffer = t+delta_t
        return max(errors)

    def getnewdelta_t(self, f, x, t, max_delta_t=0):
        if max_delta_t==0:
            max_delta_t = self.max_step
        if self.delta_t > max_delta_t:
            self.delta_t = max_delta_t

        done = 0
        while done==0:
            error = self.compute_error(f, x, t, self.delta_t)
            if error > self.max_tol:
                if self.delta_t/2. < self.min_step:
#                    print 'Min step reached...'
                    self.delta_t = self.min_step
                    self.compute_error(f, x, t, self.delta_t)                    
                    done = 1
                else:
#                    print 'Halving...'
                    self.delta_t = self.delta_t / 2.
            elif error < self.min_tol:
                if self.delta_t*2 > max_delta_t:
                    # do not go over the specified time step
                    self.delta_t = max_delta_t
                    self.compute_error(f, x, t, self.delta_t)
                    done = 1                    
                elif self.delta_t*2 > self.max_step:
#                    print 'Max step reached...'                    
                    self.delta_t = self.max_step
                    self.compute_error(f, x, t, self.delta_t)
                    done = 1
                else:
#                    print 'Doubling... ' + `self.delta_t*2`
                    self.delta_t = self.delta_t*2
            else:
                done = 1    
#        print 'time: %1.4f, timestep: %2.8f' % (now(), self.delta_t)
        return self.delta_t

    def step(self, f, x, t, delta_t=0):
        if delta_t==0:
	    # we should have called getnewdelta_t before, to obtain the time
	    # step used and hence the solution should already be computed and
	    # put in resultbuffer            
            if self.timebuffer!=t+self.delta_t:
                print 'WARNING: This was not expected to ever occur!!!!'
                self.getnewdelta_t(f, x, t, delta_t)
            return self.resultbuffer
        else:
            # run the adaptive integration until we reach t+delta_t
            curtime = t
            curx = x
            while curtime < t+delta_t:
                self.getnewdelta_t(f, curx, curtime, (t+delta_t)-curtime)
                curx = self.step(f, curx, curtime)
                curtime = curtime + self.delta_t
            return curx
            
