# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 00:34:38 2013

@author: lucadelu
"""


class GDAL2LayersClassLayer:
    """A class to convert and add layer to the file
        layer = QGIS layer
    """
    def __init__(self,
                  layer
                ):
        #qgis layer
        self.layer = layer
        #qgis layer source
        self.source = self.layer.source()
        s = self.source.split('&')
        self.sourcedict = dict((k.split('=')[0], k.split('=')[1]) for k in s)
        #layer name
        self.name = self.layer.name()

    def htmlLayer(self):
        """Create the Javascript code for raster layer"""
        if self.layer.dataProvider().name() == 'wms':
            htmlLayer = ['var ' + self.name + ' = new OpenLayers.Layer.WMS' \
            '("' + self.name + ' WMS",\n\t\t"' + self.sourcedict['url'] + '"' \
            ', \n\t\t{\n\t\t\tlayers: "' + self.sourcedict['layers'] + '",' \
            '\n\t\t\tformat: "' + self.sourcedict['format'] + '"' \
            '\n\t\t}, {\n\t\t\tisBaseLayer: false\n\t\t});']
        htmlLayer.append('\n\tmap.addLayer(' + self.name + ');\n\t')

        return htmlLayer
        