#----------------------------------------------------------------------------
# filePathLister.py
# Version: 1.0.0
# Author: Frank Shao
#
# Last Modified by: Frank Shao
# Last Updated: Apr. 12, 2020
#----------------------------------------------------------------------------

#----------------------------------------------------------------------------
# Usage:
# 
# - List all files being read into a nuke script.
#----------------------------------------------------------------------------

import nuke
import os

def file_lister():

	print ('\n\nNuke Script: ' + os.path.basename(nuke.root()['name'].value()))
	print ('\nFile & Version List:')

	node_classes = ['Read', 'ReadGeo', 'Cammera']
	node_list = []

	for i in nuke.allNodes():
		for x in node_classes:
			if i.knob('file') and i.Class() == x:
				node_list.append(i)

	for node in node_list:
		filepath = node['file'].value()
		filename = os.path.basename(filepath)

		filename_no_version = filename[0:filename.find('_v')]
		version_number = filename[filename.find('_v')+1 : filename.find('_v')+6]

		print ('You are using ' + version_number + ' of ' + filename_no_version)