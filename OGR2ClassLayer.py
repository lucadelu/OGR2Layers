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
from qgis.core import *
from qgis.gui import *

import sys
import os
import string

import OGR2ogr
from OGR2ClassQuery import *
from OGR2ClassStyle import *


class OGR2LayersClassLayer:
  """A class to convert and add layer to the file
      layer = QGIS layer
      rendering = type of rendering (default, qgis)
      query = type of query (none,single,cluster)
      outputFormat = output format 
      outProj = output projection
      mydir = directory where save the files    
  """
  def __init__(self, 
		layer,
		rendering,
		query,
		outputFormat, 
		outProj,
		mydir,
	      ):
    #qgis layer
    self.layer = layer
    #qgis layer source
    self.source = self.layer.source()
    self.source.remove(QRegExp('\|layerid=[\d]+$'))
    #layer name
    self.name = self.layer.name()   
    #layer output format
    self.outputFormat = outputFormat
    #putput vector name 
    self.outputName = unicode(self.name + "." + self.outputFormat)
    #input epsg
    self.inEpsg = self.layer.crs().epsg() 
    #set the output epsg code
    if outProj == "EPSG:900913":
	self.outputEpsg = 900913
    elif outProj == "EPSG:4326":
	self.outputEpsg = 4326
    #type of rendering
    self.rendering = rendering
    #type of query
    self.query = query
    #type of vector
    self.providerName = str(self.layer.dataProvider().name())
    #directory where save files
    self.pathSave = mydir
    #name of file to write
    self.destPathName =  os.path.abspath(os.path.join(self.pathSave,self.outputName))
    #class query	
    self.classQuery = OGR2LayersClassQuery(self.layer, self.query)
    #class rendering
    self.classStyle = OGR2LayersClassStyle(self.layer,self.pathSave)
    self.image = self.classStyle.svg

	      
  def convertOGR(self):
    """Convert vector layer and set the variable for html file"""
    #add WFS
    if (self.providerName == "WFS"):
      #if the input and output epsg have the same projection add WFS 
      #like OpenLayers.Layer.WFS
      if self.inEpsg == self.outputEpsg:
	self.OpenLayersFormat = "WFS"
	self.outputFormat = "WFS"
	self.outputName = self.source
      #else write shapefile from WFS and reproject it with the right 
      #projection and load it like OpenLayers.Layer.GML
      else:
	if self.writeShape():
	  return 0
	#nameFileWFS = os.path.abspath(os.path.join(self.pathSave, 
	#str(self.name) + "_temp.shp"))
	#QgsVectorFileWriter.deleteShapeFile(nameFileWFS)
	#inputQgsReference = QgsCoordinateReferenceSystem()
	#inputQgsReference.createFromEpsg(self.inEpsg)
	#writeShape = QgsVectorFileWriter.writeAsShapefile(self.layer, 
	#nameFileWFS, "UTF8", inputQgsReference)
	#if writeShape == QgsVectorFileWriter.NoError:
	  #OGR2ogr.Ogr2Ogr(nameFileWFS, str(self.destPathName), self.outputEpsg,
	  #self.inEpsg, self.outputFormat)
	  #self.OpenLayersFormat = "GML"
	else:
	  raise Exception, "Some problem with convertion from WFS"
    #add other vector type
    else :
      #spatialite
      if (self.providerName == "spatialite" or self.providerName == "postgres"): 
	if self.writeShape():
	  return 0	
	else:
	  raise Exception, "Some problem with convertion from database"	
	#raise Exception, "There is a bug with OGR and Spatialite and " \
	#+ "now it isn't possible support Spatialite\n" # WORK
	#mysource_temp = self.source.split(' ')[0]
	#mysource_temp = str(mysource_temp.split('=')[1])
	#self.source = mysource_temp.replace("'","")
      #grass
      elif (self.providerName == "grass"): #grass
	mysource_temp = str(self.source).split('/')[0:-1]
	mysource_temp.insert(-1,"vector")
	mysource_temp.append("head")
	self.source = string.join(mysource_temp,'/')
      #other type of vector like Esri shapefile, GML, KML, GeoJson
      OGR2ogr.Ogr2Ogr(str(self.source), str(self.destPathName), self.outputEpsg,
      self.inEpsg, self.outputFormat)
      self.OpenLayersFormat = "GML"
      
      return 0

  def writeShape(self):
      nameFile = os.path.abspath(os.path.join(str(self.pathSave), 
      str(self.name) + '_temp.shp'))
      QgsVectorFileWriter.deleteShapeFile(nameFile)
      inputQgsReference = QgsCoordinateReferenceSystem()
      inputQgsReference.createFromEpsg(self.inEpsg)
      writeShape = QgsVectorFileWriter.writeAsShapefile(self.layer, 
      str(nameFile), "UTF8", inputQgsReference)
      if writeShape == QgsVectorFileWriter.NoError:
	OGR2ogr.Ogr2Ogr(nameFile, str(self.destPathName), self.outputEpsg,
	self.inEpsg, self.outputFormat)
	self.OpenLayersFormat = "GML"
	QgsVectorFileWriter.deleteShapeFile(nameFile)
	return True
      

  def htmlStyle(self):
    """Create javascript code for style"""
    if self.rendering == 'qgis':
      try:
	return self.classStyle.typeRendering()
      except Exception, e:
	raise Exception, e
	    
	  
  def htmlQuery(self):
    """Create javascript code for query"""      
    return self.classQuery.createQuery()

  def htmlLayer(self):
    """Create the Javascript code for vector layer"""
    htmlLayer = ['var ' + self.name + ' = new OpenLayers.Layer.' \
    + self.OpenLayersFormat + '("' + self.name + ' ' + self.outputFormat \
    + '", "' + self.outputName + '"']
    #if outputFormat is GeoJson
    if self.outputFormat == 'GeoJSON':
      #add the format
      htmlLayer.append(', {format: OpenLayers.Format.GeoJSON')
      #add cluster strategy query if it's choosen
      if self.query == 'cluster':
	htmlLayer.append(', strategies: [strategy]')
      #add style if qgis style if it's choosen
      if self.rendering == 'qgis':
	htmlLayer.append(', styleMap: ' + self.name + '_style')
      htmlLayer.append('}')
    #outputFormat is GML
    else:
      #add cluster strategy
      if self.query == 'cluster':
	htmlLayer.append(', {strategies: [strategy]')
	#if qgis style it's choosen add it, I use this indentation for { 
	#because it is already open with strategy cluster
	if self.query == 'qgis':
	    htmlLayer.append(', styleMap: ' + self.name + '_style')
	htmlLayer.append('}')
      #if only qgis style it's choosen I must open {
      if self.query != 'cluster' and self.query == 'qgis':
	htmlLayer.append(', {styleMap: ' + self.name + '_style}')
    #for all it closes the layer ) and add it to the map
    htmlLayer.append(');\n\tmap.addLayer('+ self.name +');\n\t')
    
    return htmlLayer
      
