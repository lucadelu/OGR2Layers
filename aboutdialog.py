from PyQt4 import QtCore, QtGui 
from ui_About import Ui_AboutDialog

#create dialog for about/help window
class OGR2LayersAboutDialog(QtGui.QDialog): 
  def __init__(self): 
    QtGui.QDialog.__init__(self) 
    # Set up the user interface from Designer. 
    self.uiAbout = Ui_AboutDialog() 
    self.uiAbout.setupUi(self) 