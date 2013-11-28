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
from OGR2ClassLayer import *
from OGR2ClassQuery import OGR2LayersClassControlSel
#from GDAL2ClassLayer import *

class OGR2LayersClassHtml:
    """The class to create html and javascript code"""
    def __init__(self,
                  layers,
                  rasters,
                  dlg,
                  directory
                ):
        # layers = list of layers to insert in html code
        # dlg = dialog object
        # directory = directory where user want save data
        #the active ogr layers
        self.layers = layers
        #the active gdal layers
        self.rasters = rasters
        #the dialog
        self.dlg = dlg
        #the directory where save the data
        self.myDirectory = directory
        #type of query
        if self.dlg.ui.query.isChecked():
            self.myQuery = 'single'
        elif self.dlg.ui.query_2.isChecked():
            self.myQuery = 'cluster'
        else:
            self.myQuery = 'none'
        #the map baseLayer
        self.mapBaseLayer = self.dlg.ui.mapBaseLayer.currentIndex()
        # used for number of vector
        self.compteur = 0

    def createHtml(self):
        """Create the html code"""
        html = ['<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">\n']
        html.append('<html xmlns="http://www.w3.org/1999/xhtml">\n')
        html.append('<head>\n')
        html.append('<title>OGR2Layers</title>\n')
        #add style for map
        html.extend(self.olMapSize())
        #Call for OpenLayers 2.10 API on Metacarta servers
        html.append('<script src="http://www.openlayers.org/api/2.11/OpenLayers.js"></script>\n')
        if self.mapBaseLayer in [4, 5, 6, 7]:
            html.append('<script src="http://maps.google.com/maps/api/js?v=3.5&amp;sensor=false"></script> ')
        #start javascript code
        html.append('<script type="text/javascript">\n')
        #set a function to check if it is a url or not http://
        if self.myQuery != 'none':
            html.append('function urlCheck(str) {\n'\
                        '\tvar v = new RegExp();\n'\
                        '\tv.compile("^[A-Za-z]+://[A-Za-z0-9-_]+\\.[A-Za-z0-9-_%&\?\/.=]+$");\n'
                        '\tif (!v.test(str)) {\n\t\treturn "<i>"+str+"</i>";\n'\
                        '\t}\n\t\treturn "<a href=\"+str+\" target:\'_blank\'>open url</a>";\n};\n')
        #set global variable (map, selectsControls)
        html.append('var map, selectsControls\n')
        #start function for OL
        html.append('function init(){\n')
        #add the base layer
        html.extend(self.olBaseLayer())
        #add the controls
        html.extend(self.olControl())
        #try to add the code for layers
        try:
            if self.layers:
                #vector layer
                html.extend(self.htmlLayer())
            #if self.rasters:
                ##raster layer
                #html.extend(self.htmlRaster())
        #return errors
        except Exception, e:
            raise e
        #add the query
        if self.myQuery != 'none':
            html.extend(self.controlSel())
        html.extend(self.extentHtml())
        #close the init function
        html.append('};\n')
        #close javascript script and start body where is loaded init function
        html.append('</script>\n</head>\n<body onload="init()">\n')
        #Generate H1 Map Title
        mapTitle = self.dlg.ui.mapTitle.text()
        html.append('<h1>' + mapTitle + '</h1>\n')
        #add the map and close the html file
        html.append('<div id="map"></div>\n</body>\n</html>\n')
        return html

    def olMapSize(self):
        #add the style of map (dimension)
        mapSize = self.dlg.ui.mapSize.currentIndex()
        if (mapSize) == 0:   # 400x400
            return '<style>\n #map{width:400px;height:400px;}\n</style>\n'
        elif (mapSize) == 1:   # 800x600
            return '<style>\n #map{width:800px;height:600px;}\n</style>\n'
        elif (mapSize) == 2:   # full screen
            return '<style>\n #map{width:100%;height:1024px;}\n</style>\n'

    def extentHtml(self):
        """add coordinate transformation to 900913 if baseLayer is OSM"""
        # User defined Bounds
        xmin = self.dlg.ui.lineEdit.text()
        xmax = self.dlg.ui.lineEdit_2.text()
        ymin = self.dlg.ui.lineEdit_3.text()
        ymax = self.dlg.ui.lineEdit_4.text()
        # set the extent with osm projection
        if (self.mapBaseLayer) == 0 or (self.mapBaseLayer) < 8:
            html = ['extent = new OpenLayers.Bounds(' + str(xmin) + ',' + \
                    str(xmax) + ',' + str(ymin) + ',' + str(ymax) + ').' \
                    'transform(new OpenLayers.Projection("EPSG:4326"), new ' \
                    'OpenLayers.Projection("EPSG:900913"));\n\t']
        # set the extent to latlong
        else:
            html = ['extent = new OpenLayers.Bounds(' + str(xmin) + ',' +
                    str(xmax) + ',' + str(ymin) + ',' + str(ymax) + ');\n\t']
        # set the zoom of the map to extent
        html.append('map.zoomToExtent(extent);\n')
        if self.dlg.ui.maxExtent.isChecked():
            html.append('\tmap.maxExtent(extent);\n')
            #AGGIUNGERE IL CODICE PER IL MAX EXTEND
        return html

    def olBaseLayer(self):
        """Define the baseLayer"""

        # set the projection options for the map
        if (self.mapBaseLayer) == 0 or (self.mapBaseLayer) < 8:
            html = ['\tvar option = {\n\t\tprojection: new '\
            'OpenLayers.Projection("EPSG:900913"),\n\t\tdisplayProjection: new OpenLayers.Projection("EPSG:4326")\n\t};\n\t']
            html.append("map = new OpenLayers.Map('map', option);\n\t")
            self.projection = "EPSG:900913"
        else:
            html = ["map = new OpenLayers.Map('map');\n\t"]
            self.projection = "EPSG:4326"
        #Save chose Map Base Layer
        if (self.mapBaseLayer) == 0:  # OpenStreetMap (Mapnik)
            html.append('var attribution = {attribution:"&copy; <a href=\'http://www.openstreetmap.org/copyright\'>OpenStreetMap</a> contributors"};')
            html.append('olmapnik = new OpenLayers.Layer.OSM("OpenStreetMap Mapnik", "http://tile.openstreetmap.org/${z}/${x}/${y}.png", attribution);\n\t')
            html.append('map.addLayer(olmapnik);\n\t')
            html.append('map.setBaseLayer(olmapnik);\n\t')
        elif (self.mapBaseLayer) == 1:  # OpenStreetMap (Osmarender)
            html.append('olosma = new OpenLayers.Layer.OSM("OpenStreetMap Osmarender", "http://tah.openstreetmap.org/Tiles/tile/${z}/${x}/${y}.png");\n\t')
            html.append('map.addLayer(olosma);\n\t')
            html.append('map.setBaseLayer(olosma);\n\t')
        elif (self.mapBaseLayer) == 2:  # OpenStreetMap (Cycleway)
            html.append('osm = new OpenLayers.Layer.OSM("OpenStreetMap Cycleway", "http://a.andy.sandbox.cloudmade.com/tiles/cycle/${z}/${x}/${y}.png");\n\t')
            html.append('map.addLayer(osm);\n\t')
            html.append('map.setBaseLayer(osm);\n\t')
        elif (self.mapBaseLayer) == 3:  # OpenLayers WMS
            html.append('olwms = new OpenLayers.Layer.WMS( "OpenLayers WMS", ["http://labs.metacarta.com/wms/vmap0"], {layers: "basic", format: '\
            '"image/gif" } );\n\t')
            html.append('map.addLayer(olwms);\n\t')
            html.append('map.setBaseLayer(olwms);\n\t')
        elif (self.mapBaseLayer) == 4:  # Google Streets
            html.append('gtile = new OpenLayers.Layer.Google('\
            ' "Google Streets", {numZoomLevels: 20} );\n\t')
            html.append('map.addLayer(gtile);\n\t')
            html.append('map.setBaseLayer(gtile);\n\t')
        elif (self.mapBaseLayer) == 5:  # Google Physical
            html.append('gphy = new OpenLayers.Layer.Google('\
            ' "Google Physical", {type: google.maps.MapTypeId.TERRAIN} );\n\t')
            html.append('map.addLayer(gphy);\n\t')
            html.append('map.setBaseLayer(gphy);\n\t')
        elif (self.mapBaseLayer) == 6:  # Google Hybrid
            html.append('ghyb = new OpenLayers.Layer.Google('\
            ' "Google Hybrid", {type: google.maps.MapTypeId.HYBRID, numZoomLevels: 20} );\n\t')
            html.append('map.addLayer(ghyb);\n\t')
            html.append('map.setBaseLayer(ghyb);\n\t')
        elif (self.mapBaseLayer) == 7:  # Google Satellite
            html.append('gsat = new OpenLayers.Layer.Google('\
            ' "Google Satellite", {type: google.maps.MapTypeId.SATELLITE, numZoomLevels: 22} );\n\t')
            html.append('map.addLayer(gsat);\n\t')
            html.append('map.setBaseLayer(gsat);\n\t')
        elif (self.mapBaseLayer) == 8:  # Demis WMS
            html.append('bmwms = new OpenLayers.Layer.WMS( "Demis WMS", ["http://www2.demis.nl/WMS/wms.asp?wms=WorldMap"], {layers: "Bathymetry,Countries,Topography,Hillshading,Builtup+areas,Coastlines,Waterbodies,Inundated,Rivers,Streams,Railroads,Highways,Roads,Trails,Borders,Cities,Settlements"} );\n\t')
            html.append('map.addLayer(bmwms);\n\t')
            html.append('map.setBaseLayer(bmwms);\n\t')
        return html

    def olControl(self):
        """Layer Switcher active or not and add the chosen control"""
        # set the index of layer switcher
        layerSwitcherActive = self.dlg.ui.layerSwitcherActive.currentIndex()
        #it's active
        if layerSwitcherActive == 0:
            html = ['var ls= new OpenLayers.Control.LayerSwitcher(); \n\tmap.addControl(ls); \n\tls.maximizeControl(); \n\t']
        #is not active
        elif layerSwitcherActive == 1:
            html = ['map.addControl(new OpenLayers.Control.LayerSwitcher());\n\t']
        #--mouseposition
        if self.dlg.ui.mousepos.isChecked():
            html.append('map.addControl(new OpenLayers.Control.MousePosition());\n\t')
        ##--scale
        if  self.dlg.ui.scale.isChecked():
            html.append('map.addControl(new OpenLayers.Control.Scale());\n\t')
        ##--permalink
        if self.dlg.ui.permalink.isChecked():
            html.append('map.addControl(new OpenLayers.Control.Permalink());\n\t')
        ##--attribution
        if  self.dlg.ui.copyr.isChecked():
            html.append('map.addControl(new OpenLayers.Control.Attribution());\n\t')
        ##--overviewmap
        if  self.dlg.ui.navi.isChecked():
            html.append('map.addControl(new OpenLayers.Control.OverviewMap());\n\t')
        ##--panZoomBar
        if  self.dlg.ui.zoomBar.isChecked():
            html.append('map.addControl(new OpenLayers.Control.PanZoomBar());\n\t')
        ##--navigation  
        html.append('map.addControl(new OpenLayers.Control.Navigation());\n\t')
        return html

    def outFormatLayer(self):
        """The output format chosen"""
        # set the indix of output type
        layerSwitcherOutput = self.dlg.ui.outputFormCombo.currentIndex()
        # GeoJSON format
        if layerSwitcherOutput == 0:
            outputFormat = 'GeoJSON'
        # GML format
        elif layerSwitcherOutput == 1:
            outputFormat = 'GML'
        return outputFormat

    def htmlLayer(self):
        """Add the code for layer, name, style and query"""
        # variable to write html code
        html = []
        # variable to the string in the output tab
        layerString = ""
        # set the output format
        outputFormat = self.outFormatLayer()
        # cycle for each layer
        for layer in self.layers:
            # start the string for the layer to add in the output panel
            stringLayer = 'The vector <b>' + str(layer.name()) + '</b>'\
            ' is converted correctly'
            # check if qgis renderer is chosen
            if self.dlg.ui.qgisRender.isChecked():
                # set my rendering
                myRendering = 'qgis'
                stringLayer = stringLayer + ', using QGIS rendering'
            else:
                myRendering = 'default'
            #check the type of quert
            if self.myQuery == 'single':
                stringLayer = stringLayer + ' with single query'
            elif self.myQuery == 'cluster':
                #check if geometry type is point
                if layer.geometryType() == 0:
                    rendererName = False
                    #try used because two different function of old and new symbology
                    #check if symbology is single or not
                    try:
                        if layer.renderer().name() == 'Single Symbol':
                            rendererName = True
                    except:
                        if layer.rendererV2().type() == 'singleSymbol':
                            rendererName = True
                    if myRendering == 'qgis' and rendererName:
                        stringLayer = stringLayer + ' with cluster strategy query'
                    elif myRendering == 'default':
                        stringLayer = stringLayer + ' with cluster strategy query'
                    elif myRendering == 'qgis' and not rendererName:
                        #return an error if the symbology is different from Single Symbol
                        raise Exception, "Classification doesn't work with Cluster Strategy\n"
                        break
                #geometry it isn't point
                else:
                    raise Exception, "Cluster Strategy support only vector point\n"
                    break

            OGR2LayersLayer = OGR2LayersClassLayer(layer, myRendering,
                                                   self.myQuery, outputFormat,
                                                   self.projection,
                                                   self.myDirectory)
            if myRendering == 'qgis':
                try:
                    html.extend(OGR2LayersLayer.htmlStyle())
                    #OGR2LayersLayer.logStyle()
                    stringLayer = stringLayer + '<br />' + OGR2LayersLayer.logStyle()
                except Exception, e:
                    raise e
            if self.myQuery != 'none':
                html.extend(OGR2LayersLayer.htmlQuery())
            try:
                OGR2LayersLayer.convertOGR()
            except Exception, e:
                raise e
            html.extend(OGR2LayersLayer.htmlLayer())
            #add the string to textBrowser
            stringLayer = stringLayer + '<br />'
            #add the string to textBrowser
            layerString = layerString + stringLayer
            self.compteur = self.compteur + 1
            self.dlg.ui.progressBar.setValue(self.compteur)

        self.dlg.ui.textBrowserLayer.setHtml(layerString)
        return html

    def controlSel(self):
        """Add the code for have all layer queryable"""
        classControl = OGR2LayersClassControlSel(self.layers)
        return classControl.htmlSelectControl()

    def outFormatRaster(self):
        """The output format chosen"""

        # set the indix of output type
        layerSwitcherOutput = self.dlg.ui.outputRasterCombo.currentIndex()
        # PNG format
        if layerSwitcherOutput == 0:
            outputFormat = 'PNG'
        # JPEG format
        elif layerSwitcherOutput == 1:
            outputFormat = 'JPEG'
        return outputFormat

    def htmlRaster(self):
        # variable to write html code
        html = []
        # variable to the string in the output tab
        layerString = ""
        # set the output format
        outputFormat = self.outFormatRaster()
        # cycle for each layer
        for raster in self.rasters:
            # start the string for the layer to add in the output panel
            stringLayer = 'The raster <b>' + str(raster.name()) + '</b>'\
            ' is converted correctly'
            #GDAL2LayersLayer = GDAL2LayersClassLayer(layer,outputFormat,
            #                   self.projection, self.myDirectory)
            #add the string to textBrowser
            layerString = layerString + stringLayer
            self.compteur = self.compteur + 1
            self.dlg.ui.progressBar.setValue(self.compteur)
            #GDAL2LayersLayer = GDAL2LayersClassLayer(layer, outputFormat, self.projection, self.myDirectory)
            #GDAL2LayersLayer.convert()
            #html.extend(GDAL2LayersLayer.htmlLayer())

        self.dlg.ui.textBrowserRaster.setHtml(layerString)
        return html
