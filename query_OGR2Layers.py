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

#def returnLayers(layers):
    #queries:[]
    #for layer in layers:
	#if 

#create javascript code for query
def createQuery(layer,typeQuery):
    fieldsLayer=fieldsName(layer)
    html_query=['//START QUERY '+layer.name()+'\nvar selectControl = new OpenLayers.Control.SelectFeature('+layer.name()+', {onSelect: onFeatureSelect, onUnselect: onFeatureUnselect});\n map.addControl(selectControl);\n selectControl.activate();\n']
    html_query.append('function onPopupClose(evt) {selectControl.unselect(selectedFeature);}\n')
    html_query.append('function onFeatureSelect(feature) {selectedFeature = feature; ') 
    if (typeQuery==0):
	html_query.extend(htmlTable(fieldsLayer))
    else:
	html_query.extend(htmlTableCluster(fieldsLayer))
    html_query.append('popup = new OpenLayers.Popup.FramedCloud("chicken", feature.geometry.getBounds().getCenterLonLat(), new OpenLayers.Size(1000,500),tabella, null, true, onPopupClose); feature.popup = popup; map.addPopup(popup);}\n')
    html_query.append('function onFeatureUnselect(feature) {map.removePopup(feature.popup); feature.popup.destroy(); feature.popup = null;}\n//STOP QUERY '+layer.name()+'\n')
    return html_query

#read all the fields of a vector
def fieldsName(layer):
    vprovider = layer.dataProvider()
    fields = vprovider.fields()
    nameFields=[]
    for i in fields:
	nameFields.append(fields[i].name())
    return nameFields

def htmlTable(fields):
    html=['tabella="<html><meta http-equiv=\'Content-Type\' content=\'text/html; charset=UTF-8\'><body><table>']
    for field in fields:
	html.append('<tr><td><b>'+field+':</b></td><td><i>"+feature.attributes.'+field+'+"</i></td></tr>')
    html.append('</table></body></html>"; ')
    return html

def htmlTableCluster(fields):
    html=['tabella="<html><meta http-equiv=\'Content-Type\' content=\'text/html; charset=UTF-8\'><body><table><tr bgcolor=\'#c5e2ca\'>']
    for field in fields:
	html.append('<td>'+field+'</td>')
    html.append('</tr>";')
    html.append('for (var i=0; i < feature.cluster.length; ++i){tabella+="<tr>')
    for field in fields:
	html.append('<td>"+feature.cluster[i].attributes.'+field+'+"</td>')
    html.append('</tr>"}tabella+="</table></body></html>"; ')
    return html
    