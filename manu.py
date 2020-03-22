#----------------------------------------------------------------------------
# menu.py
# Version: 1.0.0
# Last Updated: Mar. 22nd, 2020
#----------------------------------------------------------------------------

import nuke
import platform

# Define where .nuke directory is on each OS's network.

Win_Dir = "C:\Users\yupushao\.nuke"
MacOS_Dir = "/Users/yupushao/.nuke"
Linux_Dir = "/home/yupushao/.nuke"

# Set global directory

if platform.system() == "Windows":
	dir = Win_Dir
elif platform.system() == "Darwin":
	dir = MacOS_Dir
elif platform.system() == "Linux":
	dir = Linux_Dir
else:
	dir = None




toolbar = nuke.menu("Nodes")
toolbar.addCommand("FrankTool/GradeTool", "nuke.createNode('GradeTool')")
