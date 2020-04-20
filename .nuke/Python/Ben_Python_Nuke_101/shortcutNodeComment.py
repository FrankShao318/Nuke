#----------------------------------------------------------------------------
# shortcut_NodeComment.py
# Version: 1.0.0
# Author: Frank Shao
#
# Last Modified by: Frank Shao
# Last Updated: Apr. 18, 2020
#----------------------------------------------------------------------------

#----------------------------------------------------------------------------
# Usage:
# 
# - Adds ctrl+alt+c shortcut to crete a node's label, so you don't waste valuable
#   clicks opening a node and switching to the Node label!
#----------------------------------------------------------------------------

import nuke

def shortcut_NodeComment():

	# Assign the selected node to a variable for easy access.
	selectedNode = nuke.selectedNode()

	# Assign the current value of the selected node's label to a variable for easy access.
	oldComment = selectedNode['label'].value()

	# Create a variable that asks a user for a string via a pop-up text input box.
	# If there is already a node label, use it as the default string.
	inputBox = nuke.getInput('Please enter a node label.', oldComment)

	# Run an if statement to check if the Cancel button was pressed.
	if inputBox == None:
		# If it was, throw up an error message.
		nuke.message('Node label will remain as ' + oldComment)
	# Otherwise, set the selected node's label to whatever text was entered.
	else:
		selectedNode['label'].setValue(inputBox)


# Add menu items.
nuke.menu('Nuke').addCommand('Edit/Shortcuts/Add Comment to Node', 'shortcutNodeComment.shortcut_NodeComment()', 'ctrl+alt+c')