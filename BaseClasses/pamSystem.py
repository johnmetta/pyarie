##################################################################
## Pyarie: Python aids for River/Ecosystem Modeling
## Copyright (C) 2005 John W Metta (prev. Pennington)
##		<john.pennington@lifetime.oregonstate.edu>	
## See license.txt for a copy of the GNU GPL license
##--------------------------------------------------------------------
## Module:		pamSystemBase.py
## Purpose:		Base class for systems of equations
## Classes:		pamSystemBase() 
##
## Notes: Instances of this class must have a list of functions
##	called (like something_xderiv(), something_yderiv(), etc) which return values calculated at
##	the timestep. execute()	can be overridden, but this version should suffice
##	if functions turnon() and turnoff() are provided, each resolving to true
##	when the equations begin or cease to govern the model, respectively.
##	The simplest case, when the equations are always valid, is that turnon() would
##	return true and turnoff return false. Such is the default case.
##--------------------------------------------------------------------
## $Id: pamSystem.py,v 1.1 2005/10/13 01:29:10 kuthu Exp $
###################################################################

from Utils.pamGlobals import *

class pamSystem(SP.Process):
    """SystemBase(model, name) -> SystemBase instance
    Returns instance of class for a system of equations that 
    governs the model given a specific condition. self.test()
    is the method that tests for specific conditions, when seen,
    the class includes its products in the models function list.
    """
    def __init__(self, model, name='Pyarie System'):
        SP.Process.__init__(self, name)
        self.name = name
        self.products = [] # something like [ self.xderiv, self.yderiv ]
        self.logger = logger.getLogger(name)
        self.model = model
        self.state = []
	
    def __repr__(self):
        return "Pyarie system: %s in model: %s" % (self.name, self.model.name)

    # Quick method to update the current state.
    def update_state(self,index,value):
        "Update the values of the state variables at time t for use by equations"
        self.state[index] = value

    def execute(self):
        "wait until model calls us, then set model's equations"
        self.log('Equation %s activated' % self.name)
        while 1:
            yield waituntil, self, self.turnon
            self.log('%s now governed by equations in %s' % (self.model.name, self.name))
            # This makes it necessary that every system have unique function names
            for i in self.products: self.model.governing_systems.append(i)
            yield waituntil, self, self.turnoff
            self.log('equations in %s no longer governing %s' % (self.name, self.model.name))
            for i in self.products: self.model.governing_systems.remove(i)
	
    def turnon(self):
        "Model is governed by our equations"
        return True
	
    def turnoff(self):
        "Model is no longer governed by our equations"
        return False
	
    def log(self, msg, lvl=logger.INFO):
        "log events"
        msg = 'Time ' + `now()` + ": " + msg
        self.logger.log(lvl, msg)