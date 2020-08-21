#----------------------------------------------------------------------------
# Node_Disabler.py
# Version: 1.0.0
# Author: Frank Shao
#
# Last Modified by: Frank Shao
# Last Updated: Aug. 20, 2020
#----------------------------------------------------------------------------

#----------------------------------------------------------------------------
# Usage:
# 
# - Add nodes to a list, disable or enable nodes in the list.
#----------------------------------------------------------------------------


# ---------------------
# addNodes button code:
# ---------------------

# Create list.
node_list = []

# Loop through selected nodes, and add their names to node_list.
for i in nuke.selectedNodes():
	node_list.append(i.name())

# Hide the start knob & show the add more knob.
nuke.thisNode().knob('addMoreNodes').setVisible(True)
nuke.thisNode().knob('addNodes').setVisible(False)

# Check if things are working...
print node_list

# Turn the list into a single string, and add a line break, a bullet point and a space in between each item.
node_list_cleaned = '\n・ '.join(node_list)

# Set the value of the txt knob.
nuke.thisNode()['txtknob_node_list'].setValue('・ ' + node_list_cleaned)

# Define function for knobChange.
def disableNodesInList():

	# Loop through all the nodes in node_list.
	for i in node_list:

		# Check if the node has a disable knob.
		if nuke.toNode(i).knob('disable'):

			# If it does, set its disable knob to the value of Node_Disabler's disable knob.
			nuke.toNode(i).knob('disable').setValue(nuke.thisNode().knob('disable').value())

        # If the node does not have a disable knob, print an error message in the Script Editor.
		else:
			print '- ' + i + " does not have a 'disable' knob! Ignoring..."

# Add the knobChange callback to Node_Disabler.
nuke.toNode('Node_Disabler').knob('knobChanged').setValue('disableNodesInList()')


# -------------------------
# addMoreNodes button code:
# -------------------------

# Loop through selected nodes.
for i in nuke.selectedNodes():

	# Check if the selected node's name is already in node_list.
	if i.name() in node_list:

		# If it is, print a message to the Script Editor.
		print i.name() + ' is already in the list.'

	# But if it isn't in node_list, add it.
    else:
    	node_list.append(i.name())

# Check if things are working...
print node_list

# Turn the list into a single string, and add a line break, a bullet point and a space in between each item.
node_list_cleaned = '\n・ '.join(node_list)

# Set the value of the txt knob.
nuke.thisNode()['txtknob_node_list'].setValue('・ ' + node_list_cleaned)


# ----------------------
# clearList button code:
# ----------------------

# Create list.
node_list = []

# Reset visibility.
nuke.thisNode().knob('addNodes').setVisible(True)
nuke.thisNode().knob('addMoreNodes').setVisible(False)

# Reset the Node List: text knob to be 'None'.
nuke.thisNode()['txtknob_node_list'].setValue('・None')


# --------------------
# Node_Disabler label.
# --------------------

# TCL expression, use double quotation marks.
[expr { [value disable] == true ? "Nodes Disabled" : "Nodes Enabled"} ]






