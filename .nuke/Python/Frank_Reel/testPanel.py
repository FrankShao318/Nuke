import sys
from PySide2 import QtWidgets
# from PySide2.QtWidgets import QWidget
import nuke


class Panel(QtWidgets.QWidget):
    def __init__(self):
        super(Panel, self).__init__()

        label = QtWidgets.QLabel('hello nuke!')
        label.setStyleSheet('background-color: cyan')
        label.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed))
        
        frame = QtWidgets.QFrame()
        frame.setFrameShape(QtWidgets.QFrame.HLine)
        
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(label)
        layout.addWidget(frame)
        
        self.setLayout(layout)


def start():
    start.panel = Panel()
    start.panel.show()


nuke.menu('Nuke').addCommand('Frank Tool Dev/Test Panel', 'testPanel.start()')


'''
app = QApplication(sys.argv)
panel = Panel()
panel.show()
app.exec_()
# Remove app and app.exec_() when pasting code in nuke or nuke will crush.
'''

