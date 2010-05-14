
###########################################################################
###
# begin : 2010-04-20
# authors: Luca Delucchi
# copyright : (C) 2010 by luca delucchi, Fondazione Edmund Mach
# email : lucadeluge@gmail.com
###

###
# This program is free software; you can redistribute it and/or modify 
# it under the terms of the GNU General Public License as published by 
# the Free Software Foundation; either version 2 of the License. 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License (GPL) for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the
#  Free Software Foundation, Inc.,
#  59 Temple Place - Suite 330,
#  Boston, MA  02111-1307, USA.
###
############################################################################

import sys, os
import zipfile
import osgeo.ogr as ogr
import osgeo.osr as osr

def Ogr2Ogr(inputs,outputpath,outputEPSG,inputEPSG,outputFormat):
    #input file
    inDatasource = ogr.Open(inputs)
    #create datasource
    inLayer = inDatasource.GetLayer()
    #get layer name
    inLayerName = inLayer.GetName()
    #get first feature for the geometry type
    inFeature = inLayer.GetFeature(0)
    #found geometry type
    inGeomType = inFeature.GetGeometryRef().GetGeometryType()
    inGeomwkb = geometryType(inGeomType)
    #create output spatial reference system
    outSpatial = osr.SpatialReference()
    outSpatial.ImportFromEPSG(int(outputEPSG))
    #create the driver from input datasource
    outDriver = ogr.GetDriverByName(outputFormat)
    #output
    outputDSN = outputpath
    #search if the file already exist
    if os.path.exists(outputDSN):
	outDriver.DeleteDataSource(outputDSN)
    #create output datasource
    outDatasource = outDriver.CreateDataSource(outputDSN)
    #create output layer
    outLayer = outDatasource.CreateLayer(inLayerName, geom_type=inGeomwkb)
    #create output feature definition
    outFeatDefn = featureDefinition(inLayer,outLayer)
    #field's name list of input layer
    inFieldsName = fieldsName(inLayer)
    #loop inside the feature
    inFeatures = inLayer.GetNextFeature()
    while inFeatures: 
	#found geometry and trasform it in the output system reference system
	geom = inFeatures.GetGeometryRef()
	
	##########
	#settare la geometria a quella di input, variabile inputEPSG
	############

	geom.TransformTo(outSpatial)
	#create output feature
	outFeature = ogr.Feature(outFeatDefn)
	#add geometry to the feature
	outFeature.SetGeometry(geom)
	#add fields
	for field in inFieldsName:
	    outFeature.SetField(field, inFeatures.GetField(field))
	#add feature to the layer
	outLayer.CreateFeature(outFeature)
	#destroy input and output feature
	outFeature.Destroy()
	inFeatures.Destroy()             
	inFeatures = inLayer.GetNextFeature()
    #destroy input and output datasource
    inDatasource.Destroy()
    outDatasource.Destroy()

    return 3

#check the geometry type and return the ogr definition
def geometryType(geomType):
    if geomType==1:
	geomwkb = ogr.wkbPoint 
    elif geomType==2:
	geomwkb = ogr.wkbLineString
    elif geomType==3:
	geomwkb = ogr.wkbPolygon
    elif geomType==4:
	geomwkb = ogr.wkbMultiPoint
    elif geomType==5:
	geomwkb = ogr.wkbMultiLineString
    elif geomType==6:
	geomwkb = ogr.wkbMultiPolygon
    else:
	print "Some problem occurs in the geometry type"
	return 0
    return geomwkb

#return the output feature definition from the input definition
def featureDefinition(layer,outlayer):
    #out feature definition
    outFeatureDefn = ogr.FeatureDefn()
    #input feature definition
    featureDefn = layer.GetLayerDefn()
    for i in range(featureDefn.GetFieldCount()):
	#input field definition
	fieldDefn = featureDefn.GetFieldDefn(i)
	#create outlayer field definition IT'S VERY IMPORTANT
	outlayer.CreateField(fieldDefn)
	nameField = fieldDefn.GetName()
	typeField = fieldDefn.GetType()
	justiField = fieldDefn.GetJustify()
	widthField = fieldDefn.GetWidth()
	precField = fieldDefn.GetPrecision()
	#output field definition
	outField = ogr.FieldDefn()
	outField.SetName(nameField)
	outField.SetType(typeField)
	outField.SetJustify(justiField)
	outField.SetWidth(widthField)
	outField.SetPrecision(precField)
	outFeatureDefn.AddFieldDefn(outField)
    return outFeatureDefn

#return a list of field's name
def fieldsName(layer):
    #out list of fieldDefn
    fields = []
    featureDefn = layer.GetLayerDefn()
    for i in range(featureDefn.GetFieldCount()):
	#input field definition
	fieldDefn = featureDefn.GetFieldDefn(i)
	fields.append(fieldDefn.GetName())
    return fields
