##################################################################
## Pyarie: Python aids for River/Ecosystem Modeling
## Copyright (C) 2005 John W Metta (prev. Pennington)
##		<john.pennington@lifetime.oregonstate.edu>	
## See license.txt for a copy of the GNU GPL license
##--------------------------------------------------------------------
## Module:		__version__.py
## Purpose:		Give a version string
## Classes:		None
##
## Notes:
##--------------------------------------------------------------------
## $Id: __version__.py,v 1.1 2005/10/13 01:26:50 kuthu Exp $
###################################################################

from string import join

APPEND = None
MAJOR = 0
MINOR = 0
RELEASE = 1

VERSION = (MAJOR, MINOR, RELEASE)

VERSION_STRING = join([`MAJOR`,`MINOR`,`RELEASE`], '.')

if APPEND: VERSION_STRING = join([VERSION_STRING, APPEND], '-')
