##################################################################
## Pyarie: Python aids for River/Ecosystem Modeling
## Copyright (C) 2005 John W Metta
##		<kuthu@users.sourceforge.net>	
## See license.txt for a copy of the GNU GPL license
##--------------------------------------------------------------------
## Module:		pamMaths.py
## Purpose:		Math class built from Python2.4's Decimal class
## Classes:		pamDecimal
##
## Notes: 
##--------------------------------------------------------------------
## $Id: pamMaths.py,v 1.1 2005/10/13 01:29:29 kuthu Exp $
###################################################################
import decimal

class pamDecimal(Decimal):
    """
    Returns an immutable Python Decimal object, built with extra methods that we need
    """
    def __new__(cls, value="0", context=None):
	    decimal.Decimal(cls, value, context)
	    # To be completed
	    pass
    