#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Scribus script to create custom 1..365 days/weeks/whatever tear off calendars.
# 8/2017
#
# For manuals and up to date versions, see:
# https://github.com/FMMT666/tear365off
#
# FMMT666(ASkr)
#

import sys

# TODO: pydoc will fail on this
try:
	import scribus
except ImportError, err:
	print("Please run this from within Scribus only.")
	sys.exit( 1 )


###################################################################################################
##
##
###################################################################################################
def CheckTemplate():
	""" Performs some sanity checks on the template page.
	
	Args:
		none
	
	Returns:
		None:   No error
		string: string with the error message
	"""
	
	# check number of documents open; we accept only one
	numDocs = scribus.haveDoc()
	if   numDocs < 1:
		return "No document opened."
	elif numDocs > 1:
		return "More than one document opened."

	# check number of pages that exist; we accept only one
	numPages = scribus.pageCount()
	if   numPages < 1:
		return "No page created."
	elif numPages > 1:
		return "Please delete all pages except page number 1."
	
	return None




###################################################################################################
##
##
###################################################################################################
def MakeCalendar( argv ):
	""" Main function to create the calendar from within Scribus.
	"""
	# check for errors in the page template
	err = CheckTemplate()
	if err != None:
		pass # TODO: make this visible someway...
	
	
	

###################################################################################################
###################################################################################################
###################################################################################################
if __name__ == '__main__':
	MakeCalendar( sys.argv )
	
	# just in case...
	if scribus.haveDoc():
		scribus.setRedraw( True )
	
