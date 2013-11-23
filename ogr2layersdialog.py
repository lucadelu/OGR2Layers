from PyQt4 import QtGui
import platform


class OGR2LayersDialog(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        if platform.system() == 'Darwin':
            from ui_OGR2Layers_mac import Ui_OGR2Layers
            self.ui = Ui_OGR2Layers()
            self.ui.setupUi(self)
        else:
            from ui_OGR2Layers import Ui_OGR2Layers
            self.ui = Ui_OGR2Layers()
            self.ui.setupUi(self)
