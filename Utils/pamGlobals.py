##################################################################
## Pyarie: Python aids for River/Ecosystem Modeling
## Copyright (C) 2005 John W Metta
##        <kuthu@users.sourceforge.net>    
## See license.txt for a copy of the GNU GPL license
##--------------------------------------------------------------------
## Module:		pamglobals.py
## Purpose:		global variables
## Classes:		None
##
## Notes:
##--------------------------------------------------------------------
## $Id: pamGlobals.py,v 1.1 2005/10/13 01:29:29 kuthu Exp $
###################################################################

import logging
import SimPy.Simulation
SP = SimPy.Simulation
hold = SP.hold
now = SP.now
waituntil = SP.waituntil
logger = logging
