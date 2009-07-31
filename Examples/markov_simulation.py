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
    ---------------------------------------------------------------------
     $Id: markov_simulation.py,v 1.2 2005/10/13 02:34:07 kuthu Exp $
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
simulation_time = 100
timestep = 1
# Datafile to export to
datafile = 'pyarie.data'
# Initial values. This must be  a tuple of values, one per state variable
initial_values = (780.0, # eggs
                  120.0, # instar
                  23.0, # subimago
                  3.0) # imago
# These are the variable names, useful if we export to a spreadsheet
# You can leave this blank by setting to None
# varnames = None
varnames = ['egg','instar1','instar2','adult']

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
        self.products = (self.egg, \
                         self.instar1, \
#                         self.instar2, \
#                         self.instar3, \
#                         self.instar4, \
#                         self.instar5, \
#                         ...
                         self.subimago, \
                         self.imago)

        # this must be modified if more instars are added!!
        self.markov = Numeric.array( [
                        [0.0, 0.0, 0.0, 0.2], # eggs
                        [0.01, 0.2, 0.0, 0.0],     # instar
                        [0.0, 0.2, 0.0, 0.0],     # subimago
                        [0.0, 0.0, 0.1, 0.2]      # imago
                        ])
        self.g_f = 0.52 #gender factor: liklihood that adult is female
    def beta_in(self):
        #input drift rate (num individuals)
        num_drift = random.gammavariate(2, 1)*100
        print num_drift
        return num_drift

    def eggs(self):
        num_eggs = random.normalvariate(500, 100)
        return num_eggs

    def calc_matrix(self, x):
        l = []
        for i in x:
            l.append(i)
        array = Numeric.array(l)
        # Must be changed for different number of instars!
        LD = self.pest_conc() # should be stochastic or determined from input/variable
        factor = LD/100 # convert to fraction
        egg = 1.0-factor # should be some function of concentration
        in1 = 1.0-factor*(exp(factor)/10) # likewise for all instars
        subimago = 1.0 
        imago = 1.0 # assume adults unaffected by concentrations
        multiplier = Numeric.array( [egg, in1, subimago, imago] )
        matrix = multiplier*self.markov
        result = Numeric.matrixmultiply(matrix, array)
        return result
        

    def beta_out(self):
        #LD = self.pest_conc()
        norm = 0.0 # Normal drift is accounted for in the matrix
        if 1:#LD < 1.0:
            return norm
#        norm += exp(LD)/10.0
#        return norm
        
    def pest_conc(self):
        # convert current concentration into LDxx value
        return 0.0 # we don't work yet, so just return something
                 
    def egg(self, x, t): # 
        array = self.calc_matrix(x)
        result = array[0] # number of eggs left
        adults = (array[3]*self.g_f)*self.eggs()
        result += adults
        return result

    def instar1(self, x, t): # 
        array = self.calc_matrix(x)
        result = self.beta_in() # input drift
        result += array[1] # instars left
        return result

    def subimago(self, x, t):
        array = self.calc_matrix(x)
        result = array[2]
        return result

    def imago(self, x, t): #
        array = self.calc_matrix(x)
        result = array[3]
        return result

class Model(pamModel.pamModel):
    """ This is the model, it is essentially a self-scheduling
    iterator. There's a lot of backend, but basically 
    the iterate() method is the important piece. """
    def __init__(self, integrator, system, dt, initial, output=None):
    	pamModel.pamModel.__init__(self, integrator, system, dt, initial, output)

        self.egg = initial[0]
        
        #number of instars:
        instars = 2
        
        for i in range(instars): 
            exec('self.in%i = initial[%i]' % (i+1, i+1))
        self.adult = initial[i+2]
        self.monitor = monitor

        # Now we put all of our variables into a list
        self.vars = self.egg, 
        for i in range(instars):
            exec('self.vars += self.in%i,' % (i+1))
        self.vars += self.adult,
        

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