##################################################################
## Pyarie: Python aids for River/Ecosystem Modeling
## Copyright (C) 2005 John W Metta
##        <kuthu@users.sourceforge.net>    
## See license.txt for a copy of the GNU GPL license
##--------------------------------------------------------------------
## Module:		pamLogger.py
## Purpose:		Base logging class
## Classes:		pamLogger() -> pamRootLog instance
##
## Notes: Root log class. Each class will then have a self.Log() 
## method which logs to a logger child of this base log class. The 
## superclass is unchanged now, but can be modified and overloaded
## in the future. This module should be called first in program.
##--------------------------------------------------------------------
## $Id: pamLogger.py,v 1.1 2005/10/13 01:29:29 kuthu Exp $
###################################################################

import logging

#log_levels = 	[(0, 'DATA'),
#		(1, 'DEBUG'),
#		(2, 'INFO'),
#		(3, 'WARN'),
#		(4, 'ERROR'),
#		(5, 'CRITICAL'),
#		(6, 'EXCEPTION')]
#map(lambda x: logging.addLevelName(x[0], x[1]), log_levels)

class pamLogger(logging.getLoggerClass()):
    """
    Main logger class instance, copied from logging.__init__.py.
    To be uncommented and modified as needed.
    """
    def __init__(self):
        logging.Logger.__init__(self, name="pamRootLog")

##########################################################
# Set up a console and a file logger.

data_log_level = 45 #Log data at lower precedence than critical, 
		    # but higher than error
logging.addLevelName(data_log_level, 'DATA')

# Set basic logging to DEBUG level
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='/tmp/pyarie.log',
                    filemode='w')
# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
## set a format which is simpler for console use
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
## tell the handler to use this format
console.setFormatter(formatter)
logging.getLogger().addHandler(console)
