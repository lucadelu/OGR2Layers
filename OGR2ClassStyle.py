# -*- coding: utf-8 -*-
#############################################
#	OGR2Layers Plugin (c)  for Quantum GIS					#
#	(c) Copyright Luca Delucchi 2010					#
#	Authors: Luca DELUCCHI							#
#	Email: lucadelucchi_at_gmail_dot_com					#
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

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from OGR2Funz import *

class OGR2LayersClassStyle:
    """A class to create style of layer and the relative code"""
    def __init__(self, 
		  layer
		):

	#qgis layer
	self.layer = layer
	# layer geometry type
	self.typeGeom = layer.geometryType()
	#layer name
	self.name = self.layer.name()
	# layer renderer
	self.renderer = self.layer.renderer()
	#type of rendering
	self.typeRend = str(self.renderer.name())
	if self.typeRend != 'Single Symbol':
	  self.numFieldClass = self.renderer.classificationAttributes()[0]
	  self.nameField = nameAttrField(self.layer,self.numFieldClass)
	    
    def typeRendering(self):
	##if Continuous Color
	if self.typeRend == 'Continuous Color':
	  #self.contColor()
	  raise Exception, "Continuous Color rendering it isn't supported yet\n"
  	##if Graduated Symbol
	if self.typeRend == 'Graduated Symbol':
	  return self.gradSymbol()
	#if Single Symbol
	elif self.typeRend == 'Single Symbol':
	  return self.singleSymbol()
	#if Unique Value
	elif self.typeRend == 'Unique Value':
	  return self.uniqueVal()
	else:
	  raise Exception, "There are some problem with the rendering\n"
	
	
    def singleSymbol(self):
	style = self.renderer.symbols()
	#set stroke color
	strokeColor=style[0].color().name()
	#set fill color
	fillColor=style[0].fillColor().name()
	#set line width
	lineWidth=style[0].lineWidth()
	html_style= ['var ' + self.name + '_template = { \n\t\t']
	if self.typeGeom == 0:
	    pointSize=style[0].pointSize()
	    html_style.append('pointRadius: ' + str(pointSize) + ',\n\t\t')
	html_style.append('strokeColor: "' + str(strokeColor) + '",\n\t\t'\
		    'strokeOpacity: 1,\n\t\t'\
		    'strokeWidth: ' + str(lineWidth) + ',\n\t\t'\
		    'fillColor: "' + str(fillColor) + '",\n\t\t'\
		    'fillOpacity: 1\n\t'\
		    '}\n\t'\
		    'var ' + self.name + '_style = new OpenLayers.Style(' + self.name + '_template)\n\t')
	return html_style

    def uniqueVal(self):
	styleMap = self.renderer.symbolMap()
	html_style= ['var ' + self.name + '_style = new OpenLayers.Style(\n\t\tOpenLayers.Util.applyDefaults({ \n\t\t\t']
	if self.typeGeom == 0:
	    html_style.append('pointRadius: "${getPoint}",\n\t\t\t')
	html_style.append('strokeColor: "${getStrokeColor}",\n\t\t\t'\
		    'strokeOpacity: 1,\n\t\t\t'\
		    'strokeWidth: "${getLineWidth}",\n\t\t\t'\
		    'fillColor: "${getFillColor}",\n\t\t\t'\
		    'fillOpacity: 1\n\t\t'\
		    '}, OpenLayers.Feature.Vector.style["default"]), {\n\t\t\t'\
		      'context: {\n\t\t\t\t')
	if self.typeGeom == 0:
	    #add style for stroke color value
	    html_style.extend(self.addElementStyleUnique(styleMap,'Point'))
	#add style for stroke color value
	html_style.extend(self.addElementStyleUnique(styleMap,'StrokeColor'))
	#add style for fill color value
	html_style.extend(self.addElementStyleUnique(styleMap,'FillColor'))
	#add style for line width value
	html_style.extend(self.addElementStyleUnique(styleMap,'LineWidth'))
	#close the style
	html_style.append('\n\t\t\t}\n\t\t}\n\t);\n\t')
	return html_style
	
    def addElementStyleUnique(self,styleMap,element):
	""" Function for the point size (used with vector point);
	    it's used in createStyle
	styleMap = stile map in qgis format
	nameField = the name of field for the classification
	"""
	value=0
	# the higher number od styleMap
	higValue=len(styleMap)-1   
	#for each field in styleMap
	for z,y in styleMap.iteritems():
	    if element == 'Point':
		valueStyle = str(y.pointSize())
	    elif element == 'StrokeColor':
		valueStyle = '"' + str(y.color().name()) + '"'
	    elif element == 'LineWidth':
		valueStyle = str(y.lineWidth())
	    elif element == 'FillColor':
		valueStyle = '"' + str(y.fillColor().name()) + '"'
	    # if the field is the first
	    if (value==0):
		html_element = ['get' + element + ': function(feature) {\n\t\t\t\t\tif (feature.attributes.' + self.nameField + '=="' + z + '"){\n\t\t\t\t\t\telement='+ valueStyle +';\n\t\t\t\t\t}']
		value=value+1
	    # if the field is the last
	    elif (value==higValue):
		html_element.append(' else if (feature.attributes.' + self.nameField + '=="' + z + '"){\n\t\t\t\t\t\telement=' + valueStyle + ';\n\t\t\t\t\t} else {\n\t\t\t\t\t\telement="NULL";\n\t\t\t\t\t}\n\t\t\t\t\treturn element;\n\t\t\t\t},\n\t\t\t\t')
	    else:
		html_element.append(' else if (feature.attributes.' + self.nameField + '=="' + z + '"){\n\t\t\t\t\t\telement=' + valueStyle + ';\n\t\t\t\t\t}')
		value=value+1
	#return the code
	return html_element
	
    def gradSymbol(self):
	symbolsGrad = self.renderer.symbols()
	value = 0
	# the higher number od styleMap
	higValue = len(symbolsGrad) - 1   	
	html_style = ['var ' + self.name + '_style = new OpenLayers.Style({\n\t\tfillOpacity: 1,\n\t\tstrokeOpacity: 1\n\t},{\n\t\trules: [\n\t\t\t']
	for symbol in symbolsGrad:
	    html_style.append('new OpenLayers.Rule({\n\t\t\t\tfilter: new OpenLayers.Filter.Comparison({\n\t\t\t\t\ttype: OpenLayers.Filter.Comparison.BETWEEN,\n\t\t\t\t\tproperty: "' + self.nameField + '",\n\t\t\t\t\tlowerBoundary: ' + str(symbol.lowerValue()) + ',\n\t\t\t\t\tupperBoundary: ' + str(symbol.upperValue()) + '\n\t\t\t\t}),\n\t\t\t\tsymbolizer: { strokeColor: "' + symbol.color().name() + '",\n\t\t\t\t\tfillColor: "' + symbol.fillColor().name() + '",\n\t\t\t\t\tstrokeWidth: ' + str(symbol.lineWidth()) + '')
	    if self.typeGeom == 0:
		html_style.append(',\n\t\t\t\t\tpointRadius: ' + str(symbol.pointSize()) + '')
	    html_style.append('\n\t\t\t\t}\n\t\t\t})')
	    if value != higValue:
		html_style.append(',\n\t\t\t')
	    value = value + 1
	html_style.append('\n\t\t]\n\t});\n')
	return html_style
	