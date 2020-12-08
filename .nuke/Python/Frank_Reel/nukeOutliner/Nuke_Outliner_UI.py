from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile
from PySide2 import QtWidgets
import nuke
import os
import subprocess


current_module_path = os.path.abspath(os.path.dirname(__file__))
ui_file = current_module_path + '/Nuke_Outliner.ui'


# Nuke Outliner: Add some tool widgets to manage the script information.
class NukeOutliner(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super(NukeOutliner, self).__init__(parent)

        loader = QUiLoader()
        uifile = QFile(ui_file)
        if uifile.open(QFile.ReadOnly):
            self.window = loader.load(uifile, parent)
            uifile.close()
            self.setCentralWidget(self.window)
            self.show()
            # Print out all widgets in ui.
            """
            for i in dir(self.window):
                print(i)
            """
            # set script info label text
            self.window.scriptNameValue_QLabel.setText(os.path.basename(nuke.root()['name'].value()))
            file_path = nuke.root()['name'].value()
            self.window.scriptLocationValue_QLabel.setText(os.path.split(file_path)[0])
                        
            # Add read files data table to Read Files Info tab.
            self.generate_data_table()
            self.signal_connection()
            
    # Generate read files data table.
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
        # [(node_name, node_file), (node_name, node_file)...]
        
        # add to table view
        row_numbers = len(final_list)
        self.window.readFilesTable_QTableWidget.setRowCount(row_numbers)
        # Create and add table widget items.
        for i in range(row_numbers):
            name_item = QtWidgets.QTableWidgetItem(final_list[i][0])
            file_item = QtWidgets.QTableWidgetItem(final_list[i][1])
            self.window.readFilesTable_QTableWidget.setItem(i, 0, name_item)
            self.window.readFilesTable_QTableWidget.setItem(i, 1, file_item)
            
    def signal_connection(self):
        # Signal and connections.
        self.window.readFiles_centerSelectedNode_QPushButton.clicked.connect(self.read_files_center_selected_node)
        self.window.copyReadFilesInfo_QPushButton.clicked.connect(self.copy_read_files_info)
    
    def read_files_center_selected_node(self):
        selected_cell = QtWidgets.QTableWidget.selectedItems(self.window.readFilesTable_QTableWidget)
        selected_cell_text = selected_cell[0].text()
        selected_node = nuke.toNode(selected_cell_text)
        if selected_node != None:
            nuke.zoom(2, [float(selected_node.xpos()), float(selected_node.ypos())])
        else:
            nuke.message('Please select a NODE name.')
    
    def copy_read_files_info(self):
        # Set row numbers.
        row_number = self.window.readFilesTable_QTableWidget.rowCount()
        
        if row_number > 0:
            # Add table data to a list.
            copy_items_list = []
            for i in range(row_number):
                node_name = self.window.readFilesTable_QTableWidget.item(i, 0).text()
                file_name = self.window.readFilesTable_QTableWidget.item(i, 1).text()
                copy_item = node_name + ' => ' + file_name
                copy_items_list.append(copy_item)
              
            # Make a single string from table data list.
            single_string_data = '\n'.join(copy_items_list)
           
            # Send single string to clipboard.
            # This is Mac version. Win and Linux may need to modify the command.
            copy_to_clipboard = subprocess.Popen('pbcopy', env={'LANG': 'en_US.UTF-8'}, stdin=subprocess.PIPE)
            copy_to_clipboard.communicate(single_string_data.encode())
        else:
            nuke.message('There is nothing in Read Files Info table.')
 
           
def start():
    start.window = NukeOutliner()
    start.window.show()


# Add item to menu.
nuke.menu('Nuke').addCommand('Frank Tool Dev/Nuke Outliner', 'Nuke_Outliner_UI.start()')


"""
if __name__ == '__main__':
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    app = QApplication(sys.argv)
    mywindow = NukeOutliner()
    sys.exit(app.exec_())
"""

"""
Error:
    Qt WebEngine seems to be initialized from a plugin.
    Please set Qt::AA_ShareOpenGLContexts using QCoreApplication::setAttribute before constructing QGuiApplication.
    can be fixed by adding the line below.
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
"""
