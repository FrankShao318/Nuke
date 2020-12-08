# ----------------------------------------------------------------------------
# readManagerUI_01.py
# Version: 1.1.0
# Author: Frank Shao

# Last Modified by: Frank Shao
# Last Updated: Oct. 3, 2020

# Usage:
# - List all files being read into a nuke script, images, cameras and geos etc.
# - Make users be able to copy and paste file list to clipboard.
# - Hit center button to bring the node to the center of node graph.
# ----------------------------------------------------------------------------

from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2 import QtWidgets
import nuke
import os
import readManagerCore
import subprocess


# Define the panel class.
class ReadManagerPanel(QtWidgets.QWidget):
    
    def __init__(self):
        super(ReadManagerPanel, self).__init__()
        
        # Default window settings.
        self.setWindowTitle('Read Manager')
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.resize(600, 600)
        self.setMinimumSize(600, 600)

        # Widgets
        # Top, script info.
        script_name_label = QtWidgets.QLabel('Script Name:')
        script_name_label.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed))
        
        script_name = QtWidgets.QLabel(self.get_script_name())
        script_name.setAlignment(Qt.AlignLeft)

        script_location = QtWidgets.QLabel('Location:')
        script_location.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed))
        
        script_file_path = QtWidgets.QLabel(self.get_script_location())
        script_file_path.setAlignment(Qt.AlignLeft)

        # Bottom, label, buttons and file list.
        # Label
        read_files_label = QtWidgets.QLabel('Read Files:')
        read_files_label.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed))
        # Buttons
        self.center_selected_node_button = QtWidgets.QPushButton('Center Selected Node')
        self.copy_list_info_button = QtWidgets.QPushButton('Copy File List Info')
        # File List
        self.read_files_list = readManagerCore.ReadManagerListTable()

        # Layout
        # Group box.
        script_group_box = QtWidgets.QGroupBox()
        file_group_box = QtWidgets.QGroupBox()

        # Top, script info.
        top_top_label_layout = QtWidgets.QHBoxLayout()
        top_top_label_layout.addWidget(script_name_label)
        top_top_label_layout.addWidget(script_name)
        top_bottom_label_layout = QtWidgets.QHBoxLayout()
        top_bottom_label_layout.addWidget(script_location)
        top_bottom_label_layout.addWidget(script_file_path)
        top_layout = QtWidgets.QVBoxLayout()
        top_layout.addLayout(top_top_label_layout)
        top_layout.addLayout(top_bottom_label_layout)
        script_group_box.setLayout(top_layout)

        # Bottom, label, buttons and file list.
        # Buttons layout.
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.center_selected_node_button)
        button_layout.addWidget(self.copy_list_info_button)
        # Bottom layout.
        bottom_layout = QtWidgets.QVBoxLayout()
        bottom_layout.addWidget(read_files_label)
        bottom_layout.addLayout(button_layout)
        bottom_layout.addWidget(self.read_files_list)
        file_group_box.setLayout(bottom_layout)

        # Master layout.
        master_layout = QtWidgets.QVBoxLayout()
        master_layout.addWidget(script_group_box)
        master_layout.addWidget(file_group_box)

        self.setLayout(master_layout)
        
        # Init functions.
        self.generate_data_table()
        self.signal_connection()
        
    def get_script_name(self):
        return os.path.basename(nuke.root()['name'].value())
    
    def get_script_location(self):
        file_path = nuke.root()['name'].value()
        return os.path.split(file_path)[0]
        
    def generate_data_table(self):
        # Create specific node class list.
        node_classes = ['Read', 'ReadGeo', 'Camera', 'Camera2']
        # Create node list and node name list.
        node_list = []
        node_name_list = []
        node_file_list = []
        # Add node and node name to lists.
        for i in nuke.allNodes():
            for x in node_classes:
                if i.knob('file') and i.Class() == x:
                    node_list.append(i)
                    node_name_list.append(i.name())
        # Get file info.
        for node in node_list:
            filepath = node['file'].value()
            filename = os.path.basename(filepath)
            node_file_list.append(filename)
    
        final_list = []
        for i in range(len(node_name_list)):
            final_list.append((node_name_list[i], node_file_list[i]))
        # [(node_name, node_file), (node_name, node_file)......]
        self.read_files_list.add_items(final_list)
        
    def signal_connection(self):
        
        # Signals and connections.
        self.center_selected_node_button.clicked.connect(self.center_selected_node)
        self.copy_list_info_button.clicked.connect(self.copy_reading_list)
        
    def center_selected_node(self):
        selected_cell = QtWidgets.QTableWidget.selectedItems(self.read_files_list)
        selected_cell_text = selected_cell[0].text()
        selected_node = nuke.toNode(selected_cell_text)
        if selected_node != None:
            nuke.zoom(2, [float(selected_node.xpos()), float(selected_node.ypos())])
        else:
            nuke.message('Please select a NODE name.')
        
    def copy_reading_list(self):
        # Set row numbers.
        row_number = self.read_files_list.rowCount()
        
        if row_number > 0:
            # Add table data to a list.
            copy_items_list = []
            for i in range(row_number):
                node_name = self.read_files_list.item(i, 0).text()
                file_name = self.read_files_list.item(i, 1).text()
                copy_item = node_name + ' => ' + file_name
                copy_items_list.append(copy_item)
                
            # Make a single string from table data list.
            single_list = '\n'.join(copy_items_list)
            
            # Send single string to clipboard.
            # This is Mac version. Win and Linux may need to modify the command.
            copy_to_clipboard = subprocess.Popen('pbcopy', env={'LANG': 'en_US.UTF-8'}, stdin=subprocess.PIPE)
            copy_to_clipboard.communicate(single_list.encode())
        else:
            nuke.message('There is nothing in Read Manager.')
        
        
def start():
    start.panel = ReadManagerPanel()
    start.panel.show()


# Add item to menu.
nuke.menu('Nuke').addCommand('Frank Tool Dev/Read Manager 01', 'readManagerUI_01.start()')
