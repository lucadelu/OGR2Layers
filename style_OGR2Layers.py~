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
    #layer name
    layerName=str(layer.name())
    #type of symbology
    typeRend=layer.renderer().classificationAttributes()
    #check if rendering is single symbol
    if (len(typeRend) == 0):
	#set the style
	style = layer.renderer().symbols()
	#set stroke color
	strokeColor=style[0].color().name()
	#set fill color
	fillColor=style[0].fillColor().name()
	#set line width
	lineWidth=style[0].lineWidth()
	#if vector is point
	if (layer.geometryType()==0):
	    #set the point size
	    pointSize=style[0].pointSize()
	    #start the javascript code for style of layer
	    html_style= 'var '+layerName+'_template = { \n\t\t'\
			'pointRadius: '+str(pointSize)+',\n\t\t'\
			'strokeColor: "'+str(strokeColor)+'",\n\t\t'\
			'strokeOpacity: 1,\n\t\t'\
			'strokeWidth: '+str(lineWidth)+',\n\t\t'\
			'fillColor: "'+str(fillColor)+'",\n\t\t'\
			'fillOpacity: 1\n\t'\
			'}\n\t'\
			'var '+layerName+'_style = new OpenLayers.Style('+layerName+'_template)\n\t'
	#if vector is not point
	else:
	    #start the javascript code for style of layer
	    html_style= 'var '+layerName+'_template = { \n\t\t'\
			'strokeColor: "'+str(strokeColor)+'",\n\t\t'\
			'strokeOpacity: 1,\n\t\t'\
			'strokeWidth: '+str(lineWidth)+',\n\t\t'\
			'fillColor: "'+str(fillColor)+'",\n\t\t'\
			'fillOpacity: 1\n\t'\
			'}\n\t'\
			'var '+layerName+'_style = new OpenLayers.Style('+layerName+'_template)\n\t'
    #if simbology is unique value
    else:
	#number of the field used for classification 
	numberField=layer.renderer().classificationAttributes()[0]
	#name of the field used for classification
	nameField=nameAttrField(layer,numberField)
	#style map
	styleMap = layer.renderer().symbolMap()
	#if layer is a vector point
	if (layer.geometryType()==0):
	    #start javascript code for style template
	    html_style= ['var '+layerName+'_style = new OpenLayers.Style(\n\t\tOpenLayers.Util.applyDefaults({ \n\t\t\t'\
			'pointRadius: "${getPointSize}",\n\t\t\t'\
			'strokeColor: "${getScolor}",\n\t\t\t'\
			'strokeOpacity: 1,\n\t\t\t'\
			'strokeWidth: "${lineWidth}",\n\t\t\t'\
			'fillColor: "${fillColor}",\n\t\t\t'\
			'fillOpacity: 1\n\t\t'\
			'}, OpenLayers.Feature.Vector.style["default"]), {\n\t\t\t'\
			 'context: {\n\t\t\t\t']
	    #add style for point size value
	    html_style.extend(pointStyle(styleMap,nameField))
	    #add style for stroke color value
	    html_style.extend(colorStyle(styleMap,nameField))
	    #add style for fill color value
	    html_style.extend(fillStyle(styleMap,nameField))
	    #add style for line width value
	    html_style.extend(lineStyle(styleMap,nameField))
	    #close the style
	    html_style.append('\n\t\t\t}\n\t\t}\n\t);\n\t')
	#if layer is not a vector point
	else:
	    #start javascript code for style template
	    html_style= ['var '+layerName+'_style = new OpenLayers.Style(\n\t\tOpenLayers.Util.applyDefaults({ \n\t\t\t'\
			'strokeColor: "${getScolor}",\n\t\t\t'\
			'strokeOpacity: 1,\n\t\t\t'\
			'strokeWidth: "${lineWidth}",\n\t\t\t'\
			'fillColor: "${fillColor}",\n\t\t\t'\
			'fillOpacity: 1\n\t\t'\
			'}, OpenLayers.Feature.Vector.style["default"]), {\n\t\t\t' \
			 'context: {\n\t\t\t\t']
	    #add style for stroke color value
	    html_style.extend(colorStyle(styleMap,nameField))
	    #add style for fill color value
	    html_style.extend(fillStyle(styleMap,nameField))
	    #add style for line width value
	    html_style.extend(lineStyle(styleMap,nameField))
	    #close the style
	    html_style.append('\n\t\t\t}\n\t\t}\n\t);\n\t')
    return html_style

#function for the name of field used in "Unique Value" symbology
def nameAttrField(layer,n):
    vprovider = layer.dataProvider()
    fields = vprovider.fields()
    #return the name of field
    return fields[n].name()

#function for the point size (used with vector point)
def pointStyle(styleMap,nameField):
    value=0
    higValue=len(styleMap)-1    
    for z,y in styleMap.iteritems():
	if (value==0):
	    html_point=['getPointSize: function(feature) {\n\t\t\t\t\tif (feature.attributes.'+nameField+'=="'+z+'"){\n\t\t\t\t\t\tpoint='+str(y.pointSize())+';\n\t\t\t\t\t}']
	    value=value+1
	elif (value==higValue):
	    html_point.append(' else if (feature.attributes.'+nameField+'=="'+z+'"){\n\t\t\t\t\t\tpoint='+str(y.pointSize())+';\n\t\t\t\t\t}\n\t\t\t\t\treturn point;\n\t\t\t\t},\n\t\t\t\t')
	else:
	    html_point.append(' else if (feature.attributes.'+nameField+'=="'+z+'"){\n\t\t\t\t\t\tpoint='+str(y.pointSize())+';\n\t\t\t\t\t}')
	    value=value+1
    return html_point

#function for the stroke color
def colorStyle(styleMap,nameField):
    value=0
    higValue=len(styleMap)-1
    for z,y in styleMap.iteritems():
	if (value==0):
	    html_color=['getScolor: function(feature) {\n\t\t\t\t\tif (feature.attributes.'+nameField+'=="'+z+'"){\n\t\t\t\t\t\tscolor="'+y.color().name()+'";\n\t\t\t\t\t}']
	    value=value+1
	elif (value==higValue):
	    html_color.append(' else if (feature.attributes.'+nameField+'=="'+z+'"){\n\t\t\t\t\t\tscolor="'+y.color().name()+'";\n\t\t\t\t\t}\n\t\t\t\t\treturn scolor;\n\t\t\t\t},\n\t\t\t\t')
	else:
	    html_color.append(' else if (feature.attributes.'+nameField+'=="'+z+'"){\n\t\t\t\t\t\tscolor="'+y.color().name()+'";\n\t\t\t\t\t}')
	    value=value+1
    return html_color

#function for the fill color
def fillStyle(styleMap,nameField):
    value=0
    higValue=len(styleMap)-1    
    for z,y in styleMap.iteritems():
	if (value==0):
	    html_fill=['fillColor: function(feature) {\n\t\t\t\t\tif (feature.attributes.'+nameField+'=="'+z+'"){\n\t\t\t\t\t\tfillcolor="'+y.fillColor().name()+'";\n\t\t\t\t\t}']
	    value=value+1
	elif (value==higValue):
	    html_fill.append(' else if (feature.attributes.'+nameField+'=="'+z+'"){\n\t\t\t\t\t\tfillcolor="'+y.fillColor().name()+'";\n\t\t\t\t\t}\n\t\t\t\t\treturn fillcolor;\n\t\t\t\t},\n\t\t\t\t')
	else:
	    html_fill.append(' else if (feature.attributes.'+nameField+'=="'+z+'"){\n\t\t\t\t\t\tfillcolor="'+y.fillColor().name()+'";\n\t\t\t\t\t}')
	    value=value+1
    return html_fill

#function for the line width
def lineStyle(styleMap,nameField):
    value=0
    higValue=len(styleMap)-1    
    for z,y in styleMap.iteritems():
	if (value==0):
	    html_line=['lineWidth: function(feature) {\n\t\t\t\t\tif (feature.attributes.'+nameField+'=="'+z+'"){\n\t\t\t\t\t\tlineWidth='+str(y.lineWidth())+';\n\t\t\t\t\t}']
	    value=value+1
	elif (value==higValue):
	    html_line.append(' else if (feature.attributes.'+nameField+'=="'+z+'"){\n\t\t\t\t\t\tlineWidth='+str(y.lineWidth())+';\n\t\t\t\t\t}\n\t\t\t\t\treturn lineWidth;\n\t\t\t\t},\n\t\t\t\t')
	else:
	    html_line.append(' else if (feature.attributes.'+nameField+'=="'+z+'"){\n\t\t\t\t\t\tlineWidth='+str(y.lineWidth())+';\n\t\t\t\t\t}')
	    value=value+1
    return html_line