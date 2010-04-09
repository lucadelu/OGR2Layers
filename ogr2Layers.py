# -*- coding: latin1 -*-
#############################################
#	OGR2Layers Plugin (c)  for Quantum GIS					#
#	(c) Copyright Nicolas BOZON - 2008					#
#	Authors: Nicolas BOZON, Rene-Luc D'HONT, Michael DOUCHIN, Luca DELUCCHI	#
#	Email: nicolas_dot_bozon_at_gmail_dot_com				#
#										#
#############################################
#    OGR2Layers Plugin is licensed under the terms of GNU GPL 2			#
#  	This program is free software; you can redistribute it and/or modify	#
# 	 it under the terms of the GNU General Public License as published by	#
# 	 the Free Software Foundation; either version 2 of the License, or	#
# 	 (at your option) any later version.					#
#	This program is distributed in the hope that it will be useful,		#
#	 but WITHOUT ANY WARRANTY; without even implied warranty of		#
# 	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.			# 
# 	 See the GNU General Public License for more details.			#
#############################################

#Python, PyQt and QGIS imports
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
from ogr2layersdialog import OGR2LayersDialog
from aboutdialog import OGR2LayersAboutDialog
from querydialog import OGR2LayersQueryDialog
import sys
import os
import resources_rc
import style_OGR2Layers
import vect_OGR2Layers
import query_OGR2Layers
import __init__

class OGR2Layers:
    MSG_BOX_TITLE = "OGR2Layers Plugin"

    def __init__(self, iface):
	self.iface = iface

    def initGui(self):
	self.action = QAction(QIcon(":/plugins/OGR2Layers/ogr2layersicon.png"), "OGR2Layers", self.iface.mainWindow())
	self.action.setWhatsThis("Configuration for OGR2Layers plugin")
	QObject.connect(self.action, SIGNAL("triggered()"), self.run)
	self.iface.addToolBarIcon(self.action)
	self.iface.addPluginToMenu("&OGR2Layers Plugin...", self.action)
	#os.mkdir('$HOME/.ogr2layers')
	#log=open('$HOME/.ogr2layers/ogr2layers.log',"w")
	#log.close()

    #Plugin disjunction
    def unload(self):
	self.iface.removePluginMenu("&OGR2Layers Plugin...",self.action)
	self.iface.removeToolBarIcon(self.action)
    #Plugin run
    def run(self):
	self.dlg = OGR2LayersDialog()
	#select directory where save files
	QObject.connect(self.dlg.ui.browseButton, SIGNAL("clicked()"), self.SelectKmlDir) 
	#function for open about dialog
	QObject.connect(self.dlg.ui.helpButton, SIGNAL("clicked()"), self.helpAbout) 

	#function for open query dialog
	#QObject.connect(self.dlg.ui.queryButton, SIGNAL("clicked()"), self.showQuery) 


	#load layer
	layers =  self.iface.activeLayer()
	#Checks for loaded layers, do not load if no layers
	if layers == None:
		QMessageBox.warning(self.iface.mainWindow(), self.MSG_BOX_TITLE, ("No active layer found\n" "Please make one or more OGR layer active\n" "Beware of layers sizes for export"), QMessageBox.Ok, QMessageBox.Ok)
		return
	#OGR layers 
	self.layers = [] 
	#WFS layers
	self.layersWFS = []
	#load qgis mapCanvas
	mapCanvas = self.iface.mapCanvas()
	#Checks vector type and populates the layer list view
	for i in range(mapCanvas.layerCount()-1,-1,-1):
		layer = mapCanvas.layer(i)
		if layer.type() == layer.VectorLayer:
			if layer.dataProvider().name() == "WFS":
				self.layersWFS.append(layer)
			else:
				self.layers.append(layer)
			#this is for remove "layerid=*" when use "Unique Value" symbology
			source=layer.source()
			source.remove(QRegExp('\|layerid=[\d]+$'))
			self.dlg.ui.LayerList.addItem(source)
	#check if there is some vectors layer
	if len(self.layers) == 0 and len(self.layersWFS) == 0:
		QMessageBox.warning(self.iface.mainWindow(), self.MSG_BOX_TITLE, ("No vector layer found\n" "Please load one or more OGR layer\n"), QMessageBox.Ok, QMessageBox.Ok)
		return

	#button for start the plugin
	QObject.connect(self.dlg.ui.buttonBox, SIGNAL("accepted()"), self.WriteKML)
	#button for close the plugin after create openlayers file
	QObject.connect(self.dlg.ui.buttonBox, SIGNAL("rejected()"), self.dlg.close)
	#Set up the default map extent
	Extent = mapCanvas.extent()
	if len(self.layers) > 0:
		mylayer = self.layers[0]
		myprovider = mylayer.dataProvider()
	else:
		mylayer = self.layersWFS[0]
		myprovider = mylayer.dataProvider()
	#set min and max extent of mapCanvas
	SrsSrc = myprovider.crs()
	SrsDest = QgsCoordinateReferenceSystem(4326)    # WGS 84
	xform = QgsCoordinateTransform(SrsSrc,SrsDest)
	minPt = xform.transform(QgsPoint(Extent.xMinimum(),Extent.yMinimum()))
	maxPt = xform.transform(QgsPoint(Extent.xMaximum(),Extent.yMaximum()))
	xMin = self.dlg.ui.lineEdit.setText(str(round(minPt.x(),6)))
	yMin = self.dlg.ui.lineEdit_2.setText(str(round(minPt.y(),6)))
	xMax = self.dlg.ui.lineEdit_3.setText(str(round(maxPt.x(),6)))
	yMax = self.dlg.ui.lineEdit_4.setText(str(round(maxPt.y(),6)))

	#settings = QSettings("3LIZ", "OGR2Layers")
	global mydir
	mydir=""
	self.dlg.show()
	result = self.dlg.exec_() 

    #for about/help
    def helpAbout(self):
	source=__init__.version()
	self.aboutDlg=OGR2LayersAboutDialog()
	regexVers = QRegExp('Version ([\d]+\.[\d]+)')
	if regexVers.indexIn(source) > -1:
	    version=regexVers.cap(1)
	self.aboutDlg.uiAbout.version_n.setText(QApplication.translate("AboutDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n" "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n" "p, li { white-space: pre-wrap; }\n" "</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal;\">\n" "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:400;\" align=\"center\">"+version+"</span></p></body></html>", None, QApplication.UnicodeUTF8))
	self.aboutDlg.show()

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

 
    def SelectKmlDir(self):
	#set up the output dir for KML
	global mydir
	mydir = QFileDialog.getExistingDirectory( None,QString("Choose the GML files destination folder"),"")
	self.dlg.ui.kmldirpath.setText(mydir)
	    
    def WriteKML(self):
	#string for textBrowser of last tab
	layerString=""
	#add the string to textBrowser
	self.dlg.ui.textBrowser.setHtml(layerString)
	#configure ProgressBar
	if len(self.layers) > 0 and len(self.layersWFS) > 0:
	    self.dlg.ui.progressBar.setMinimum(0) 
	    self.dlg.ui.progressBar.setMaximum(len(self.layers)+len(self.layersWFS)) 
	elif len(self.layers) > 0 and len(self.layersWFS) == 0:
	    self.dlg.ui.progressBar.setMinimum(0) 
	    self.dlg.ui.progressBar.setMaximum(len(self.layers)) 
	elif len(self.layers) == 0 and len(self.layersWFS) > 0:
	    self.dlg.ui.progressBar.setMinimum(0) 
	    self.dlg.ui.progressBar.setMaximum(len(self.layersWFS)) 
	compteur = 0
	#control variable
	control =[]
	#test if the output dir "mydir" is set and correct
	if str(self.dlg.ui.kmldirpath.text())=='':
	    control.append("Please select the output directory first")
	else:
	    mydirtest=self.dlg.ui.kmldirpath.text()
	    if not os.path.exists(mydirtest):
		control.append("Please check the validity of the output directory.")
	if len(control) == 0:
	    for layer in self.layers:
		if (vect_OGR2Layers.createOGR(layer,self.dlg.ui,mydir,self.iface)):
		    compteur = compteur + 1
		    #change progress bar value
		    self.dlg.ui.progressBar.setValue(compteur)
		else:
		    control.append('Error in vector layer, you have seen the error in last information window')
		    break
	if len(control) == 0:
	    #Generates XHTML 1 / Javascript
	    html = ['<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">\n']
	    html.append('<html xmlns="http://www.w3.org/1999/xhtml">\n')
	    html.append('<head>\n')
	    html.append('<title>OGR2Layers</title>\n')
	    
	    # Save chosen Map Size
	    mapSize = self.dlg.ui.mapSize.currentIndex()
	    if (mapSize) == 0: #400x400
		html.append('<style>\n #map{width:400px;height:400px;}\n</style>\n')
	    elif (mapSize) == 1: #800x600
		html.append('<style>\n #map{width:800px;height:600px;}\n</style>\n')
	    elif (mapSize) == 2: #full screen
		html.append('<style>\n #map{width:100%;height:1024px;}\n</style>\n')
    
	    #Call for OpenLayers 2.8 API on Metacarta servers
	    html.append('<script src="http://www.openlayers.org/api/2.8/OpenLayers.js"></script>\n')
	    html.append('<script type="text/javascript">\n')
	    html.append('var map, selectsControls\n')
	    html.append('function init(){\n')
	    # add coordinate transformation to 900913 if baseLayer is OSM
	    mapBaseLayer = self.dlg.ui.mapBaseLayer.currentIndex()
	    if (mapBaseLayer) == 0 or (mapBaseLayer) < 3:
		html.append('\tvar option = {\n\t\tprojection: new OpenLayers.Projection("EPSG:900913"),\n\t\tdisplayProjection: new OpenLayers.Projection("EPSG:4326")\n\t};\n\t')
		html.append("map = new OpenLayers.Map('map', option);\n\t")
		projection="EPSG:900913"
	    else:
		html.append("map = new OpenLayers.Map('map');\n\t")
		projection="EPSG:4326"
	    #Save chose Map Base Layer
	    # Lucadelu: add OpenLayers.Layer.OSM mapnik, osmarender (next cyclemap)
	    if (mapBaseLayer) == 0: #OpenStreetMap (Mapnik)
		html.append('olmapnik = new OpenLayers.Layer.OSM("OpenStreetMap Mapnik", "http://tile.openstreetmap.org/${z}/${x}/${y}.png");\n\t')
		html.append('map.addLayer(olmapnik);\n\t')
		html.append('map.setBaseLayer(olmapnik);\n\t')

	    elif (mapBaseLayer) == 1: #OpenStreetMap (Osmarender)
		html.append('olosma = new OpenLayers.Layer.OSM("OpenStreetMap Osmarender", "http://tah.openstreetmap.org/Tiles/tile/${z}/${x}/${y}.png");\n\t')
		html.append('map.addLayer(olosma);\n\t')
		html.append('map.setBaseLayer(olosma);\n\t')

	    elif (mapBaseLayer) == 2: #OpenStreetMap WMS
		html.append('osm = new OpenLayers.Layer.OSM("OpenStreetMap Cycleway", "http://a.andy.sandbox.cloudmade.com/tiles/cycle/${z}/${x}/${y}.png");\n\t')
		html.append('map.addLayer(osm);\n\t')
		html.append('map.setBaseLayer(osm);\n\t')
		    
	    elif (mapBaseLayer) == 3: #OpenLayers WMS
		html.append('olwms = new OpenLayers.Layer.WMS( "OpenLayers WMS", ["http://labs.metacarta.com/wms/vmap0"], {layers: "basic", format: "image/gif" } );\n\t')
		html.append('map.addLayer(olwms);\n\t')
		html.append('map.setBaseLayer(olwms);\n\t')
		    
	    elif (mapBaseLayer) == 4: #OpenLayers WMS
		html.append('bmwms = new OpenLayers.Layer.WMS( "Demis WMS", ["http://www2.demis.nl/WMS/wms.asp?wms=WorldMap"], {layers: "Bathymetry,Countries,Topography,Hillshading,Builtup+areas,Coastlines,Waterbodies,Inundated,Rivers,Streams,Railroads,Highways,Roads,Trails,Borders,Cities,Settlements"} );\n\t')
		html.append('map.addLayer(bmwms);\n\t')
		html.append('map.setBaseLayer(bmwms);\n\t')

	    # add vector layer
	    if len(self.layers) != 0:
		for layer in self.layers:
		    # make render by qgis symbology
		    if self.dlg.ui.qgisRender.isChecked():
			# create style from qgis rendering
			html.extend(style_OGR2Layers.createStyle(layer))
			if self.dlg.ui.query.isChecked():
			    html.append(''+layer.name()+' = new OpenLayers.Layer.GML("'+layer.name()+' GML","'+layer.name()+'.gml",{styleMap: '+layer.name()+'_style});\n\tmap.addLayer('+layer.name()+')\n\t')
			    html.extend(query_OGR2Layers.createQuery(layer,0))
			    
			elif self.dlg.ui.query_2.isChecked():
			    html.append('var strategy = new OpenLayers.Strategy.Cluster();')
			    html.append(''+layer.name()+' = new OpenLayers.Layer.GML("'+layer.name()+' GML","'+layer.name()+'.gml",{styleMap: '+layer.name()+'_style, strategies: [strategy]});\n\tmap.addLayer('+layer.name()+')\n\t')
			    html.extend(query_OGR2Layers.createQuery(layer,1))
			else:
			    html.append(''+layer.name()+' = new OpenLayers.Layer.GML("'+layer.name()+' GML","'+layer.name()+'.gml",{styleMap: '+layer.name()+'_style});\n\tmap.addLayer('+layer.name()+')\n\t')

		    else:
			if self.dlg.ui.query.isChecked():
			    html.append(''+layer.name()+' = new OpenLayers.Layer.GML("'+layer.name()+" "+'GML","'+layer.name()+'.gml");\n\tmap.addLayer('+layer.name()+');\n\t')
			    html.extend(query_OGR2Layers.createQuery(layer,0))
			elif self.dlg.ui.query_2.isChecked():
			    html.append('var strategy = new OpenLayers.Strategy.Cluster();')
			    html.append(''+layer.name()+' = new OpenLayers.Layer.GML("'+layer.name()+" "+'GML","'+layer.name()+'.gml",{strategies: [strategy]});\n\tmap.addLayer('+layer.name()+');\n\t')
			    html.extend(query_OGR2Layers.createQuery(layer,1))
			else:
			    html.append(''+layer.name()+' = new OpenLayers.Layer.GML("'+layer.name()+" "+'GML","'+layer.name()+'.gml");\n\tmap.addLayer('+layer.name()+');\n\t')
		if self.dlg.ui.query.isChecked() or self.dlg.ui.query_2.isChecked():
		    html.extend(query_OGR2Layers.addselectsControls(self.layers))
	
	    #add wfs layers still does not work
	    #if len(self.layersWFS) != 0:
		#for wfs in self.layersWFS:
		    #if self.dlg.ui.qgisRender.isChecked():
			#html.extend(style_OGR2Layers.createStyle(layer))
			#html.extend(vect_OGR2Layers.writeWFS(wfs,projection))
		    #else:
			#html.extend(vect_OGR2Layers.writeWFS(wfs,projection,False))

	    #Layer Switcher active or not
	    layerSwitcherActive = self.dlg.ui.layerSwitcherActive.currentIndex()
	    
	    if (layerSwitcherActive) == 0:
		html.append('var ls= new OpenLayers.Control.LayerSwitcher(); \n\tmap.addControl(ls); \n\tls.maximizeControl(); \n\t')
		    
	    elif (layerSwitcherActive) == 1:
		html.append('\n\t')
		    
	    #User defined Bounds
	    xmin = self.dlg.ui.lineEdit.text()
	    xmax = self.dlg.ui.lineEdit_2.text()
	    ymin = self.dlg.ui.lineEdit_3.text()
	    ymax = self.dlg.ui.lineEdit_4.text()

	    # Lucadelu: add for 900913 EPSG for the extent
	    if (mapBaseLayer) == 0 or (mapBaseLayer) < 3:
		html.append('extent = new OpenLayers.Bounds(' +str(xmin)+','+str(xmax)+','+str(ymin)+','+str(ymax)+').transform(new OpenLayers.Projection("EPSG:4326"), new OpenLayers.Projection("EPSG:900913"));\n\t')
		html.append('map.zoomToExtent(extent);\n\t')
	    else:
		html.append('map.zoomToExtent(new OpenLayers.Bounds(' +str(xmin)+','+str(xmax)+','+str(ymin)+','+str(ymax)+'))\n\t')

	    # Lucadelu: add optional controls
	    #--mouseposition
	    if self.dlg.ui.mousepos.isChecked():
		html.append('map.addControl(new OpenLayers.Control.MousePosition());\n\t')
	    ##--scale
	    if  self.dlg.ui.scale.isChecked():
		html.append('map.addControl(new OpenLayers.Control.Scale());\n\t')
	    ##--permalink
	    if self.dlg.ui.permalink.isChecked():
		html.append('map.addControl(new OpenLayers.Control.Permalink());\n\t')
	    ##--attribution
	    if  self.dlg.ui.copyr.isChecked():
		html.append('map.addControl(new OpenLayers.Control.Attribution());\n\t')
	    ##--overviewmap
	    if  self.dlg.ui.navi.isChecked():
		html.append('map.addControl(new OpenLayers.Control.OverviewMap());\n\t')
	    ##--panZoomBar
	    if  self.dlg.ui.zoomBar.isChecked():
		html.append('map.addControl(new OpenLayers.Control.PanZoomBar());\n')

	    

	    html.append('};\n\t')
	    html.append('function toggleControl(element) {\n\t\tfor(key in selectsControls) {\n\t\t\tvar control = selectsControls[key];\n\t\t\tif(element.value == key && element.checked) {\n\t\t\t\tcontrol.activate();\n\t\t\t} else {\n\t\t\t\t control.deactivate();\n\t\t\t}\n\t\t}\n\t}\n\t')
	    html.append('</script>\n</head>\n<body onload="init()">\n')
    
	    #Generate H1 Map Title
	    mapTitle = self.dlg.ui.mapTitle.text()
	    html.append('<h1>'+ mapTitle +'</h1>\n')
	    if self.dlg.ui.query.isChecked() or self.dlg.ui.query_2.isChecked():
		html.append('<input type="radio" name="select" value="-1" id="noQuery" onclick="toggleControl(this);" checked="checked" /> <label for="noQuery">No layer</label> ')
		if len(self.layers) != 0:
		    id_layer=0
		    for layer in self.layers:	    
			html.append('<input type="radio" name="select" value="'+str(id_layer)+'" id="'+layer.name()+'Query" onclick="toggleControl(this);" /> <label for="'+layer.name()+'Query">Query '+layer.name()+'</label> ')
			id_layer=id_layer+1
	    html.append('<div id="map"></div>\n</body>\n</html>\n')
	    htmlfileName = str(mydir)+'/index.html'
	    file = open(htmlfileName, "w")
	    file.writelines(html)
	    file.close()
	    ##change ok button in close button and show a messages
	    self.dlg.ui.buttonBox.setStandardButtons(QDialogButtonBox.Close)			
	    QMessageBox.information(self.dlg,"Information",str("The OpenLayers Map has been created! Click \"Close\" for exit from the plugin") )
		
	else:
	    QMessageBox.information(self.iface.mainWindow(),"Warning", "Some errors occured before processing. Please check and resolve the following errors:\n" + str([str(x) for x in control]) )
	    self.dlg.close()
	    self.run()
