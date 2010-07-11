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

#create javascript code for query
def createQuery(layer,typeQuery):
    #set the field name of the vector
    fieldsLayer=fieldsName(layer)
    #start javascript code for the query (add selectControl)
    html_query=['//START QUERY '+layer.name()+'\n\tvar selectControl'+layer.name()+' = new OpenLayers.Control.SelectFeature(\n\t\t'+layer.name()+', {\n\t\t\tonSelect: onFeatureSelect'+layer.name()+',\n\t\t\tonUnselect: onFeatureUnselect'+layer.name()+'\n\t\t}\n\t);\n\tmap.addControl(selectControl'+layer.name()+');\n\t//selectControl'+layer.name()+'.activate();\n\t']
    #add function for close the popup
    html_query.append('function onPopupClose'+layer.name()+'(evt) {\n\t\tselectControl'+layer.name()+'.unselect(selectedFeature);\n\t}\n\t')
    #add function for features selected
    html_query.append('function onFeatureSelect'+layer.name()+'(feature) {\n\t\tselectedFeature = feature;') 
    #check the typo of query
    if (typeQuery==0):
	#simple query
	html_query.extend(htmlTable(fieldsLayer,layer))
    else:
	#query with cluster strategy
	html_query.extend(htmlTableCluster(fieldsLayer,layer))
    #add popup to the function for features selected
    html_query.append('\n\t\tpopup = new OpenLayers.Popup.FramedCloud("chicken", \n\t\t\tfeature.geometry.getBounds().getCenterLonLat(),\n\t\t\tnew OpenLayers.Size(1000,500),\n\t\t\ttable'+layer.name()+',\n\t\t\tnull,\n\t\t\ttrue,\n\t\t\tonPopupClose'+layer.name()+'\n\t\t); \n\t\tfeature.popup = popup;\n\t\tmap.addPopup(popup);\n\t}\n\t')
    #create function for unselect features
    html_query.append('function onFeatureUnselect'+layer.name()+'(feature) {\n\t\tmap.removePopup(feature.popup);\n\t\tfeature.popup.destroy();\n\t\tfeature.popup = null;\n\t}\n\t//STOP QUERY '+layer.name()+'\n\t');
    #return javascript code for the query
    return html_query

#read all the fields of a vector
def fieldsName(layer):
    #dataprovider for the layer
    vprovider = layer.dataProvider()
    #fields of a layer (in number)
    fields = vprovider.fields()
    nameFields=[]
    for i in fields:
	#add the name of field
	nameFields.append(fields[i].name())
    #return a list with the name of fields
    return nameFields

#create html table for the single query
def htmlTable(fields,layer):
    #add javascript table for popup
    html=['\n\t\ttable'+layer.name()+'="<html><meta http-equiv=\'Content-Type\' content=\'text/html; charset=UTF-8\'><body><table>']
    #for each field add a column for the feature
    for field in fields:
	html.append('<tr><td><b>'+field+':</b></td><td><i>"+feature.attributes.'+field+'+"</i></td></tr>')
    html.append('</table></body></html>"; ')
    #return javascript code
    return html

#create html table for the query using cluster strategy
def htmlTableCluster(fields,layer):
    #start table
    html=['\n\t\ttable'+layer.name()+'="<html><meta http-equiv=\'Content-Type\' content=\'text/html; charset=UTF-8\'><body><table><tr bgcolor=\'#c5e2ca\'>']
    #for each field add a column with the name of the field
    for field in fields:
	html.append('<td>'+field+'</td>')
    #finisc the caption row
    html.append('</tr>";')
    #add javascript code for all features select create a row
    html.append('\n\t\tfor (var i=0; i < feature.cluster.length; ++i){\n\t\t\ttable'+layer.name()+'+="<tr>')
    #for each field add a column in the row of selected features
    for field in fields:
	html.append('<td>"+feature.cluster[i].attributes.'+field+'+"</td>')
    html.append('</tr>"\n\t\t}\n\t\ttable'+layer.name()+'+="</table></body></html>"; ')
    #return javascript code
    return html

#function for add a javascript variable, it contain the selectControl for all layer
def addselectsControls(layers):
    #start html code
    html=['selectsControls=[']
    cont=0
    #for each layer append the selectControl
    for layer in layers:
	if cont==0:
	    html.append('selectControl'+layer.name())
	else:
  	    html.append(', selectControl'+layer.name())
	cont=cont+1
    html.append('];\n\t')
    #return javascript code
    return html