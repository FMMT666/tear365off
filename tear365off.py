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
		None:   No error.
		string: A string containing the error message
	"""
	
	# check number of documents open; we accept only one
	numDocs = scribus.haveDoc()
	if   numDocs < 1:
		return "No document opened."
	elif numDocs > 1:
		return "More than one document is opened."

	# check number of pages that exist; we accept only one
	numPages = scribus.pageCount()
	if   numPages < 1:
		return "No page created."
	elif numPages > 1:
		return "Please reduce the document to a single calendar template page."
	
	# check if items exist on this page
	numItems = len( scribus.getPageItems() )
	if   numItems < 1:
		return "This page is empty."
	
	# check if at least one object's name starts with the magic "t365_" string
	magicStrings = 0
	for item in scribus.getPageItems():
		if item[0].find( "t365_" ) == 0:
			magicStrings += 1
	if magicStrings == 0:
		return "No object with modification tag 't365_' found."
		
	return None



###################################################################################################
##
##
###################################################################################################
def CreateNewPage( index ):
	# interesting:
	#   getObjectType( <name> ) -> string
	
	
	pass



###################################################################################################
##
##
###################################################################################################
def MakeCalendar( argv ):
	""" Main function to create the calendar from within Scribus.
	
	Args:
		command line
	
	Returns:
		None:   No error.
		string: A string containing the error message
	"""
	
	# check for errors in the page template
	err = CheckTemplate()
	if err != None:
		scribus.messageBox("Template Error", err )
		return err
	
	# load the ini file (and get current path)
	fileIni = scribus.fileDialog( "Select an ini file", "*.ini" , "")
	
	
	return None
	
	

###################################################################################################
###################################################################################################
###################################################################################################
if __name__ == '__main__':
	err = MakeCalendar( sys.argv )
	
	# just in case...
	if scribus.haveDoc():
		scribus.setRedraw( True )

