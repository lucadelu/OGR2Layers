# -*- coding: latin1 -*-
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

#function for create the javascript code for the style
def createStyle(layer):
    layerName=str(layer.name())
    typeRend=layer.renderer().classificationAttributes()
    if (len(typeRend) == 0):
	style = layer.renderer().symbols()
	strokeColor=style[0].color().name()
	fillColor=style[0].fillColor().name()
	lineWidth=style[0].lineWidth()

	if (layer.geometryType()==0):
	    pointSize=style[0].pointSize()
	    html_style= 'var '+layerName+'_template = { '\
			'pointRadius: '+str(pointSize)+','\
			'strokeColor: "'+str(strokeColor)+'",'\
			'strokeOpacity: 1,'\
			'strokeWidth: '+str(lineWidth)+','\
			'fillColor: "'+str(fillColor)+'",'\
			'fillOpacity: 1'\
			'}\n'\
			'var '+layerName+'_style = new OpenLayers.Style('+layerName+'_template)\n'
	else:
	    html_style= 'var '+layerName+'_template = { '\
			'strokeColor: "'+str(strokeColor)+'",'\
			'strokeOpacity: 1,'\
			'strokeWidth: '+str(lineWidth)+','\
			'fillColor: "'+str(fillColor)+'",'\
			'fillOpacity: 1'\
			'}\n'\
			'var '+layerName+'_style = new OpenLayers.Style('+layerName+'_template)\n'
    else:
	numberField=layer.renderer().classificationAttributes()[0]
	nameField=nameAttrField(layer,numberField)
	styleMap = layer.renderer().symbolMap()
	if (layer.geometryType()==0):
	    html_style= ['var '+layerName+'_style = new OpenLayers.Style(OpenLayers.Util.applyDefaults({ '\
			'pointRadius: "${getPointSize}",'\
			'strokeColor: "${getScolor}",'\
			'strokeOpacity: 1,'\
			'strokeWidth: "${lineWidth}",'\
			'fillColor: "${fillColor}",'\
			'fillOpacity: 1'\
			'}, OpenLayers.Feature.Vector.style["default"]), {'\
			 'context: {']
	    html_style.extend(pointStyle(styleMap,nameField))
	    html_style.extend(colorStyle(styleMap,nameField))
	    html_style.extend(fillStyle(styleMap,nameField))
	    html_style.extend(lineStyle(styleMap,nameField))
	    html_style.append('}});\n')
	else:
	    html_style= ['var '+layerName+'_template = { '\
			'strokeColor: "${getScolor}",'\
			'strokeOpacity: 1,'\
			'strokeWidth: "${lineWidth}",'\
			'fillColor: "${fillColor}",'\
			'fillOpacity: 1'\
			'}, OpenLayers.Feature.Vector.style["default"]), {' \
			 'context: {']
	    html_style.extend(pointStyle(styleMap,nameField))
	    html_style.extend(colorStyle(styleMap,nameField))
	    html_style.extend(fillStyle(styleMap,nameField))
	    html_style.extend(lineStyle(styleMap,nameField))
	    html_style.append('}});\n')
    return html_style

#function for the name of field used in "Unique Value" symbology
def nameAttrField(layer,n):
    vprovider = layer.dataProvider()
    fields = vprovider.fields()
    return fields[n].name()
#function for the point size (used with vector point)
def pointStyle(styleMap,nameField):
    value=0
    higValue=len(styleMap)-1    
    for z,y in styleMap.iteritems():
	if (value==0):
	    html_point=['getPointSize: function(feature) { if (feature.attributes.'+nameField+'=="'+z+'"){point='+str(y.pointSize())+';}']
	    value=value+1
	elif (value==higValue):
	    html_point.append(' else if (feature.attributes.'+nameField+'=="'+z+'"){point='+str(y.pointSize())+';}; return point;},\n')
	else:
	    html_point.append(' else if (feature.attributes.'+nameField+'=="'+z+'"){point='+str(y.pointSize())+';}')
	    value=value+1
    return html_point
#function for the stroke color
def colorStyle(styleMap,nameField):
    value=0
    higValue=len(styleMap)-1
    for z,y in styleMap.iteritems():
	if (value==0):
	    html_color=['getScolor: function(feature) { if (feature.attributes.'+nameField+'=="'+z+'"){scolor="'+y.color().name()+'";}']
	    value=value+1
	elif (value==higValue):
	    html_color.append(' else if (feature.attributes.'+nameField+'=="'+z+'"){scolor="'+y.color().name()+'";}; return scolor;},\n')
	else:
	    html_color.append(' else if (feature.attributes.'+nameField+'=="'+z+'"){scolor="'+y.color().name()+'";}')
	    value=value+1
    return html_color
#function for the fill color
def fillStyle(styleMap,nameField):
    value=0
    higValue=len(styleMap)-1    
    for z,y in styleMap.iteritems():
	if (value==0):
	    html_fill=['fillColor: function(feature) { if (feature.attributes.'+nameField+'=="'+z+'"){fillcolor="'+y.fillColor().name()+'";}']
	    value=value+1
	elif (value==higValue):
	    html_fill.append(' else if (feature.attributes.'+nameField+'=="'+z+'"){fillcolor="'+y.fillColor().name()+'";}; return fillcolor;},\n')
	else:
	    html_fill.append(' else if (feature.attributes.'+nameField+'=="'+z+'"){fillcolor="'+y.fillColor().name()+'";}')
	    value=value+1
    return html_fill
#function for the line width
def lineStyle(styleMap,nameField):
    value=0
    higValue=len(styleMap)-1    
    for z,y in styleMap.iteritems():
	if (value==0):
	    html_line=['lineWidth: function(feature) { if (feature.attributes.'+nameField+'=="'+z+'"){lineWidth='+str(y.lineWidth())+';}']
	    value=value+1
	elif (value==higValue):
	    html_line.append(' else if (feature.attributes.'+nameField+'=="'+z+'"){lineWidth='+str(y.lineWidth())+';}; return lineWidth;}\n')
	else:
	    html_line.append(' else if (feature.attributes.'+nameField+'=="'+z+'"){lineWidth='+str(y.lineWidth())+';}')
	    value=value+1
    return html_line