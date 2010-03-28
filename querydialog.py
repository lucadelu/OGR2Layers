from PyQt4 import QtCore, QtGui 
from ui_Query import Ui_QueryDialog

class OGR2LayersQueryDialog(QtGui.QDialog): 
  def __init__(self): 
    QtGui.QDialog.__init__(self) 
    # Set up the user interface from Designer. 
    self.uiQuery = Ui_QueryDialog() 
    self.uiQuery.setupUi(self) 