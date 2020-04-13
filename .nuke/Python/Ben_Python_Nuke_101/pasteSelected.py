#----------------------------------------------------------------------------
# pasteSelected.py
# Version: 1.0.0
# Author: Frank Shao
#
# Last Modified by: Frank Shao
# Last Updated: Apr. 12, 2020
#----------------------------------------------------------------------------

#----------------------------------------------------------------------------
# Usage:
# 
# - Paste previous copied node to all the selected nodes.
#----------------------------------------------------------------------------

import nuke

def paste_selected():

	for i in nuke.selectedNodes():
		i.setSelected(True)
		nuke.nodePaste('%clipboard%')