# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_About.ui'
#
# Created: Tue Dec 10 10:38:57 2013
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_AboutDialog(object):
    def setupUi(self, AboutDialog):
        AboutDialog.setObjectName(_fromUtf8("AboutDialog"))
        AboutDialog.resize(629, 418)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(AboutDialog.sizePolicy().hasHeightForWidth())
        AboutDialog.setSizePolicy(sizePolicy)
        self.gridLayout = QtGui.QGridLayout(AboutDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.about = QtGui.QLabel(AboutDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.about.sizePolicy().hasHeightForWidth())
        self.about.setSizePolicy(sizePolicy)
        self.about.setMinimumSize(QtCore.QSize(91, 25))
        self.about.setMaximumSize(QtCore.QSize(91, 25))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.about.setFont(font)
        self.about.setObjectName(_fromUtf8("about"))
        self.horizontalLayout_3.addWidget(self.about)
        self.logo = QtGui.QLabel(AboutDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.logo.sizePolicy().hasHeightForWidth())
        self.logo.setSizePolicy(sizePolicy)
        self.logo.setMinimumSize(QtCore.QSize(70, 79))
        self.logo.setMaximumSize(QtCore.QSize(70, 79))
        self.logo.setObjectName(_fromUtf8("logo"))
        self.horizontalLayout_3.addWidget(self.logo)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.version = QtGui.QLabel(AboutDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.version.sizePolicy().hasHeightForWidth())
        self.version.setSizePolicy(sizePolicy)
        self.version.setMinimumSize(QtCore.QSize(72, 19))
        self.version.setMaximumSize(QtCore.QSize(72, 19))
        self.version.setAlignment(QtCore.Qt.AlignCenter)
        self.version.setMargin(0)
        self.version.setObjectName(_fromUtf8("version"))
        self.horizontalLayout.addWidget(self.version)
        self.version_n = QtGui.QLabel(AboutDialog)
        self.version_n.setMaximumSize(QtCore.QSize(136, 89))
        self.version_n.setText(_fromUtf8(""))
        self.version_n.setObjectName(_fromUtf8("version_n"))
        self.horizontalLayout.addWidget(self.version_n)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.autors = QtGui.QLabel(AboutDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.autors.sizePolicy().hasHeightForWidth())
        self.autors.setSizePolicy(sizePolicy)
        self.autors.setMinimumSize(QtCore.QSize(77, 19))
        self.autors.setMaximumSize(QtCore.QSize(77, 19))
        self.autors.setObjectName(_fromUtf8("autors"))
        self.horizontalLayout_2.addWidget(self.autors)
        self.autors_name = QtGui.QLabel(AboutDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.autors_name.sizePolicy().hasHeightForWidth())
        self.autors_name.setSizePolicy(sizePolicy)
        self.autors_name.setMinimumSize(QtCore.QSize(136, 89))
        self.autors_name.setMaximumSize(QtCore.QSize(136, 89))
        self.autors_name.setObjectName(_fromUtf8("autors_name"))
        self.horizontalLayout_2.addWidget(self.autors_name)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.textBrowser_3 = QtGui.QTextBrowser(AboutDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textBrowser_3.sizePolicy().hasHeightForWidth())
        self.textBrowser_3.setSizePolicy(sizePolicy)
        self.textBrowser_3.setMinimumSize(QtCore.QSize(263, 121))
        self.textBrowser_3.setMaximumSize(QtCore.QSize(261, 121))
        self.textBrowser_3.setObjectName(_fromUtf8("textBrowser_3"))
        self.verticalLayout.addWidget(self.textBrowser_3)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.label_help = QtGui.QLabel(AboutDialog)
        self.label_help.setMinimumSize(QtCore.QSize(0, 25))
        self.label_help.setMaximumSize(QtCore.QSize(16777215, 25))
        self.label_help.setObjectName(_fromUtf8("label_help"))
        self.verticalLayout_2.addWidget(self.label_help)
        self.textBrowser_2 = QtGui.QTextBrowser(AboutDialog)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.textBrowser_2.setFont(font)
        self.textBrowser_2.setObjectName(_fromUtf8("textBrowser_2"))
        self.verticalLayout_2.addWidget(self.textBrowser_2)
        self.buttonBox = QtGui.QDialogButtonBox(AboutDialog)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout_2.addWidget(self.buttonBox)
        self.gridLayout.addLayout(self.verticalLayout_2, 0, 1, 1, 1)

        self.retranslateUi(AboutDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), AboutDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(AboutDialog)

    def retranslateUi(self, AboutDialog):
        AboutDialog.setWindowTitle(QtGui.QApplication.translate("AboutDialog", "OGR2Layers Plugin: Info", None, QtGui.QApplication.UnicodeUTF8))
        self.about.setText(QtGui.QApplication.translate("AboutDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:12pt; font-weight:600; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:20pt;\">About</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
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
        self.textBrowser_3.setHtml(QtGui.QApplication.translate("AboutDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'DejaVu Sans\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Sans Serif\';\">More info</span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a href=\"http://wiki.github.com/lucadelu/OGR2Layers/ \"><span style=\" font-family:\'Sans Serif\'; font-weight:600; text-decoration: underline; color:#0000ff;\">http://wiki.github.com/lucadelu/OGR2Layers/</span></a></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Sans Serif\'; font-weight:600; text-decoration: underline; color:#0000ff;\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Sans Serif\';\">You can add an issue or a bug</span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a href=\"http://hub.qgis.org/projects/ogr2layers\"><span style=\" font-family:\'Sans Serif\'; font-weight:600; text-decoration: underline; color:#0000ff;\">http://hub.qgis.org/projects/ogr2layers</span></a></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_help.setText(QtGui.QApplication.translate("AboutDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600;\">How to use</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.textBrowser_2.setHtml(QtGui.QApplication.translate("AboutDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'DejaVu Sans\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Sans Serif\'; font-size:10pt;\">OGR2Layer create a html page with OpenLayers library to show on the web your vector data loaded on QGIS. You can choose a background layer, some controls, you can render data using QGIS symbology and you can add query on your layer.</span></p>\n"
"<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Sans Serif\'; font-size:10pt;\"><br /></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Sans Serif\'; font-size:10pt;\">From </span><span style=\" font-family:\'Sans Serif\'; font-size:10pt; font-weight:600;\">0.7 version it work with python-gdal</span><span style=\" font-family:\'Sans Serif\'; font-size:10pt;\"> to convert vector data, </span><a name=\"result_box\"></a><span style=\" font-family:\'Sans Serif\'; background-color:#ffffff;\">y</span><span style=\" font-family:\'Sans Serif\'; background-color:#ffffff;\">ou should check its installation</span></p>\n"
"<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Sans Serif\'; font-size:10pt;\"><br /></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Sans Serif\'; font-size:10pt;\">First you must </span><span style=\" font-family:\'Sans Serif\'; font-size:10pt; font-weight:600;\">add the definition for the projection of Spherical Mercator to your proj.4 data directories</span><span style=\" font-family:\'Sans Serif\'; font-size:10pt;\"> (on linux /usr/share/proj/epsg), this is necessary for usign OpenStreetMap background; you must add only the line:</span></p>\n"
"<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Sans Serif\'; font-size:10pt;\"><br /></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Courier New, courier\';\">&lt;900913&gt; +proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +no_defs</span></p>\n"
"<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Sans Serif\';\"><br /></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Sans Serif\'; font-size:10pt;\">The second important part is </span><span style=\" font-family:\'Sans Serif\'; font-size:10pt; font-weight:600;\">your vector layer has a  known spatial reference system</span><span style=\" font-family:\'Sans Serif\'; font-size:10pt;\"> (e.g. file .prj for shapefile) then you can load vector data and start OGR2Layer plugin, now  you choose the directory where the plugin save the files (.html for internet page and gml for vector data) and several option to add in OpenLayers.</span></p>\n"
"<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Sans Serif\'; font-size:10pt;\"><br /></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Sans Serif\'; font-size:10pt;\">From </span><span style=\" font-family:\'Sans Serif\'; font-size:10pt; font-weight:600;\">version 0.8.0</span><span style=\" font-family:\'Sans Serif\'; font-size:10pt;\"> &quot;</span><span style=\" font-family:\'Sans Serif\'; font-size:10pt; font-style:italic;\">QGIS Render</span><span style=\" font-family:\'Sans Serif\'; font-size:10pt;\">&quot; in the &quot;</span><span style=\" font-family:\'Sans Serif\'; font-size:10pt; font-style:italic;\">Render option</span><span style=\" font-family:\'Sans Serif\'; font-size:10pt;\">&quot; supports all symbologies of &quot;</span><span style=\" font-family:\'Sans Serif\'; font-size:10pt; font-style:italic;\">Old symbology Style</span><span style=\" font-family:\'Sans Serif\'; font-size:10pt;\">&quot;</span></p>\n"
"<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Sans Serif\'; font-size:10pt;\"><br /></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Sans Serif\'; font-size:10pt;\">From </span><span style=\" font-family:\'Sans Serif\'; font-size:10pt; font-weight:600;\">version 0.8.1</span><span style=\" font-family:\'Sans Serif\'; font-size:10pt;\"> it supports also the QGIS svg symbols for &quot;</span><span style=\" font-family:\'Sans Serif\'; font-size:10pt; font-style:italic;\">Single Symbol</span><span style=\" font-family:\'Sans Serif\'; font-size:10pt;\">&quot; and &quot;</span><span style=\" font-family:\'Sans Serif\'; font-size:10pt; font-style:italic;\">Unique Value</span><span style=\" font-family:\'Sans Serif\'; font-size:10pt;\">&quot;, using &quot;</span><span style=\" font-family:\'Sans Serif\'; font-size:10pt; font-style:italic;\">Old symbology</span><span style=\" font-family:\'Sans Serif\'; font-size:10pt;\">&quot;. </span></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Sans Serif\'; font-size:10pt; font-weight:600;\">Important</span><span style=\" font-family:\'Sans Serif\'; font-size:10pt;\">: Only svg icons can be used.</span></p>\n"
"<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Sans Serif\'; font-size:10pt;\"><br /></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Sans Serif\'; font-size:10pt;\">From </span><span style=\" font-family:\'Sans Serif\'; font-size:10pt; font-weight:600;\">version 0.8.4</span><span style=\" font-family:\'Sans Serif\'; font-size:10pt;\"> it supports the &quot;</span><span style=\" font-family:\'Sans Serif\'; font-size:10pt; font-style:italic;\">New Symbology</span><span style=\" font-family:\'Sans Serif\'; font-size:10pt;\">&quot;, it is possible to use only simple simbology for &quot;</span><span style=\" font-family:\'Sans Serif\'; font-size:10pt; font-style:italic;\">Single Symbol</span><span style=\" font-family:\'Sans Serif\'; font-size:10pt;\">&quot;, &quot;</span><span style=\" font-family:\'Sans Serif\'; font-size:10pt; font-style:italic;\">Catagorized</span><span style=\" font-family:\'Sans Serif\'; font-size:10pt;\">&quot;, &quot;</span><span style=\" font-family:\'Sans Serif\'; font-size:10pt; font-style:italic;\">Graduated</span><span style=\" font-family:\'Sans Serif\'; font-size:10pt;\">&quot;. </span></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Sans Serif\'; font-size:10pt; font-weight:600;\">Warning</span><span style=\" font-family:\'Sans Serif\'; font-size:10pt;\">: The svg icons are not supported yet</span></p>\n"
"<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Sans Serif\'; font-size:10pt;\"><br /></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Sans Serif\'; font-size:10pt;\">In the &quot;</span><span style=\" font-family:\'Sans Serif\'; font-size:10pt; font-style:italic;\">Query Options</span><span style=\" font-family:\'Sans Serif\'; font-size:10pt;\">&quot; the option &quot;</span><span style=\" font-family:\'Sans Serif\'; font-size:10pt; font-style:italic;\">query more features</span><span style=\" font-family:\'Sans Serif\'; font-size:10pt;\">&quot; use OpenLayers Strategy Cluster, this solution allow to cluster more point features and query the group, it\'s useful when points are very neighbouring.</span></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Sans Serif\'; font-size:10pt; font-weight:600;\">Important</span><span style=\" font-family:\'Sans Serif\'; font-size:10pt;\">: remember &quot;</span><span style=\" font-family:\'Sans Serif\'; font-size:10pt; font-style:italic;\">query more features</span><span style=\" font-family:\'Sans Serif\'; font-size:10pt;\">&quot; doesn\'t work with &quot;</span><span style=\" font-family:\'Sans Serif\'; font-size:10pt; font-style:italic;\">Unique Value</span><span style=\" font-family:\'Sans Serif\'; font-size:10pt;\">&quot; symbology</span></p>\n"
"<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Sans Serif\'; font-size:10pt;\"><br /></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Sans Serif\'; font-size:10pt;\">From </span><span style=\" font-family:\'Sans Serif\'; font-size:10pt; font-weight:600;\">version 0.9.0</span><span style=\" font-family:\'Sans Serif\'; font-size:10pt;\"> there is </span><span style=\" font-family:\'Sans Serif\'; font-size:10pt; font-style:italic;\">support for WMS</span><span style=\" font-family:\'Sans Serif\'; font-size:10pt;\">, they must be in the same coordinate system of base layer. For example if OpenStreetMap is the base layer your WMS should accept EPSG code 3857 or 900913.</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))

import resources_rc
