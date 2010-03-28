from PyQt4 import QtCore, QtGui 
from ui_OGR2Layers import Ui_OGR2Layers

class OGR2LayersDialog(QtGui.QDialog): 
  def __init__(self): 
    QtGui.QDialog.__init__(self) 
    # Set up the user interface from Designer. 
    self.ui = Ui_OGR2Layers() 
    self.ui.setupUi(self) 