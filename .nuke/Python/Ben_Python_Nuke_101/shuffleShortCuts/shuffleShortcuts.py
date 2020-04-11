#----------------------------------------------------------------------------
# shuffleShortcuts.py
# Version: 0.2.0
# Last Updated: Apr. 11, 2020
#----------------------------------------------------------------------------

#----------------------------------------------------------------------------
# Usage:
# Creates a shuffle node that shuffle RGBA channels into R,G,B, or Black, White channel.
#----------------------------------------------------------------------------

import nuke

# Define the function.
def createCustomShuffle(in_channel, out_channel, set_channel, rColor, gColor, bColor):

    # Create a new shuffle node, and assign it to a variable so we can change something.
    
    myShuffle = nuke.createNode('Shuffle')

    # Change the input & output channels to what is defined in the in_channel and out channel arguments.
    myShuffle['in'].setValue(in_channel)
    myShuffle['out'].setValue(out_channel)
    
    # Change the relevant knobs to shuffle the RGBA channels to the green channel.
    
    myShuffle['red'].setValue(set_channel)
    myShuffle['green'].setValue(set_channel)
    myShuffle['blue'].setValue(set_channel)
    myShuffle['alpha'].setValue(set_channel)   
    
    # Change the node color to green (we have to convert Nuke's weird hex color values to RGB to be a bit
    # more human-readable)
    
    myShuffle['tile_color'].setValue(int('%02x%02x%02x%02x' % (rColor*255, gColor*255, bColor*255, 1), 16)) 
    
    # Add a node label.
    
    myShuffle['label'].setValue('[value red] >> [value out]')



# Define the function.
def shuffleRGBchannel():

    # Create a variable for the selected node, before creating any shuffle node.
    selectedNode = nuke.selectedNode()

    # Get the x position and y position of the selected node.
    selectedNode_xPos = selectedNode['xpos'].value()
    selectedNode_yPos = selectedNode['ypos'].value()

    # Create our red, green and blue shuffle nodes, and assign them to a variable after creation.
    createCustomShuffle('rgba', 'rgba', 'red', 1, 0, 0)
    redShuffle = nuke.selectedNode()
    createCustomShuffle('rgba', 'rgba', 'green', 0, 1, 0)
    greenShuffle = nuke.selectedNode()
    createCustomShuffle('rgba', 'rgba', 'blue', 0, 0, 1)
    blueShuffle = nuke.selectedNode()

    # Set the input of the red shuffle node to the selected node, and transform the red shuffle node down to the left.
    redShuffle.setInput(0, selectedNode)
    redShuffle['xpos'].setValue(selectedNode_xPos - 150)
    redShuffle['ypos'].setValue(selectedNode_yPos + 150)

    # Set the input of the green shuffle node to the selected node, and transform the green shuffle node down.
    greenShuffle.setInput(0, selectedNode)
    greenShuffle['xpos'].setValue(selectedNode_xPos)
    greenShuffle['ypos'].setValue(selectedNode_yPos + 150)

    # Set the input of the blue shuffle node to the selected node, and transform the blue shuffle node down to the right.
    blueShuffle.setInput(0, selectedNode)
    blueShuffle['xpos'].setValue(selectedNode_xPos + 150)
    blueShuffle['ypos'].setValue(selectedNode_yPos + 150)

    # Lesson 04 Challenge. Create a merge node, connect B to green shuffle, A to red and blue shuffle.
    redShuffle.setSelected(True)
    greenShuffle.setSelected(True)
    blueShuffle.setSelected(True)

    g_pos_x = greenShuffle['xpos'].value()
    g_pos_y = greenShuffle['ypos'].value()


    myMerge = nuke.createNode('Merge2')
    myMerge.setInput(1, redShuffle)
    myMerge.setInput(0, greenShuffle)
    myMerge.setInput(3, blueShuffle)
    myMerge['xpos'].setValue(g_pos_x)
    myMerge['ypos'].setValue(g_pos_y + 150)

    myMerge['operation'].setValue('max')





# Add menu items to the Channel menu.
nuke.menu('Nodes').addCommand('Channel/Shuffle (Red to All)', 'shuffleShortcuts.createCustomShuffle("rgba", "rgba", "red", 1, 0, 0)', 'ctrl+alt+r', icon = 'redShuffle.png', shortcutContext = 2)
nuke.menu('Nodes').addCommand('Channel/Shuffle (Green to All)', 'shuffleShortcuts.createCustomShuffle("rgba", "rgba", "green", 0, 1, 0)', 'ctrl+alt+g', icon = 'greenShuffle.png', shortcutContext = 2)
nuke.menu('Nodes').addCommand('Channel/Shuffle (Blue to All)', 'shuffleShortcuts.createCustomShuffle("rgba", "rgba", "blue", 0, 0, 1)', 'ctrl+alt+b', icon = 'blueShuffle.png', shortcutContext = 2)
nuke.menu('Nodes').addCommand('Channel/Shuffle (Alpha to All)', 'shuffleShortcuts.createCustomShuffle("rgba", "rgba", "alpha", 1, 1, 1)', 'ctrl+alt+a', icon = 'alphaToAll.png', shortcutContext = 2)
nuke.menu('Nodes').addCommand('Channel/Shuffle (Alpha to 0)', 'shuffleShortcuts.createCustomShuffle("rgba", "rgba", "black", 0, 0, 0)', 'ctrl+alt+`', icon = 'alpha0Shuffle.png', shortcutContext = 2)
nuke.menu('Nodes').addCommand('Channel/Shuffle (Alpha to 1)', 'shuffleShortcuts.createCustomShuffle("rgba", "rgba", "white", 1, 1, 1)', 'ctrl+alt+1', icon = 'alpha1Shuffle.png', shortcutContext = 2)

nuke.menu('Nodes').addCommand('Channel/Shuffle (Split RGB Channel)', 'shuffleShortcuts.shuffleRGBchannel()', 'ctrl+alt+s', icon = 'ShuffleSplitRGB.png', shortcutContext = 2)
