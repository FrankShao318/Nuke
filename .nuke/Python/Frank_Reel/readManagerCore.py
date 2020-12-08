# ----------------------------------------------------------------------------
# readManagerCore.py
# Version: 1.1.0
# Author: Frank Shao

# Last Modified by: Frank Shao
# Last Updated: Oct. 3, 2020

# Usage:
# - List all files being read into a nuke script, images, cameras and geos etc.
# - Make users be able to copy and paste file list to clipboard.
# - Hit center button to bring the node to the center of node graph.
# ----------------------------------------------------------------------------

import nuke
import os
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2 import QtWidgets


# Define the list table class.
class ReadManagerListTable(QtWidgets.QTableWidget):
    def __init__(self):
        super(ReadManagerListTable, self).__init__()

        self.setColumnCount(2)
        self.setHorizontalHeaderItem(0, QtWidgets.QTableWidgetItem('Node Name'))
        self.setHorizontalHeaderItem(1, QtWidgets.QTableWidgetItem('File'))
        self.horizontalHeader().setStretchLastSection(True)
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)

    # Add item to table.
    def add_items(self, final_list):
        # Set row numbers.
        row_numbers = len(final_list)
        self.setRowCount(row_numbers)
        # Create and add table widget items.
        for i in range(row_numbers):
            name_item = QtWidgets.QTableWidgetItem(final_list[i][0])
            file_item = QtWidgets.QTableWidgetItem(final_list[i][1])
            self.setItem(i, 0, name_item)
            self.setItem(i, 1, file_item)
