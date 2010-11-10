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

from OGR2Funz import *

class OGR2LayersClassQuery:
    """A class to convert and add layer to the file
       	layer = QGIS layer
	rendering = type of rendering (default, qgis)
	query = type of query (none,single,cluster)
	outputFormat = output format 
	outProj = output projection
	mydir = directory where save the files    
	ui = interface for dialogs
    """
    def __init__(self, 
		  layer,
		  query
		):

	#qgis layer
	self.layer = layer
  	#layer name
	self.name = str(self.layer.name())
	#type of query
	self.query = query
	#fields name
	self.fieldsNameLayer = fieldsName(self.layer)
  
    def createQuery(self):
	#start javascript code for the query (add selectControl)
	html_query=['//START QUERY '+ self.name]
	
	#'\n\tvar selectControl'+self.name+' = new OpenLayers.Control.SelectFeature(\n\t\t'+self.name+', {\n\t\t\tonSelect: onFeatureSelect'+self.name+',\n\t\t\tonUnselect: onFeatureUnselect'+self.name+'\n\t\t}\n\t);'\n\tmap.addControl(selectControl'+self.name+');\n\t//selectControl'+self.name+'.activate();\n\t']
	#add function for close the popup
	html_query.append('\n\tfunction onPopupClose' + self.name + '(evt) {\n\t\tselectControl.unselect(selectedFeature);\n\t}\n\t')
	#add function for features selected
	html_query.append('function onFeatureSelect' + self.name + '(feature){\n\t\tselectedFeature = feature;') 
	if (self.query == 'single'):
	    #simple query
	    html_query.extend(self.htmlTable())
	elif (self.query == 'cluster'):
	    #query with cluster strategy
	    html_query.extend(self.htmlTableCluster())	
	#else
	    #AGGIUNGERE ERRORE
	#add popup to the function for features selected
	html_query.append('\n\t\tpopup = new OpenLayers.Popup.FramedCloud("chicken", \n\t\t\tfeature.geometry.getBounds().getCenterLonLat(),\n\t\t\tnew OpenLayers.Size(1000,500),\n\t\t\ttable'+self.name+',\n\t\t\tnull,\n\t\t\ttrue,\n\t\t\tonPopupClose'+self.name+'\n\t\t); \n\t\tfeature.popup = popup;\n\t\tmap.addPopup(popup);\n\t}\n\t')
	#create function for unselect features
	html_query.append('function onFeatureUnselect'+self.name+'(feature) {\n\t\tmap.removePopup(feature.popup);\n\t\tfeature.popup.destroy();\n\t\tfeature.popup = null;\n\t}\n\t//STOP QUERY '+self.name+'\n\t');
	#return javascript code for the query
	return html_query
	
    def htmlTable(self):
	""" Create html table for the single query; it's used in createQuery
	fields = a list of all field name (return from fieldsName function)
	layer = the input layer
	"""
	#add javascript table for popup
	html=['\n\t\ttable'+self.name+'="<html><meta http-equiv=\'Content-Type\' content=\'text/html; charset=UTF-8\'><body><table>']
	#for each field add a column for the feature
	for field in self.fieldsNameLayer:
	    html.append('<tr><td><b>' + field + ':</b></td><td><i>"+feature.attributes.' + field + '+"</i></td></tr>')
	html.append('</table></body></html>"; ')
	#return javascript code
	return html
	
    def htmlTableCluster(self):
	""" Create html table for the query using cluster strategy; it's used in createQuery
	fields = a list of all field name (return from fieldsName function)
	layer = the input layer
	"""
	#start table
	html=['\n\t\ttable'+self.name+'="<html><meta http-equiv=\'Content-Type\' content=\'text/html; charset=UTF-8\'><body><table><tr bgcolor=\'#c5e2ca\'>']
	#for each field add a column with the name of the field
	for field in self.fieldsNameLayer:
	    html.append('<td>'+field+'</td>')
	#finisc the caption row
	html.append('</tr>";')
	#add javascript code for all features select create a row
	html.append('\n\t\tfor (var i=0; i < feature.cluster.length; ++i){\n\t\t\ttable'+self.name+'+="<tr>')
	#for each field add a column in the row of selected features
	for field in fields:
	    html.append('<td>"+feature.cluster[i].attributes.'+field+'+"</td>')
	html.append('</tr>"\n\t\t}\n\t\ttable'+self.name+'+="</table></body></html>"; ')
	#return javascript code
	return html
	
class OGR2LayersClassControlSel:
    """A class to convert and add layer to the file
       	layer = QGIS layer
	rendering = type of rendering (default, qgis)
	query = type of query (none,single,cluster)
	outputFormat = output format 
	outProj = output projection
	mydir = directory where save the files    
	ui = interface for dialogs
    """
    def __init__(self, 
		  layers,
		):
		  
	self.layers = layers
	
    def htmlSelectControl(self):
	#start control
	html = ['selectControl = new OpenLayers.Control.SelectFeature(\n\t\t[']
	#for each layer
        for layer in self.layers:
	    #layer name
	    name = str(layer.name())
	    #append layer name to control
	    html.append(name + ', ')
	html.append('],\n\t\t{\n\t\t\tclickout: true, toggle: false, \n\t\t\tmultiple: false, hover: false, \n\t\t\ttoggleKey: "ctrlKey", // ctrl key removes from selection\n\t\t\tmultipleKey: "shiftKey" // shift key adds to selection\n\t\t}\n\t);\n\tmap.addControl(selectControl);\n\tselectControl.activate();')
        for layer in self.layers:
	    name = str(layer.name())
	    
	    html.append('\n\t' + name + '.events.on({\n\t\t"featureselected": function(e) {\n\t\t\tonFeatureSelect' + name + '(e.feature);\n\t\t},\n\t\t"featureunselected": function(e) {\n\t\t\tonFeatureUnselect' + name + '(e.feature);\n\t\t}\n\t});\n\t')
	return html
