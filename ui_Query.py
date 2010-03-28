# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_Query.ui'
#
# Created: Mon Mar 22 18:58:00 2010
#      by: PyQt4 UI code generator 4.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_QueryDialog(object):
    def setupUi(self, QueryDialog):
        QueryDialog.setObjectName("QueryDialog")
        QueryDialog.resize(470, 303)
        QueryDialog.setMinimumSize(QtCore.QSize(470, 0))
        self.verticalLayout = QtGui.QVBoxLayout(QueryDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.buttonBox = QtGui.QDialogButtonBox(QueryDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(QueryDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), QueryDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(QueryDialog)

    def retranslateUi(self, QueryDialog):
        QueryDialog.setWindowTitle(QtGui.QApplication.translate("QueryDialog", "OGR2Layers Plugin: Query options", None, QtGui.QApplication.UnicodeUTF8))

