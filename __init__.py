#############################################
#       OGR2Layers Plugin (c)  for Quantum GIS                                #
#       (c) Copyright Nicolas BOZON - 2008                                    #
#       Authors: Luca DELUCCHI, Nicolas BOZON, Rene-Luc D'HONT,               #
#                Michael DOUCHIN, Mathias Walker                              #
#       Email: lucadeluge at gmail dot com                                    #
#                                                                             #
#############################################
#       OGR2Layers Plugin is licensed under the terms of GNU GPL 2            #
#       This program is free software; you can redistribute it and/or modify  #
#       it under the terms of the GNU General Public License as published by  #
#       the Free Software Foundation; either version 2 of the License, or     #
#       (at your option) any later version.                                   #
#       This program is distributed in the hope that it will be useful,       #
#       but WITHOUT ANY WARRANTY; without even implied warranty of            #
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.                  # 
#       See the GNU General Public License for more details.                  #
#############################################


def name():
    return "OGR2Layers"


def description():
    return " A plugin to export OGR layers to OpenLayers HTML"


def version():
    return "Version 0.9.0"


def qgisMinimumVersion():
    return "2.0"


def authorName():
    return "Luca DELUCCHI, Nicolas BOZON, Rene-Luc D'HONT, Michael DOUCHIN," \
           "Mathias Walker"


def icon():
    return "icongui.png"


def classFactory(iface):
    from ogr2Layers import OGR2Layers
    return OGR2Layers(iface)
