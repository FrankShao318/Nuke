# ----------------------------------------------------------------------------
# readManagerUI.py
# Version: 1.0.0
# Author: Frank Shao

# Last Modified by: Frank Shao
# Last Updated: Sep. 27, 2020

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
import pyperclip
# pyperclip may cause nuke not open.
import readManagerCore


# Define the panel class.
class ReadManagerPanel(QtWidgets.QWidget):
    def __init__(self):
        super(ReadManagerPanel, self).__init__()

        self.setWindowTitle('Read Manager')
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.resize(500, 600)
        self.setMinimumSize(500, 600)

        # Signals and connections.
        # self.copy_list_info_button.clicked.connect(self.copy_reading_list)

        # Widgets
        # Top, center and copy button.
        self.center_selected_node_button = QtWidgets.QPushButton('Center Selected Node')
        self.copy_list_info_button = QtWidgets.QPushButton('Copy File List Info')
        # Bottom, label and file list.
        read_files_label = QtWidgets.QLabel('Read Files')
        self.read_files_list = readManagerCore.ReadManagerListTable()

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

        # Layout
        # Top, button layout.
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.center_selected_node_button)
        button_layout.addWidget(self.copy_list_info_button)
        # Bottom, list layout.
        list_layout = QtWidgets.QVBoxLayout()
        list_layout.addWidget(read_files_label)
        list_layout.addWidget(self.read_files_list)
        # Master layout.
        master_layout = QtWidgets.QVBoxLayout()
        master_layout.addLayout(button_layout)
        master_layout.addLayout(list_layout)

        self.setLayout(master_layout)
"""
    # Copy reading file list data.
    def copy_reading_list(self):
        print('copied')

        # Set row numbers.
        row_number = self.read_files_list.rowCount()
        if row_number > 0:
            for i in range(row_number):
                node_name = self.read_files_list.item(i, 0).text()
                file_name = self.read_files_list.item(i, 1).text()
                copy_items = node_name + ' => ' + file_name + '\n'
                pyperclip.copy(copy_items)
        else:
            nuke.message('There is nothing in Read Manager.')
"""


def start():
    start.panel = ReadManagerPanel()
    start.panel.show()


# Add item to menu.
nuke.menu('Nuke').addCommand('Frank Tool Dev/Read Manager', 'readManagerUI.start()')
