#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Scribus script to create custom 1..365 days/weeks/whatever tear off calendars or whatever.
# 8/2017
#
# For manuals and up to date versions, see:
# https://github.com/FMMT666/tear365off
#
# This code uses tabs. Tabs everywhere.
# Deal with it.
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


# Beginning of the magic string tagging Scribus' objects that shall be modified
MAGICSTRING = "t365_"


###################################################################################################
##
##
###################################################################################################
def TemplateCheck():
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
	
	# check if at least one object's name starts with the MAGICSTRING
	magicStrings = 0
	for item in scribus.getPageItems():
		if item[0].find( MAGICSTRING ) == 0:
			magicStrings += 1
	if magicStrings == 0:
		return "No object with file name tag 't365_' found."
		
	return None



###################################################################################################
##
##
###################################################################################################
def TemplateGetFileNames():
	""" Analyse Scibus' object names and return a list of file names associated with them.
	
	Args:
		none
	
	Returns:
		list:   A list with file names, e.g [ "day.t365", "month.t365", ... ]
		        If nothing was found, an empty list [] will be returned.
	"""
	
	listNames = []
	for item in scribus.getPageItems():
		if item[0].find( MAGICSTRING ) == 0:
			fileName = item[0][len( MAGICSTRING ):]
			if fileName != "":
				listNames += [ fileName ]
			
	return listNames



###################################################################################################
##
##
###################################################################################################
def FilesCheckContent( path, listNames ):
	""" Analyse the Scibus' objects associated files and their content.
	
	 So far, it is only checked whether:
	  - the file exists and is readable
	  - the number of entries in the files match
	
	Args:
		list:   List with file names
	
	Returns:
		None  : No error occured.
		string: A string containing the error message."
	"""
	
	err = None
	
	# a list with the number of lines per file(name)
	# Should be a dict, but that would be more complicated later on...
	lineNumbers = []
	
	# for the complete list of file names
	for fileName in listNames:
		
		# create a complete file name
		tmpStr = path + "/" + fileName + ".t365"
		
		# open the file
		try:
			fin = open( tmpStr, "r+t" )
		except:
			err = "unable to open file " + tmpStr
			return err
		
		# count the lines in the file (TODO: check what's in there)
		n = 0
		for line in fin:
			n += 1
		lineNumbers.append( n )
		
		# close the file
		fin.close()
		
	# check whether we collected the data right
	# (this should never fail)
	if len( listNames ) != len ( lineNumbers ):
		err = "unable to count the lines in the files"
		return err
	
	# Check whether all files contain the same amount of lines
	if lineNumbers.count( lineNumbers[0] ) != len( lineNumbers ):
		err = "Amount of lines does not match:"
		for i in range( len(lineNumbers) ):
			err += "\n " + listNames[i] + ": " + str( lineNumbers[i] )
	
	
	return err
	



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
	err = TemplateCheck()
	if err != None:
		scribus.messageBox("Template Error", err )
		return err
	
	# ask user for working directory
	path = scribus.fileDialog( "Select the working directory", "" , "", isdir = True )
	if path == "" or path == None:
		scribus.messageBox("tear365off", "aborting..." )
		return None
	
	# get file names from template page
	listFileNames = TemplateGetFileNames()
	if listFileNames == []:
		err = "No valid file name tag 't365_' found"
		scribus.messageBox("Template Error", err )
		return err
	
	# check the contents of the files (roughly)
	err = FilesCheckContent( path, listFileNames )
	if err != None:
		scribus.messageBox("File content mismatch", err )
	
	
	
	return None



###################################################################################################
###################################################################################################
###################################################################################################
if __name__ == '__main__':
	err = MakeCalendar( sys.argv )
	
	# just in case...
	if scribus.haveDoc():
		scribus.setRedraw( True )

