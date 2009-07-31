"""
    -----------------------------------------------------------------
    Pyarie: Python aids for River/Ecosystem Modeling
    Copyright (C) 2005 John W Metta
    All rights reserved, see LICENSE for details.
    
    This program is free software; you can redistribute it and/or 
    modify it under the terms of the GNU General Public License as 
    published by the Free Software Foundation; either version 2 of 
    the License, or (at your option) any later version.
    
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    -----------------------------------------------------------------
     $Id: stochastic_simulation.py,v 1.2 2005/10/13 02:34:36 kuthu Exp $
"""
# Import system modules
from string import join
from math import *
from os import system
import copy

# Import local modules
from BaseClasses import pamSystem, pamModel
from Maths.pamSolvers import pamSimple, pamRungeKutta, pamAdaptive
from Utils import pamGlobals
# Simplify the calls to integrators

#########################################################
## Here we set up the characteristics of your model.
## This may become a class in the future.

# Total time of simulation and timestep increment
simulation_time = 400
timestep = 100
# Datafile to export to
datafile = 'pyarie.data'
# Initial values. This must be  a tuple of values, one per state variable
initial_values = (10)
# These are the variable names, useful if we export to a spreadsheet
# You can leave this blank by setting to None
# varnames = None
varnames = ['population']

# Integrator. See pamSolvers for information.
# Choose from:
#    1: pamSimple()
#    2: pamRungeKutta()
#    3: pamAdaptive()
integrator = pamSimple()

dataset = {} # Currently unused
datastop = None # Currently unused

##########################################################
## System is where you define

class System(pamSystem.pamSystem):
    """ This is the system of equations that will 
    run at each timestep """
    def __init__(self, model): # name): # Name is currently unused.
        pamSystem.pamSystem.__init__(self, model)
        # These are the equations that define the variables
        # THIS LIST MUST BE IN THE PROPER ORDER FOR CALCULATIONS.
        self.products = [self.pop]
        
        self.Weibull = Weibull_Test
        self.k_min = 0.00255271
        self.k_max = 0.49523644
        self.vol = 50.0
        self.p_max = 10.0
        
    def wei(self):
        return self.Weibull.Value(random.random())
    def uni(self):
        return random.uniform(self.k_min,self.k_max)

    def pop(self, x, t): # x[0] organic nitrogen
        k = self.uni()
        Q = self.wei()
        left = k * x[0] * (self.p_max - x[0])
        right = (Q/self.vol) * x[0]
        result = left - right
        return result

class Model(pamModel.pamModel):
    """ This is the model, it is essentially a self-scheduling
    iterator. There's a lot of backend, but basically 
    the iterate() method is the important piece. """
    def __init__(self, integrator, system, dt, initial, output=None):
    	pamModel.pamModel.__init__(self, integrator, system, dt, initial, output)

        if self.file: # Check if we have a filename to spit out to
            # If we have variable names, put them at the top of the datafile
            if varnames:
                text = 'time\t' + varnames[0]
                for var in varnames[1:]:
                    text += '\t' + var
                text += '\n0\t' + `initial[0]`
                for val in initial[1:]:
                    text += '\t' + `val`
                self.file.write(text + '\n')

 #    def iterate(self):
 #        "You can define this method to override the stock behavior"
 #        pass