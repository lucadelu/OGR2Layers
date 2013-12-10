#############################################
#       OGR2Layers Plugin (c)  for Quantum GIS                                  #
#       (c) Copyright Nicolas BOZON - 2008                                      #
#       Authors: Nicolas BOZON, Rene-Luc D'HONT, Michael DOUCHIN, Luca DELUCCHI #
#       Email: lucadeluge at gmail dot com                                      #
#                                                                               #
#############################################
#       OGR2Layers Plugin is licensed under the terms of GNU GPL 2              #
#       This program is free software; you can redistribute it and/or modify    #
#       it under the terms of the GNU General Public License as published by    #
#       the Free Software Foundation; either version 2 of the License, or       #
#       (at your option) any later version.                                     #
#       This program is distributed in the hope that it will be useful,         #
#       but WITHOUT ANY WARRANTY; without even implied warranty of              #
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.                    # 
#       See the GNU General Public License for more details.                    #
#############################################

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *

import os
import string

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
        #layer name
        self.name = self.layer.name()
        #layer output format
        self.outputFormat = outputFormat
        #putput vector name
        self.outputName = unicode(self.name + "." + self.outputFormat)
        #input epsg
        self.inEpsg = self.layer.crs().authid()
        #set the output epsg code
        self.outputEpsg = outProj
        #type of rendering
        self.rendering = rendering
        #type of query
        self.query = query
        #type of vector
        self.providerName = str(self.layer.dataProvider().name())
        #directory where save files
        self.pathSave = mydir
        #name of file to write
        self.destPathName =  os.path.abspath(os.path.join(self.pathSave,
                                                          self.outputName))
        #class query
        self.classQuery = OGR2LayersClassQuery(self.layer, self.query)

    def convertOGR(self):
        """Convert vector layer and set the variable for html file"""
        #TODO fix when WFS url will be correct
#        #add WFS
#        if (self.providerName == "WFS"):
#            #if the input and output epsg have the same projection add WFS
#            #like OpenLayers.Layer.WFS
#            if self.inEpsg == self.outputEpsg:
#                self.outputFormat = "WFS"
#                self.outputName = self.source
#            #else write shapefile from WFS and reproject it with the right
#            #projection and load it like OpenLayers.Layer.GML
#            else:
#                if self.writeShape():
#                    return 0
#                else:
#                    err = "A problem occurs during convertion of layer {l}".format(l=self.name)
#                    raise Exception, err
#        #add other vector type
#        else:
        self.writeShape()

    def writeShape(self):
        nameFile = os.path.abspath(os.path.join(str(self.pathSave),
        str(self.name) + '_temp.shp'))
        QgsVectorFileWriter.deleteShapeFile(nameFile)
        inputQgsReference = QgsCoordinateReferenceSystem()
        inputQgsReference.createFromOgcWmsCrs(self.outputEpsg)
        writeShape = QgsVectorFileWriter.writeAsVectorFormat(self.layer,
                                                             str(self.destPathName),
                                                             "UTF8",
                                                             inputQgsReference,
                                                             self.outputFormat)
        if writeShape == QgsVectorFileWriter.NoError:
            return True
        else:
            err = "A problem occurs during convertion of layer {l}".format(l=self.name)
            raise Exception, err

    def htmlStyle(self):
        """Create javascript code for style"""
        if self.rendering == 'qgis':
            try:
            #class rendering
                self.classStyle = OGR2LayersClassStyle(self.layer,
                                                       self.pathSave)
                self.image = self.classStyle.svg
                return self.classStyle.typeRendering()
            except Exception, e:
                raise Exception, e

    def logStyle(self):
        """Return the log string of style operation for output"""
        if self.rendering == 'qgis':
            try:
                #return the log string
                return self.classStyle.retLog()
            except Exception, e:
                raise Exception, e

    def htmlQuery(self):
        """Create javascript code for query"""
        return self.classQuery.createQuery()

    def htmlLayer(self):
        """Create the Javascript code for vector layer"""
        #TODO fix when WFS url will work
        if self.outputFormat == 'WFS':
            htmlLayer = ['var ' + self.name + ' = new OpenLayers.Layer.Vector'\
            + '("' + self.name + ' ' + self.outputFormat \
            + '", {\n\t\tprotocol: new OpenLayers.Protocol.WFS({\n\t\t\t' \
            + 'url: "' + self.outputName + '",\n\t\t\t' \
            + 'featureType: "' + self.outputName + '",']
            #add cluster strategy
            htmlLayer.append('\n\t\t})')
            htmlLayer.append(',\n\t\tstrategies: [\n\t\t\tnew OpenLayers.Strategy.BBOX()')
        else:
            htmlLayer = ['var ' + self.name + ' = new OpenLayers.Layer.Vector'\
            + '("' + self.name + ' ' + self.outputFormat \
            + '", {\n\t\tprotocol: new OpenLayers.Protocol.HTTP({\n\t\t\t' \
            + 'url: "' + self.outputName + '",\n\t\t\t']
            #if outputFormat is GeoJson
            if self.outputFormat == 'GeoJSON':
                #add the format
                htmlLayer.append('format: new OpenLayers.Format.GeoJSON()')
            elif self.outputFormat == 'GML':
                #add the format
                htmlLayer.append('format: new OpenLayers.Format.GML()')
            elif self.outputFormat == 'KML':
                #add the format
                htmlLayer.append('format: new OpenLayers.Format.KML()')
            #add cluster strategy
            htmlLayer.append('\n\t\t})')
            htmlLayer.append(',\n\t\tstrategies: [\n\t\t\tnew OpenLayers.Strategy.Fixed()')
        if self.query == 'cluster':
            htmlLayer.append(',\n\t\t\tnew OpenLayers.Strategy.Cluster()')
        htmlLayer.append('\n\t\t]')
        #if only qgis style it's choosen I must open {
        if self.rendering == 'qgis':
            htmlLayer.append(',\n\t\tstyleMap: ' + self.name + '_style')
        #for all it closes the layer ) and add it to the map
        htmlLayer.append('\n\t});\n\tmap.addLayer(' + self.name + ');\n\t')

        return htmlLayer
