#############################################
#       OGR2Layers Plugin (c)  for Quantum GIS                                  #
#       (c) Copyright Nicolas BOZON - 2008                                      #
#       Authors: Nicolas BOZON, Rene-Luc D'HONT, Michael DOUCHIN, Luca DELUCCHI #
#       Email: lucadeluge at gmail dot com                                      #
#                                                                               #
#############################################
#       OGR2Layers Plugin is licensed under the terms of GNU GPL 2              #
#       This program is free software; you can redistribute it and/or modify    #
#       it under the terms of the GNU General Public License as published by    #
#       the Free Software Foundation; either version 2 of the License, or       #
#       (at your option) any later version.                                     #
#       This program is distributed in the hope that it will be useful,         #
#       but WITHOUT ANY WARRANTY; without even implied warranty of              #
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.                    # 
#       See the GNU General Public License for more details.                    #
#############################################
# OL == OpenLayers
# OSM == OpenStreetMap


# Python, PyQt and QGIS imports
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *

#import system class
import sys
import os
import resources_rc

# import dialog of other window
from ogr2layersdialog import OGR2LayersDialog
from aboutdialog import OGR2LayersAboutDialog
# for next version
from querydialog import OGR2LayersQueryDialog

#import function from other files
from OGR2ClassLayer import *
from OGR2ClassQuery import OGR2LayersClassControlSel
from OGR2ClassHtml import *

import __init__

class OGR2Layers:
    MSG_BOX_TITLE = "OGR2Layers Plugin Warning"

    def __init__(self, iface):
        self.iface = iface

    #plugin is loaded
    def initGui(self):
        #loaded icon
        self.action = QAction(QIcon(":/plugins/OGR2Layers/ogr2layersicon.png"),
        "OGR2Layers", self.iface.mainWindow())
        self.action.setWhatsThis("Configuration for OGR2Layers plugin")
        QObject.connect(self.action, SIGNAL("triggered()"), self.run)
        # first check if Web menu availbale in this QGIS version
        if hasattr(self.iface, "addPluginToWebMenu"):
            #add plugin to the web plugin menu
            self.iface.addPluginToWebMenu( "&OGR2Layers Plugin...", self.action)
            # and add button to the Web panel
            self.iface.addWebToolBarIcon( self.action)
        else:
            #add icon to the toolbar
            self.iface.addToolBarIcon(self.action)
            #add plugin to the plugin menu
            self.iface.addPluginToMenu("&OGR2Layers Plugin...", self.action)

    #Plugin disjunction
    def unload(self):
        # first check if Web menu availbale in this QGIS version
        if hasattr(self.iface, "addPluginToWebMenu"):
            # new menu used, remove submenus from main Web menu
            self.iface.removePluginWebMenu("&OGR2Layers Plugin...", self.action)
            # also remove button from Web toolbar
            self.iface.removeWebToolBarIcon(self.action)
        else:
            #remove plugin
            self.iface.removePluginMenu("&OGR2Layers Plugin...",self.action)
            #remove icon
            self.iface.removeToolBarIcon(self.action)

    #Plugin run
    def run(self):
        #set the dialog windows
        self.dlg = OGR2LayersDialog()
        #select directory where save files
        QObject.connect(self.dlg.ui.browseButton, SIGNAL("clicked()"), self.SelectKmlDir) 
        #function for open about dialog
        QObject.connect(self.dlg.ui.helpButton, SIGNAL("clicked()"), self.helpAbout) 
        #function for open query dialog in next version
        #QObject.connect(self.dlg.ui.queryButton, SIGNAL("clicked()"), self.showQuery) 

        #load layer
        layers =  self.iface.activeLayer()
        #Checks for loaded layers, do not load if no layers
        if layers == None:
            QMessageBox.warning(self.iface.mainWindow(), self.MSG_BOX_TITLE, 
            ("No active layer found\n" "Please make one or more OGR layer "\
            "active\n" "Beware of layers sizes for export"), QMessageBox.Ok, 
            QMessageBox.Ok)
            return
        #OGR layers 
        self.layers = [] 
        #GDAL layers
        self.rasters = []
        #load qgis mapCanvas
        self.mapCanvas = self.iface.mapCanvas()
        #Checks vector type and populates the layer list view in opposite 
        #order for the correct visualization on OL
        for i in range(self.mapCanvas.layerCount()-1,-1,-1):
            # define actual layer
            layer = self.mapCanvas.layer(i)
            #check if is a vector
            if layer.type() == layer.VectorLayer:
                self.layers.append(layer)
                #this is for remove "layerid=*" when use "Unique Value" symbology
                source=layer.source()
                source.remove(QRegExp('\|layerid=[\d]+$'))
                self.dlg.ui.LayerList.addItem(source)
            if layer.type() == layer.RasterLayer:
                self.rasters.append(layer)
                #this is for remove "layerid=*" when use "Unique Value" symbology
                source=layer.source()
                source.remove(QRegExp('\|layerid=[\d]+$'))
                self.dlg.ui.RasterList.addItem(source)              
        #check if there is some vectors layer, else return an error
        #if len(self.layers) == 0:
            #QMessageBox.warning(self.iface.mainWindow(), self.MSG_BOX_TITLE, 
            #("No vector layer found\n" "Please load one or more OGR layer\n"), 
            #QMessageBox.Ok, QMessageBox.Ok)
            #return
        #button for start the plugin
        QObject.connect(self.dlg.ui.buttonBox, SIGNAL("accepted()"), self.WriteKML)
        #button for close the plugin after create openlayers file
        QObject.connect(self.dlg.ui.buttonBox, SIGNAL("rejected()"), self.dlg.close)
        #Set up the default map extent
        Extent = self.mapCanvas.extent()
        if len(self.layers) != 0:
            mylayer = self.layers[0]
            myprovider = mylayer.dataProvider()
        elif len(self.rasters) != 0:
            mylayer = self.rasters[0]
            myprovider = mylayer.dataProvider()
        else:
            QMessageBox.warning(self.iface.mainWindow(), self.MSG_BOX_TITLE, 
            ("No active layer found\n" "Please make one or more OGR layer "\
            "active\n" "Beware of layers sizes for export"), QMessageBox.Ok, 
            QMessageBox.Ok)
            return
        #set coordinate system of my first vector
        SrsSrc = myprovider.crs()
        #set wgs84 coordinate system
        SrsDest = QgsCoordinateReferenceSystem(4326)
        #set qgis transformation
        xform = QgsCoordinateTransform(SrsSrc,SrsDest)
        minPt = xform.transform(QgsPoint(Extent.xMinimum(),Extent.yMinimum()))
        maxPt = xform.transform(QgsPoint(Extent.xMaximum(),Extent.yMaximum()))
        #set min and max extent of mapCanvas
        xMin = self.dlg.ui.lineEdit.setText(str(round(minPt.x(),6)))
        yMin = self.dlg.ui.lineEdit_2.setText(str(round(minPt.y(),6)))
        xMax = self.dlg.ui.lineEdit_3.setText(str(round(maxPt.x(),6)))
        yMax = self.dlg.ui.lineEdit_4.setText(str(round(maxPt.y(),6)))
        #set the directory where save the files
        global mydir
        mydir=""
        self.dlg.show()
        result = self.dlg.exec_() 

    def error(self,errorStr):
        #function to return error
        QMessageBox.warning(self.iface.mainWindow(), self.MSG_BOX_TITLE, str(errorStr))
        #raise errorStr
        self.dlg.close()
        self.run()
        
    #for about/help
    def helpAbout(self):
        #set the version
        source=__init__.version()
        #set the dialog of about/help
        self.aboutDlg=OGR2LayersAboutDialog()
        #set the regular expression for found the version
        regexVers = QRegExp('Version ([\d]+\.[\d]+\.[\d]+)')
        if regexVers.indexIn(source) > -1:
            #set the version number
            version=regexVers.cap(1)
        #add version to the label 
        self.aboutDlg.uiAbout.version_n.setText(QApplication.translate(
        "AboutDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \""\
        "http://www.w3.org/TR/REC-html40/strict.dtd\">\n" "<html><head><meta "\
        "name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n" "p,"\
        " li { white-space: pre-wrap; }\n" "</style></head><body style=\" "\
        "font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; "\
        "font-style:normal;\">\n" "<p style=\" margin-top:0px; margin-bottom:"\
        "0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; "\
        "text-indent:0px;\"><span style=\" font-size:12pt; font-weight:400;\" align=\"center\">"+version+"</span></p></body></html>", None, 
        QApplication.UnicodeUTF8))
        #show dialog
        self.aboutDlg.show()

    def SelectKmlDir(self):
        #set up the output dir for new vector files
        global mydir
        mydir = QFileDialog.getExistingDirectory( None,QString("Choose the GML"\
        " files destination folder"),"")
        if os.access(mydir, os.W_OK):
            self.dlg.ui.kmldirpath.setText(mydir)
            return
        else:
            self.error("It is not possible to write into folder '%s'" % mydir)
            
    def WriteKML(self):
        #string for textBrowser of last tab
        layerString=""
        #add the string to textBrowser
        self.dlg.ui.textBrowserLayer.setHtml(layerString)
        self.dlg.ui.textBrowserRaster.setHtml(layerString)

        #configure ProgressBar
	if len(self.layers) > 0:
	    #exist also ogr layers and WFS layers
	    self.dlg.ui.progressBar.setMinimum(0) 
	    #TO DECOMMENT WHEN ALSO RASTER WILL BE SUPPORTED
	    #self.dlg.ui.progressBar.setMaximum(len(self.mapCanvas.layers())) 
	    self.dlg.ui.progressBar.setMaximum(len(self.layers))
	    
	#control variable
	control =[]
	#test if the output dir "mydir" is set
	myDirectory = unicode(self.dlg.ui.kmldirpath.text())
	if myDirectory=='':
	    self.error("Please select the output directory first")
	else:
	    #if the directory is set, check if exist DA CORREGGERE COL METODO USATO CON MODIS
	    if not os.path.exists(myDirectory):
	        self.error("Please check the validity of the output directory")
	#initialize OGR2LayersClassHtml 
	OGR2LayersHtml = OGR2LayersClassHtml(self.layers,self.rasters,self.dlg,myDirectory)
	#start html code
	html = []
	try:
	    #write html code
	    html.append(OGR2LayersHtml.createHtml())
	    #name to write file with html code
	    htmlfileName = mydir+'/index.html'
	    #open a file
	    file = open(htmlfileName, "w")
	    #write the file
	    file.writelines(html[0])
	    #close the file
	    file.close()
	    
	    lastTab= self.dlg.ui.tabWidget.count()-1
	    #set the output tab like active
	    self.dlg.ui.tabWidget.setCurrentIndex(lastTab)
	    ##change ok button in close button and show a messages
	    self.dlg.ui.buttonBox.setStandardButtons(QDialogButtonBox.Close)			
	    QMessageBox.information(self.dlg,"Information",str("The OpenLayers"\
	    " Map has been created! Click \"Close\" for exit from the plugin") )	
	except Exception, e:
	    #raise e
	    self.error(e)

    #for choose what layer is queriable
    #def showQuery(self):
        #self.queryDlg=OGR2LayersQueryDialog()
        #for layer in self.layers:
            #self.queryDlg.uiQuery.prova=QGroupBox(self.queryDlg)
            #self.queryDlg.uiQuery.prova.setObjectName(''+layer.name()+'')
            #self.queryDlg.uiQuery.query = QRadioButton(self.queryDlg.uiQuery.prova)
            #self.queryDlg.uiQuery.query.setGeometry(QRect(10, 20, 132, 22))
            #self.queryDlg.uiQuery.query.setObjectName("query")
            #self.queryDlg.uiQuery.query_2 = QRadioButton(self.queryDlg.uiQuery.prova)
            #self.queryDlg.uiQuery.query_2.setGeometry(QRect(150, 20, 275, 22))
            #self.queryDlg.uiQuery.query_2.setObjectName("query_2")
            #self.queryDlg.uiQuery.query.setText(QApplication.translate("OGR2Layers", "query one feature", None, QApplication.UnicodeUTF8))
            #self.queryDlg.uiQuery.query_2.setText(QApplication.translate("OGR2Layers", "query more features (OL cluster strategy)", None, QApplication.UnicodeUTF8))
            #self.queryDlg.uiQuery.prova.setTitle(QApplication.translate("OGR2Layers", ""+layer.name()+"", None, QApplication.UnicodeUTF8))
            #self.queryDlg.uiQuery.verticalLayout.addWidget(self.queryDlg.uiQuery.prova)
        #self.queryDlg.show()
        #QObject.connect(self.queryDlg.uiQuery.buttonBox, SIGNAL("accepted()"), self.queryDlg.accept)
