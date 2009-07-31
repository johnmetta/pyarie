##################################################################
## Pyarie: Python aids for River/Ecosystem Modeling
## Copyright (C) 2005 John W Metta (prev. Pennington)
##		<john.pennington@lifetime.oregonstate.edu>	
## See license.txt for a copy of the GNU GPL license
##--------------------------------------------------------------------
## Module:		pamModelBase.py
## Purpose:		Base class for all models
## Classes:		pamModelBase(name, times, init_cond) 
##
## Notes: Instances of this class must override the iterate() method,
##	which calls the integrator.step() method with the function list
##	variable list, time and timestep. All methods can be overridden,
##	but it should suffice to define a new iterate method in simple cases.
##--------------------------------------------------------------------
## $Id: pamModel.py,v 1.2 2005/10/13 02:30:35 kuthu Exp $
###################################################################

import copy
from Utils.pamGlobals import *

class pamModel(SP.Process):
    def __init__(self, integrator, system, dt, initial, output, monitor=None, name='Pyarie Model'):
        SP.Process.__init__(self)
        self.step = dt
        self.name = name
        self.logger = logger.getLogger(self.name)
        # define governing system classes. Each system has a name and
        # a tuple of conditions. The conditions coorespond to the coefficients or
        # functions needed to calculate the equations derivatives and probably
        # come from the ModelBase's conditions. As many values and functions
        # as possible should be built within the SystemBase class. Only values
        # or functions that change over time or simulations should be provided here
        # because the more we throw around between classes, the more the simulation
        # costs in computer time. In any rate, the SystemBase class must know what is
        # coming in (const, Decimal(), function, etc) and deal with it appropriately.
        # Example:
        # system1 = SomeSystem(self, 'Condition 1 Equations', (x_init, 0.8, 1.5, 0.2))
        # system2 = AnotherSystem(self, 'Condition 2 Equations', (Monitor, 0.8, 1.5), (foo), (bar))
        # system3 = ThirdSystem(self, 'Condition 3 Equations', (Function, 0.8, 0.2), (foo), (bar, bunt))

        # Place the instances of any systems that govern the model immediately in here.
        # This then determines which system's derivatives we calculate.
        self.governing_systems = system.products

        self.state = system.state
        # Set our integrator to what we were told to use
        self.integrator = integrator
        # and set our timestep (delta t)
        self.dt = dt
        # Set the output file to None if not given
        self.file = output

        # These are our variables, and we set the 
        # initial conditions, sent to us when the 
        # class was created (in pyarie.py)
        self.vars = []
        for i in range(len(initial)):
            self.vars.append(initial[i])
        # Copy values, not references, into the system's cur_state list
        system.state = copy.deepcopy(self.vars)
	
    def __repr__(self):
        "How do we represent ourselves"
        return "Pyarie Model: %s" % self.name
     
    def execute(self):
        "Active model and step through calculations using self.iterate()"
        while 1:
            yield hold, self, self.step
            self.iterate()

    def iterate(self):
        """ each timestep calls this method. The equations and 
        variables are sent to the integrator (with the current time
        and the timestep), and the new values are then stored.
        PLEASE IGNORE THE MAN BEHIND THE CURTAIN!!!"""
        values = self.integrator.step(self.governing_systems, self.vars, now(), self.dt)
        self.vars = values
        if self.file:
            self.write() # write to the file, if we have one

    def write(self):
        """ Write everything to a text file """
        text = `now()`
        for var in self.vars:
            text += '\t' + `var`
        self.file.write(text + '\n')
        