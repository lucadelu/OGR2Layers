# -*- coding: utf-8 -*-
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

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
import ogr2ogr
import sys
import os
#import urllib2
import string

def createOGR(layer,ui,mydir,iface):
    """ Convert ogr layer to gml - geojson; 
    it's used in ogr2Layer class OGR2Layer function writeKML at line 227
    layer = input layer
    ui = ui 
    mydir = path where files are writeKML
    iface = qgis interface
    """
    #the number of last tab
    lastTab=ui.tabWidget.count()-1
    if layer and layer.type() == QgsMapLayer.VectorLayer:
	#source of each vector layer (postgres, shapefile path, etc.)
	mysource = layer.source()
	#IT'S IMPORTANT: when it's used unique value classification in the source 
	#add this string layerid='number' with this code remove it
	mysource.remove(QRegExp('\|layerid=[\d]+$'))
	#layer name
	myname = layer.name()
	#layer provider (ogr, postgres, etc.)
	myprovider = layer.dataProvider()
	myprovidername = myprovider.name()
	#layer EpsgCrsId projection
	mysrs = myprovider.crs() #layer spatial reference system
	myepsg = mysrs.epsg()
	myproj4 = mysrs.toProj4()
	#read base layer for choose the projection
	mapBaseLayer = ui.mapBaseLayer.currentIndex()
	if (mapBaseLayer) == 0 or (mapBaseLayer) < 3:
	    #wkt for 900913 EPSG
	    outputepsg = '900913'
	    #outputepsg = 'PROJCS["Google Maps Global Mercator",GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.01745329251994328,AUTHORITY["EPSG","9122"]],AUTHORITY["EPSG","4326"]],PROJECTION["Mercator_2SP"],PARAMETER["standard_parallel_1",0],PARAMETER["latitude_of_origin",0],PARAMETER["central_meridian",0],PARAMETER["false_easting",0],PARAMETER["false_northing",0],UNIT["Meter",1],EXTENSION["PROJ4","+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +wktext  +no_defs"],AUTHORITY["EPSG","900913"]]'
	else:
	    #wkt for 4326 EPSG
	    outputepsg = '4326'
	    #outputepsg = 'GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EpsgCrsId","7030"]],AUTHORITY["EpsgCrsId","6326"]],PRIMEM["Greenwich",0,AUTHORITY["EpsgCrsId","8901"]],UNIT["degree",0.01745329251994328,AUTHORITY["EpsgCrsId","9122"]],AUTHORITY["EpsgCrsId","4326"]]'
	#destination of file
	#mydestpath = os.path.abspath(os.path.join(str(mydir),str(myname)+".gml"))

	layerSwitcherActive = ui.outputFormCombo.currentIndex()
	# GeoJSON format
	if layerSwitcherActive == 0:
	    outputFormat='GeoJSON'
	    mydestpath = os.path.abspath(os.path.join(str(mydir),str(myname)+".json"))
	# GML format
	elif layerSwitcherActive == 1:
	    outputFormat='GML'
	    mydestpath = os.path.abspath(os.path.join(str(mydir),str(myname)+".gml"))
	# KML format ###still does not work
	#elif layerSwitcherActive == 2:
	    #outputFormat='KML'
	    #mydestpath = os.path.abspath(os.path.join(str(mydir),str(myname)+".kml"))

	if (myproj4 != '' ): #process only vector layers with a well known srs
	#use ogr2ogr to create kml file
	    if (str(myprovidername)=="postgres"): #postgresql
		mypglayerinfo = mysource.split('table')[0]
		#new converter TO CHECK
		#ogr2ogr.Ogr2Ogr(str(mysource),mydestpath,outputepsg,myproj4,outputFormat)

		######old convert
		#myogr2ogr = 'ogr2ogr -a_srs EpsgCrsId:'+str(myepsg)+' -t_srs \''+str(outputepsg)+'\' -overwrite -f "GML" "'+str(mydestpath)+'" PG:"' + str(mypglayerinfo) + '" layer ' + str(myname) + ' 2>&1 > $HOME/.ogr2layers/ogr2layers.log'
		#res=os.popen(myogr2ogr).readlines()
		
		#for spatialite
	    elif (str(myprovidername)=="spatialite"):
		mysource_temp = mysource.split(' ')[0]
		mysource_temp = str(mysource_temp.split('=')[1])
		mysource_ogr_format = mysource_temp.replace("'","")
		ogr2ogr.Ogr2Ogr(mysource_ogr_format,mydestpath,outputepsg,myproj4,outputFormat)
	      
	    elif (str(myprovidername)=="ogr"): #ogr
		ogr2ogr.Ogr2Ogr(str(mysource),mydestpath,outputepsg,myproj4,outputFormat)

		#####old convert
		#myogr2ogr = 'ogr2ogr -a_srs "' + str(myproj4) + '" -t_srs \''+str(outputepsg)+'\' -overwrite -f "GML" "' + str(mydestpath) + '" "'+ str(mysource) +'" 2>&1 > $HOME/.ogr2layers/ogr2layers.log'
		#res=os.popen(myogr2ogr).readlines()
		#####
	    #add grass
	    elif (str(myprovidername)=="grass"): #grass
		mysource_temp = str(mysource).split('/')[0:-1]
		mysource_temp.insert(-1,"vector")
		mysource_temp.append("head")
		mysource_ogr_format = string.join(mysource_temp,'/')
		ogr2ogr.Ogr2Ogr(mysource_ogr_format,mydestpath,outputepsg,myproj4,outputFormat)

	    else: #do nothing and warn the user for unsupportade providers
		QMessageBox.information(iface.mainWindow(),"Information",str("Only postgres and ogr providers are supported") )
		return 0
	    #take the string of textBrowser and add new layer and ogr2ogr string
	    layerString=ui.textBrowser.toHtml()
	    layerString.append("""<b>%s</b> was reprojected correctly<br />""" % (myname))
	    ui.textBrowser.setHtml(layerString)
	    #set the last tab for show the string
	    #ui.tabWidget.setCurrentIndex(lastTab)
	    return 1
	else:
	    #message for unknown spatial reference system
	    QMessageBox.information(iface.mainWindow(),"Information","The layer " + str(myname) + " has an unknown spatial reference system." )
	    return 0
    else:
	#message for not supportaded vector
	QMessageBox.information(iface.mainWindow(),"Information",str("Only PostGIS, and OGR data provider layers are supported, GRASS and Spatialite layers are coming") )
	return 0

##FUNCTION FOR WFS LAYER still does not work
def writeWFS(layer,projection,style=True):
    source = layer.source()
    regexVers = QRegExp('\&VERSION=([\d]+\.[\d]+\.[\d]+)')
    regexFeat = QRegExp('\&TYPENAME=([^\&]+$?)')
    regexUrl = QRegExp('^(.+)[\?\&]SERVICE=WFS')
    regexUrlC = QRegExp('^(.+)SERVICE=WFS')
    if regexVers.indexIn(source) > -1:
	version=regexVers.cap(1)
    else:
	QMessageBox.information(self.iface.mainWindow(),"Information",str("WFS is not compatible") )
    if regexFeat.indexIn(source) > -1:
	feature=regexFeat.cap(1)
    else:
	QMessageBox.information(self.iface.mainWindow(),"Information",str("WFS is not compatible") )
    if regexUrl.indexIn(source) > -1:
	url=regexUrl.cap(1)
    else:
	QMessageBox.information(self.iface.mainWindow(),"Information",str("WFS is not compatible") )
    if regexUrlC.indexIn(source) > -1:
	urlC=regexUrlC.cap(1)
	urlCapabilities = ""+urlC+"SERVICE=WFS&VERSION="+version+"&REQUEST=GetCapabilities"
	getCapabilities = urllib2.urlopen(urlCapabilities)
    else:
	QMessageBox.information(self.iface.mainWindow(),"Information",str("WFS is not compatible") )

    #htmlWFS=['map.addLayer(new OpenLayers.Layer.Vector("'+layer.name()+' WFS", {' \
	#'strategies: [new OpenLayers.Strategy.BBOX()],' \
	#'protocol: new OpenLayers.Protocol.WFS({'\
	#'version: "'+version+'",'\
	#'srsName: "EPSG:'+str(layer.srs().epsg())+'", '\
	#'url:  \''+url+'\','\
	#'featureType: "'+feature+'"'\
    #'}),']
    #if style:
	#htmlWFS.append('projection: "'+projection+'",'\
	#'styleMap:"'+layer.name()+'_style"'\
	#'}))\n;'\
	#)
    #else:
	#htmlWFS.append('projection: "'+projection+'",'\
	#'}))\n;'\
	#)

    htmlWFS=['map.addLayer(new OpenLayers.Layer.WFS("'+layer.name()+' WFS", "'+url+'", ' \
	'{typename: "'+feature+'", srsName: "EPSG:'+str(layer.srs().epsg())+'"}, ']
    if style:
	htmlWFS.append('{projection: "'+projection+'", styleMap: "'+layer.name()+'_style"}))\n')
    else:
	htmlWFS.append('{projection: "'+projection+'"}))\n')

    return htmlWFS