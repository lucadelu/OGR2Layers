# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_About.ui'
#
# Created: Sat Apr 10 00:50:35 2010
#      by: PyQt4 UI code generator 4.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_AboutDialog(object):
    def setupUi(self, AboutDialog):
        AboutDialog.setObjectName("AboutDialog")
        AboutDialog.resize(514, 370)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(AboutDialog.sizePolicy().hasHeightForWidth())
        AboutDialog.setSizePolicy(sizePolicy)
        self.verticalLayout_3 = QtGui.QVBoxLayout(AboutDialog)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.about = QtGui.QLabel(AboutDialog)
        self.about.setMinimumSize(QtCore.QSize(0, 25))
        self.about.setMaximumSize(QtCore.QSize(16777215, 25))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setWeight(75)
        font.setBold(True)
        self.about.setFont(font)
        self.about.setObjectName("about")
        self.verticalLayout.addWidget(self.about)
        self.logo = QtGui.QLabel(AboutDialog)
        self.logo.setObjectName("logo")
        self.verticalLayout.addWidget(self.logo)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.version = QtGui.QLabel(AboutDialog)
        self.version.setObjectName("version")
        self.horizontalLayout.addWidget(self.version)
        self.version_n = QtGui.QLabel(AboutDialog)
        self.version_n.setMaximumSize(QtCore.QSize(200, 16777215))
        self.version_n.setObjectName("version_n")
        self.horizontalLayout.addWidget(self.version_n)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.autors = QtGui.QLabel(AboutDialog)
        self.autors.setObjectName("autors")
        self.horizontalLayout_2.addWidget(self.autors)
        self.autors_name = QtGui.QLabel(AboutDialog)
        self.autors_name.setMaximumSize(QtCore.QSize(150, 16777215))
        self.autors_name.setObjectName("autors_name")
        self.horizontalLayout_2.addWidget(self.autors_name)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.textBrowser = QtGui.QTextBrowser(AboutDialog)
        self.textBrowser.setMaximumSize(QtCore.QSize(16777215, 60))
        self.textBrowser.setLineWidth(0)
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout.addWidget(self.textBrowser)
        self.horizontalLayout_3.addLayout(self.verticalLayout)
        self.line = QtGui.QFrame(AboutDialog)
        self.line.setFrameShape(QtGui.QFrame.VLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout_3.addWidget(self.line)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_help = QtGui.QLabel(AboutDialog)
        self.label_help.setMinimumSize(QtCore.QSize(0, 25))
        self.label_help.setMaximumSize(QtCore.QSize(16777215, 25))
        self.label_help.setObjectName("label_help")
        self.verticalLayout_2.addWidget(self.label_help)
        self.textBrowser_2 = QtGui.QTextBrowser(AboutDialog)
        font = QtGui.QFont()
        font.setWeight(50)
        font.setBold(False)
        self.textBrowser_2.setFont(font)
        self.textBrowser_2.setObjectName("textBrowser_2")
        self.verticalLayout_2.addWidget(self.textBrowser_2)
        self.horizontalLayout_3.addLayout(self.verticalLayout_2)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.buttonBox = QtGui.QDialogButtonBox(AboutDialog)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_3.addWidget(self.buttonBox)

        self.retranslateUi(AboutDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), AboutDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(AboutDialog)

    def retranslateUi(self, AboutDialog):
        AboutDialog.setWindowTitle(QtGui.QApplication.translate("AboutDialog", "OGR2Layers Plugin: Info", None, QtGui.QApplication.UnicodeUTF8))
        self.about.setText(QtGui.QApplication.translate("AboutDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:12pt; font-weight:600; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">About</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.logo.setText(QtGui.QApplication.translate("AboutDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><img src=\":/plugins/OGR2Layers/icongui.png\" /></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.version.setText(QtGui.QApplication.translate("AboutDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600;\">Version:</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.autors.setText(QtGui.QApplication.translate("AboutDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600;\">Authors:</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.autors_name.setText(QtGui.QApplication.translate("AboutDialog", "Nicolas Bozon, \n"
"Rene-Luc D\'Hont, \n"
"Michael Douchin, \n"
"Mathias Walker, \n"
"Luca Delucchi", None, QtGui.QApplication.UnicodeUTF8))
        self.textBrowser.setHtml(QtGui.QApplication.translate("AboutDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">More info</p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">http://wiki.github.com/lucadelu/OGR2Layers/</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_help.setText(QtGui.QApplication.translate("AboutDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600;\">How to use</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.textBrowser_2.setHtml(QtGui.QApplication.translate("AboutDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">OGR2Layer create a html page with OpenLayers library to show on the web your vector data loaded on QGIS. You can choose a background layer, some controls, you can render data using QGIS symbology and you can add query on your layer.</span></p>\n"
"<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:10pt;\"></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">First you must </span><span style=\" font-size:10pt; font-weight:600;\">add the definition for the projection of Spherical Mercator to your proj.4 data directories</span><span style=\" font-size:10pt;\"> (on linux /usr/share/proj/epsg), this is necessary for usign OpenStreetMap background; you must add only the line:</span></p>\n"
"<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:10pt;\"></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Courier New, courier\';\">&lt;900913&gt; +proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +no_defs</span></p>\n"
"<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">The second important part is </span><span style=\" font-size:10pt; font-weight:600;\">your vector layer has a  known spatial reference system</span><span style=\" font-size:10pt;\"> (e.g. file .prj for shapefile) then you can load vector data and start OGR2Layer plugin, now  you choose the directory where the plugin save the files (.html for internet page and gml for vector data) and several option to add in OpenLayers.</span></p>\n"
"<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:10pt;\"></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">For use the \"</span><span style=\" font-size:10pt; font-style:italic;\">QGIS Render</span><span style=\" font-size:10pt;\">\" in the \"</span><span style=\" font-size:10pt; font-style:italic;\">Render option</span><span style=\" font-size:10pt;\">\" remember  that work only \"</span><span style=\" font-size:10pt; font-style:italic;\">Single Symbol</span><span style=\" font-size:10pt;\">\" and \"</span><span style=\" font-size:10pt; font-style:italic;\">Unique Value</span><span style=\" font-size:10pt;\">\" symbology</span></p>\n"
"<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:10pt;\"></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">In the \"</span><span style=\" font-size:10pt; font-style:italic;\">Query Options</span><span style=\" font-size:10pt;\">\" the option \"</span><span style=\" font-size:10pt; font-style:italic;\">query more features</span><span style=\" font-size:10pt;\">\" use OpenLayers Strategy Cluster, this solution allow to cluster more features and query the group, it\'s useful for points specially when they are very neighbouring. </span></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt; font-weight:600;\">Important</span><span style=\" font-size:10pt;\">: remember \"</span><span style=\" font-size:10pt; font-style:italic;\">query more features</span><span style=\" font-size:10pt;\">\" doesn\'t work with \"</span><span style=\" font-size:10pt; font-style:italic;\">Unique Value</span><span style=\" font-size:10pt;\">\" symbology</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))

import resources_rc
