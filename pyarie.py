#!/usr/bin/env python
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
	Module:		pyarie.py
	Purpose:	Entrance to user space program
	Classes:	None
	 
	Notes:
	-----------------------------------------------------------------
 	$Id: pyarie.py,v 1.1 2005/10/13 01:26:50 kuthu Exp $
"""
####################
# Check Python version greater than 2.3 before starting
import sys
v1 = sys.version_info[0]
v2 = sys.version_info[1]
if v1 + v2 < 6:
    raise Exception, "Python version 2.4 or later is needed for this program."
del sys,v1, v2 # clean up
######################


#####################
## Import everything we need
import simulation
from Maths.pamSolvers import pamRungeKutta, pamAdaptive
#import Gnuplot, Gnuplot.funcutils

import logging, time, copy
import SimPy.Simulation
SP = SimPy.Simulation
hold = SP.hold
now = SP.now
waituntil = SP.waituntil
logger = logging
##############################

# Do we have a datafile?
if simulation.datafile: file = open(simulation.datafile,'w')
else: file = None

# Mount the system and set up the model
system = simulation.System(None)
model = simulation.Model(integrator=simulation.integrator,\
                    system=system, \
                    dt=simulation.timestep, \
                    initial=simulation.initial_values, 
                    output=file)

# initialize the scheduling system
SP.initialize()
# activate the model and make sure it's set up
SP.activate(model, model.execute())
# run the model until the simulation end-time
SP.simulate(until=simulation.simulation_time)
# close the output file
if simulation.datafile: file.close()

## Start a plotter
#g = Gnuplot.Gnuplot(persist=1)
#
## Set it up for multiple plots
#g('set style function lines')
##g('set size 2.0,2.0')
##g('set origin 0.0,0.0')
##g('set multiplot')
#g('set grid')
#
## plot Nitrogen
#g('set size 0.5,0.5')
#g('set origin 0.0,0.5')
#g('set title "Stochastic Reactor"')
#g('set xlabel "Time in Days"')
#g('set ylabel "Population"')
#g("""plot "%s" using 1:2 notitle with linespoints""" % filename)
#
#	"%s" using 1:3 title "Ammonia" with linespoints, \
#	"%s" using 1:4 title "Nitrite" with linespoints""" % (filename, filename, filename))
#
## Plot Oxygen
#g('set size 0.5,0.5')
#g('set origin 0.0,0.0')
#g('set title "Dissolved Oxygen"')
#g('plot "%s" using 1:6 notitle with linespoints' % filename)
#
## Plot Bacteria
#g('set size 0.5,0.5')
#g('set origin 0.5, 0.5')
#g('set title "Aerobic Bacterial Populations"')
#g("""plot "%s" using 1:7 title "Population 1" with linespoints, \
#	"%s" using 1:8 title "Population 2" with linespoints, \
#	"%s" using 1:9 title "Population 3" with linespoints""" % (filename, filename, filename))
#
## Plot Anerobic
#g('set size 0.5,0.5')
#g('set origin 0.5,0.0')
#g('set title "Anaerobic Bacteria and Nitrate"')
#g("""plot "%s" using 1:5 title "Nitrate" with linespoints, \
#	"%s" using 1:10 title "Bacteria" with linespoints""" % (filename, filename))
#
#g('unset multiplot')

