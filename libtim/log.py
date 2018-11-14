#!/usr/bin/env python
# encoding: utf-8
"""
@file log.py
@brief Terminal and file logging functionality

@package libtim.log
@brief Terminal and file logging functionality
@author Tim van Werkhoven (werkhoven@strw.leidenuniv.nl)
@copyright Creative Commons Attribution-Share Alike license versions 3.0 or higher, see http://creativecommons.org/licenses/by-sa/3.0/
@date 20090330

Logging functions to log data using prefixes, loglevels and permanent logfiles. This is probably only useful in more elaborate scripts.
"""

#==========================================================================
# Import libraries here
#==========================================================================

import sys
import time

#==========================================================================
# Defines
#==========================================================================

# Various levels of verbosity (make sure these increment nicely)
# EMERG = 0
# ALERT = 1
# CRIT = 2
ERR = 3
WARNING = 4
NOTICE = 5
INFO = 6
DEBUG = 7
## @brief strings describing the different loglevel
LVLDESC=['[EMERG]', \
				 '[ALERT]', \
				 '[CRIT ]', \
				 '[ERROR]', \
				 '[warn ]', \
				 '[notic]', \
 				 '[info ]', \
				 '[debug]']


## @brief Exit code for messages with the ERR level
EXIT = -1

## @brief Stores logfile when set
LOGFILE = None
LOGFD = 0
LOGLASTDAY = 0

## @brief Verbosity level to use
VERBOSITY = 8

## @brief Reset color codes
RESETCL = "\033[0m"
## @brief Debug color, blue text
DEBUGCL = "\033[34m"
## @brief Warning color, yellow text on black bg
WARNCL = "\033[33;40m"
## @brief Error color, white text on red bg
ERRORCL = "\033[37;41m"

#==========================================================================
# Routines
#==========================================================================

def initLogFile(*args):
	"""
	@deprecated Use init_logfile instead
	"""
	raise DeprecationWarning("Use init_logfile() instead")

def init_logfile(logfile):
	"""
	(Re-)initialize logging to disk at **logfile**

	@param logfile file to use for loggin
	"""
	global LOGFD
	if (not LOGFD):
		LOGFD = open(logfile, "a+")
	else:
		LOGFD.close()
		LOGFD = open(logfile, "a+")


def log_msg(verb, msg, err=EXIT):
	"""
	Print log message with a certain verbosity.

	Print a log message **msg**. If global LOGFD is set, it is also written to the file that file descriptor is poiting to. Status levels are prepended to the output.

	@param verb The status level of the message
	@param msg The message to print
	@param err Exit status to use for verb == ERR
	"""
	# First save to file if LOGFD is set...
	if (verb <= DEBUG and LOGFD):
		tm = time.localtime()
		global LOGLASTDAY
		if (LOGLASTDAY != tm[2]):
			print("-"*20, time.asctime(tm), "-"*20, file=LOGFD)
			LOGLASTDAY = tm[2]
		print(time.strftime("%H:%M:%S", tm), LVLDESC[verb], msg, file=LOGFD)
		LOGFD.flush()
	# Then print to screen
	if (VERBOSITY >= verb):
		if (verb >= INFO):
			sys.stdout.write(DEBUGCL)
			print(LVLDESC[verb], msg, RESETCL)
		elif (verb == WARNING):
			sys.stdout.write(WARNCL)
			print(LVLDESC[verb], msg, RESETCL)
		elif (verb <= ERR):
			sys.stdout.write(ERRORCL)
			print(LVLDESC[verb], msg, RESETCL)
			# If we have an error, close the file, or data might be lost
			if LOGFD: LOGFD.close()
			sys.exit(err)
		else:
			print(LVLDESC[verb], msg)

def prNot(verb, msg, err=EXIT):
	"""
	@deprecated Use log_msg instead
	"""
	raise DeprecationWarning("Use log_msg() instead")
