# -*- coding: utf-8 -*-
#############################################
#	OGR2Layers Plugin (c)  for Quantum GIS				
#	(c) Copyright Nicolas BOZON - 2008				
#	Authors: Nicolas BOZON, Rene-Luc D'HONT, Michael DOUCHIN, Luca DELUCCHI
#	Email: nicolas_dot_bozon_at_gmail_dot_com			
#									
#############################################
#    OGR2Layers Plugin is licensed under the terms of GNU GPL 2		
#  	This program is free software; you can redistribute it and/or modify
# 	 it under the terms of the GNU General Public License as published by
# 	 the Free Software Foundation; either version 2 of the License, or
# 	 (at your option) any later version.				
#	This program is distributed in the hope that it will be useful,	
#	 but WITHOUT ANY WARRANTY; without even implied warranty of	
# 	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.		 
# 	 See the GNU General Public License for more details.		
#############################################

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from OGR2ClassLayer import *
from OGR2ClassQuery import OGR2LayersClassControlSel

class OGR2LayersClassHtml:
  """The class to create html and javascript code"""
  def __init__(self, 
		layers,
		dlg,
		directory
	      ):
    #the active layers
    self.layers = layers
    #the dialog
    self.dlg = dlg
    #the directory where save the data
    self.myDirectory = directory
    #type of query
    self.myQuery = 'none' 
    #the map baseLayer
    self.mapBaseLayer = self.dlg.ui.mapBaseLayer.currentIndex()
      
  def createHtml(self):
    """Create the html code"""
    html = ['<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">\n']
    html.append('<html xmlns="http://www.w3.org/1999/xhtml">\n')
    html.append('<head>\n')
    html.append('<title>OGR2Layers</title>\n')
    #add style for map
    html.extend(self.olMapSize()) 
    #Call for OpenLayers 2.10 API on Metacarta servers
    html.append('<script src="http://www.openlayers.org/api/OpenLayers.js"></script>\n')
    #start javascript code
    html.append('<script type="text/javascript">\n')
    #set global variable (map, selectsControls)
    html.append('var map, selectsControls\n')
    #start function for OL
    html.append('function init(){\n')	
    #add the base layer
    html.extend(self.olBaseLayer()) 
    #add the controls
    html.extend(self.olControl())
    #try to add the code for layer
    try:
      html.extend(self.htmlLayer())
    #return errors
    except Exception, e:
      raise e
    #add the query 
    if self.myQuery != 'none':
      html.extend(self.controlSel())
    html.extend(self.extentHtml())
    #close the init function
    html.append('};\n')	    
    #close javascript script and start body where is loaded init function
    html.append('</script>\n</head>\n<body onload="init()">\n')
    #Generate H1 Map Title
    mapTitle = self.dlg.ui.mapTitle.text()
    html.append('<h1>'+ mapTitle +'</h1>\n')		    
    #add the map and close the html file
    html.append('<div id="map"></div>\n</body>\n</html>\n')
    
    return html
    
  def olMapSize(self):
    #add the style of map (dimension)
    mapSize = self.dlg.ui.mapSize.currentIndex()
    if (mapSize) == 0: #400x400
      return '<style>\n #map{width:400px;height:400px;}\n</style>\n'
    elif (mapSize) == 1: #800x600
      return '<style>\n #map{width:800px;height:600px;}\n</style>\n'
    elif (mapSize) == 2: #full screen
      return '<style>\n #map{width:100%;height:1024px;}\n</style>\n'

  def extentHtml(self):
    """add coordinate transformation to 900913 if baseLayer is OSM"""
    #User defined Bounds
    xmin = self.dlg.ui.lineEdit.text()
    xmax = self.dlg.ui.lineEdit_2.text()
    ymin = self.dlg.ui.lineEdit_3.text()
    ymax = self.dlg.ui.lineEdit_4.text()		
    if (self.mapBaseLayer) == 0 or (self.mapBaseLayer) < 3:
      html = ['extent = new OpenLayers.Bounds(' +str(xmin)+','+str(xmax)+','+str(ymin)+','+str(ymax)+').transform(new OpenLayers.Projection("EPSG:4326"), new '\
      'OpenLayers.Projection("EPSG:900913"));\n\t']
      	
    else:
      html = ['extent = new OpenLayers.Bounds(' +str(xmin)+','+str(xmax)+','+str(ymin)+','+str(ymax)+'))\n']
    html.append('map.zoomToExtent(extent);\n')
    #if self.dlg.ui.maxExtent.isChecked():
      #AGGIUNGERE IL CODICE PER IL MAX EXTEND
    return html
	  
  def olBaseLayer(self):
    """Define the baseLayer"""
    if (self.mapBaseLayer) == 0 or (self.mapBaseLayer) < 3:
      html = ['\tvar option = {\n\t\tprojection: new '\
      'OpenLayers.Projection("EPSG:900913"),\n\t\tdisplayProjection: new OpenLayers.Projection("EPSG:4326")\n\t};\n\t']
      html.append("map = new OpenLayers.Map('map', option);\n\t")	    
      self.projection="EPSG:900913"
    else:
      html = ["map = new OpenLayers.Map('map');\n\t"]  
      self.projection="EPSG:4326"
    #Save chose Map Base Layer
    if (self.mapBaseLayer) == 0: #OpenStreetMap (Mapnik)
      html.append('olmapnik = new OpenLayers.Layer.OSM("OpenStreetMap Mapnik", "http://tile.openstreetmap.org/${z}/${x}/${y}.png");\n\t')
      html.append('map.addLayer(olmapnik);\n\t')
      html.append('map.setBaseLayer(olmapnik);\n\t')
    elif (self.mapBaseLayer) == 1: #OpenStreetMap (Osmarender)
      html.append('olosma = new OpenLayers.Layer.OSM("OpenStreetMap Osmarender", "http://tah.openstreetmap.org/Tiles/tile/${z}/${x}/${y}.png");\n\t')
      html.append('map.addLayer(olosma);\n\t')
      html.append('map.setBaseLayer(olosma);\n\t')
    elif (self.mapBaseLayer) == 2: #OpenStreetMap (Cycleway)
      html.append('osm = new OpenLayers.Layer.OSM("OpenStreetMap Cycleway", "http://a.andy.sandbox.cloudmade.com/tiles/cycle/${z}/${x}/${y}.png");\n\t')
      html.append('map.addLayer(osm);\n\t')
      html.append('map.setBaseLayer(osm);\n\t')    
    elif (self.mapBaseLayer) == 3: #OpenLayers WMS
      html.append('olwms = new OpenLayers.Layer.WMS( "OpenLayers WMS", ["http://labs.metacarta.com/wms/vmap0"], {layers: "basic", format: '\
      '"image/gif" } );\n\t')
      html.append('map.addLayer(olwms);\n\t')
      html.append('map.setBaseLayer(olwms);\n\t')    
    elif (self.mapBaseLayer) == 4: #Demis WMS
      html.append('bmwms = new OpenLayers.Layer.WMS( "Demis WMS", ["http://www2.demis.nl/WMS/wms.asp?wms=WorldMap"], {layers: "Bathymetry,Countries,Topography,Hillshading,Builtup+areas,Coastlines,Waterbodies,Inundated,Rivers,Streams,Railroads,Highways,Roads,Trails,Borders,Cities,Settlements"} );\n\t')
      html.append('map.addLayer(bmwms);\n\t')
      html.append('map.setBaseLayer(bmwms);\n\t')	
    return html
      
  def olControl(self):
    """Layer Switcher active or not and add the chosen control"""
    layerSwitcherActive = self.dlg.ui.layerSwitcherActive.currentIndex()
    #it's active
    if layerSwitcherActive == 0:
      html = ['var ls= new OpenLayers.Control.LayerSwitcher(); \n\tmap.addControl(ls); \n\tls.maximizeControl(); \n\t']
    #is not active
    elif layerSwitcherActive == 1:
      html = ['map.addControl(new OpenLayers.Control.LayerSwitcher());\n\t']
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
      html.append('map.addControl(new OpenLayers.Control.PanZoomBar());\n\t')	
    return html
      
  def outFormat(self):
    """The output format chosen"""
    layerSwitcherOutput = self.dlg.ui.outputFormCombo.currentIndex()
    if layerSwitcherOutput == 0:
      outputFormat='GeoJSON'
    # GML format
    elif layerSwitcherOutput == 1:
      outputFormat='GML'		    
    return outputFormat
      
  def htmlLayer(self):
    """Add the code for layer, name, style and query"""
    compteur = 0
    html = []
    outputFormat = self.outFormat()
    for layer in self.layers:
      if self.dlg.ui.qgisRender.isChecked():
	myRendering = 'qgis'
      else:
	myRendering = 'default'
	  
      if self.dlg.ui.query.isChecked():
	self.myQuery = 'single'
      elif self.dlg.ui.query_2.isChecked():
	if layer.geometryType() == 0:
	  if myRendering == 'qgis' and layer.renderer().name() == 'Single Symbol':
	    self.myQuery = 'cluster'
	  elif myRendering == 'default':
	    self.myQuery = 'cluster'
	  elif myRendering == 'qgis' and not layer.renderer().name() == 'Single Symbol':
	    #return an error if the symbology is different from Single Symbol
	    raise Exception, "Unique value classification doesn't work with "\
	    "Cluster Strategy\n" # WORK
	    break
	else:
	  raise Exception, "Cluster Strategy support only vector point\n" # WORK
	  break

      OGR2LayersLayer = OGR2LayersClassLayer(layer, myRendering, self.myQuery, 
      outputFormat, self.projection, self.myDirectory)
      try:
	OGR2LayersLayer.convertOGR()
      except Exception, e:
	raise e # WORK
      if myRendering == 'qgis':
	try:
	  html.extend(OGR2LayersLayer.htmlStyle())
	except Exception, e:
	  raise e
      if self.myQuery != 'none':
	html.extend(OGR2LayersLayer.htmlQuery())
      html.extend(OGR2LayersLayer.htmlLayer())
      #self.dlg.ui.textBrowser.  ##AGGIUNGERE TESTO AL TEXTBROWSER PER BUONA RIUSCITA CONVERSIONE
      compteur = compteur + 1	    
      self.dlg.ui.progressBar.setValue(compteur)
      
    return html
	  
  def controlSel(self):
    """Add the code for have all layer queryable"""
    classControl = OGR2LayersClassControlSel(self.layers)
    return classControl.htmlSelectControl()