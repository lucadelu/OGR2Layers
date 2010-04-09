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
    html_query=['//START QUERY '+layer.name()+'\n\tvar selectControl'+layer.name()+' = new OpenLayers.Control.SelectFeature('+layer.name()+', {onSelect: onFeatureSelect'+layer.name()+', onUnselect: onFeatureUnselect'+layer.name()+'});\n\t map.addControl(selectControl'+layer.name()+');\n\t selectControl'+layer.name()+'.activate();\n\t']
    html_query.append('function onPopupClose'+layer.name()+'(evt) {selectControl'+layer.name()+'.unselect(selectedFeature);}\n\t')
    html_query.append('function onFeatureSelect'+layer.name()+'(feature) {selectedFeature = feature; ') 
    if (typeQuery==0):
	html_query.extend(htmlTable(fieldsLayer,layer))
    else:
	html_query.extend(htmlTableCluster(fieldsLayer,layer))
    html_query.append('popup = new OpenLayers.Popup.FramedCloud("chicken", feature.geometry.getBounds().getCenterLonLat(), new OpenLayers.Size(1000,500),tabella'+layer.name()+', null, true, onPopupClose'+layer.name()+'); feature.popup = popup; map.addPopup(popup);}\n\t')
    html_query.append('function onFeatureUnselect'+layer.name()+'(feature) {map.removePopup(feature.popup); feature.popup.destroy(); feature.popup = null;}\n\t//STOP QUERY '+layer.name()+'\n\t')
    return html_query

#read all the fields of a vector
def fieldsName(layer):
    vprovider = layer.dataProvider()
    fields = vprovider.fields()
    nameFields=[]
    for i in fields:
	nameFields.append(fields[i].name())
    return nameFields

def htmlTable(fields,layer):
    html=['tabella'+layer.name()+'="<html><meta http-equiv=\'Content-Type\' content=\'text/html; charset=UTF-8\'><body><table>']
    for field in fields:
	html.append('<tr><td><b>'+field+':</b></td><td><i>"+feature.attributes.'+field+'+"</i></td></tr>')
    html.append('</table></body></html>"; ')
    return html

def htmlTableCluster(fields,layer):
    html=['tabella'+layer.name()+'="<html><meta http-equiv=\'Content-Type\' content=\'text/html; charset=UTF-8\'><body><table><tr bgcolor=\'#c5e2ca\'>']
    for field in fields:
	html.append('<td>'+field+'</td>')
    html.append('</tr>";')
    html.append('for (var i=0; i < feature.cluster.length; ++i){tabella+="<tr>')
    for field in fields:
	html.append('<td>"+feature.cluster[i].attributes.'+field+'+"</td>')
    html.append('</tr>"}tabella+="</table></body></html>"; ')
    return html
    