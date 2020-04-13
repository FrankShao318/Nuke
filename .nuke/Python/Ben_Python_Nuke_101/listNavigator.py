#----------------------------------------------------------------------------
# listNavigator.py
# Version: 1.0.0
# Author: Frank Shao
#
# Last Modified by: Frank Shao
# Last Updated: Apr. 12, 2020
#----------------------------------------------------------------------------

#----------------------------------------------------------------------------
# Usage:
# 
# - List selected nodes alphabetically.
# - Show details about the list in a message box.
#----------------------------------------------------------------------------

import nuke

def listNavigator():

	node_list = []

	for i in nuke.selectedNodes():
		node_list.append(i.name())

	node_list.sort()

	# Print all nodes in list.
	print ('Nodes in list:\n')

	for i in node_list:
		print ('- ' + i)

	nuke.message('There are ' + str(len(node_list)) + ' nodes in the list.\n\nThe first node in the list is ' + node_list[0] + '\nThe last node in the list is ' + node_list[-1] + '\n\nSee the script editor for all nodes in list, sorted alphabetically...')