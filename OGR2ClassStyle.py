# -*- coding: utf-8 -*-
#############################################
#	OGR2Layers Plugin (c)  for Quantum GIS					
#	(c) Copyright Luca Delucchi 2010					
#	Authors: Luca DELUCCHI							
#	Email: lucadelucchi_at_gmail_dot_com					
#										
#############################################
#    OGR2Layers Plugin is licensed under the terms of GNU GPL 2			
#  	This program is free software; you can redistribute it and/or modify	
# 	 it under the terms of the GNU General Public License as published by	
# 	 the Free Software Foundation; either version 2 of the License, or	
# 	 (at your option) any later version.					
#	This program is distributed in the hope that it will be useful,		
#	 but WITHOUT ANY WARRANTY; without even implied warranty of		
# 	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.			 
# 	 See the GNU General Public License for more details.			
#############################################

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *

import os, sys
import os2emxpath

from OGR2Funz import *

class OGR2LayersClassStyle:
  """A class to create style of layer and the relative code"""
  def __init__(self, 
		layer,
		directory
	      ):
    #qgis layer
    self.layer = layer
    # layer geometry type
    self.typeGeom = self.layer.geometryType()
    #layer name
    self.name = self.layer.name()
    # path to save image from svg
    self.path = directory
    # layer renderer
    if self.layer.renderer() != None:
      self.version = 1
      self.renderer = self.layer.renderer()
      #type of rendering
      self.typeRend = str(self.renderer.name())
      if self.typeRend != 'Single Symbol':
	self.numFieldClass = self.renderer.classificationAttributes()[0]
	self.nameField = nameAttrField(self.layer,self.numFieldClass)
    elif self.layer.rendererV2() != None:
      #raise Exception, "New symbology is not yet implement, it'll be soon ready\n"
      self.version = 2
      self.renderer = self.layer.rendererV2()
      #type of rendering
      self.typeRend = str(self.renderer.type()) 
      if self.typeRend != 'singleSymbol':
	self.nameField = str(self.renderer.classAttribute())
    else:
      raise Exception, "There are some problem with the rendering\n"
    # data provider
    self.provider = self.layer.dataProvider()
    self.svg = False
    self.log = ""
    
  def typeRendering(self):
    """Choose the function for each rendering type"""
    ##if Continuous Color
    if self.version == 1:
      return self.typeV1()
    elif self.version == 2:
      return self.typeV2()
    else:
      raise Exception, "There are some problem with the rendering\n"

  def typeV1(self):
    if self.typeRend == 'Continuous Color':
      return self.contColor()
    ##if Graduated Symbol
    if self.typeRend == 'Graduated Symbol':
      return self.gradSymbol()
    #if Single Symbol
    elif self.typeRend == 'Single Symbol':
      return self.singleSymbol()
    #if Unique Value
    elif self.typeRend == 'Unique Value':
      return self.uniqueVal()
    else:
      raise Exception, "There are some problem with the rendering\n"

  def typeV2(self):
    if self.typeRend == 'graduatedSymbol':
      return self.gradSymbol2()
    #if Single Symbol
    elif self.typeRend == 'singleSymbol':
        return self.singleSymbol2()
    #if Unique Value
    elif self.typeRend == 'categorizedSymbol':
      #raise Exception, "New categorized symbology is not yet implement, it'll be soon ready\n"
      return self.uniqueVal2()
    else:
      raise Exception, "There are some problem with the rendering\n"

  def singleSymbol(self):
    """Return the javascript code for single symbology"""
    style = self.renderer.symbols()
    #set stroke color
    strokeColor=style[0].color().name()
    #set fill color
    # check if it's opaque or not
    if style[0].brush().isOpaque():
      fillColor=style[0].fillColor().name()
    else:
      fillColor=0
    #set line width
    lineWidth=style[0].lineWidth()
    #javascript code
    html_style= ['var ' + self.name + '_template = { \n\t\t']
    #if is point geometry add the point size
    if self.typeGeom == 0:
      pointSize=style[0].pointSize()
      html_style.append('pointRadius: ' + str(pointSize) + ',\n\t\t')
      self.imagePNG(style[0])
      if self.svg:
	html_style.append('externalGraphic: "' + str(self.nameSvg) + '"\n\t')
      else:
	html_style.append('strokeColor: "' + str(strokeColor) + '",\n\t\t'\
	  'strokeOpacity: 1,\n\t\t'\
	  'strokeWidth: ' + str(lineWidth) + ',\n\t\t'\
	  'fillColor: "' + str(fillColor) + '",\n\t\t'\
	  'fillOpacity: 1\n\t'
	)
    else:
      html_style.append('strokeColor: "' + str(strokeColor) + '",\n\t\t'\
	'strokeOpacity: 1,\n\t\t'\
	'strokeWidth: ' + str(lineWidth) + ',\n\t\t'\
	'fillColor: "' + str(fillColor) + '",\n\t\t'\
	'fillOpacity: 1\n\t'
      )
	  
    html_style.append(  
      '}\n\t'\
      'var ' + self.name + '_style = new OpenLayers.Style(' + self.name + 
	'_template)\n\t'
    )
    return html_style

  def singleSymbol2(self):
    """Return the javascript code for single symbology"""
    symbol = self.renderer.symbol()
    self.checkSymbol2(symbol)
    style = dictV2(symbol.symbolLayer(0).properties())
    self.checkProprierties2(style)
    #set fill color
    fillColor = 'rgb(%s)' % ",".join(style['color'].split(',')[:-1])
    alpha = symbol.alpha()
    #javascript code
    html_style= ['var ' + self.name + '_template = { \n\t\t']
    #if is point geometry add the point size
    if self.typeGeom == 0:
      #set stroke color
      strokeColor='rgb(%s)' % ",".join(style['color_border'].split(',')[:-1])
      #set line width
      size=style['size']
      html_style.append('pointRadius: ' + size + ',\n\t\t')
      #TO CHECK FOR NEW STYLE
      #self.imagePNG(style[0])
      #if self.svg:
        #html_style.append('externalGraphic: "' + str(self.nameSvg) + '"\n\t')
      #else:
      html_style.append('strokeColor: "' + str(strokeColor) + '",\n\t\t'\
        'strokeOpacity: ' + str(alpha) + ',\n\t\t'\
        #'strokeWidth: ' + str(lineWidth) + ',\n\t\t'\
        'fillColor: "' + str(fillColor) + '",\n\t\t'\
        'fillOpacity: ' + str(alpha) + '\n\t'
      )
    elif self.typeGeom == 1:
      lineWidth = style['width']
      html_style.append('strokeColor: "' + str(fillColor) + '",\n\t\t'\
        'strokeOpacity: ' + str(alpha) + ',\n\t\t'\
        'strokeWidth: ' + str(lineWidth) + ',\n\t\t'
        #'fillColor: "' + str(fillColor) + '",\n\t\t'\
        #'fillOpacity: 1\n\t'
      )
    elif self.typeGeom == 2:
      #set stroke color
      strokeColor='rgb(%s)' % ",".join(style['color_border'].split(',')[:-1])
      lineWidth = style['width_border']
      html_style.append('strokeColor: "' + str(strokeColor) + '",\n\t\t'\
        'strokeOpacity: ' + str(alpha) + ',\n\t\t'\
        'strokeWidth: ' + str(lineWidth) + ',\n\t\t'\
        'fillColor: "' + str(fillColor) + '",\n\t\t'\
        'fillOpacity: ' + str(alpha) + '\n\t'
      )
    html_style.append(  
      '}\n\t'\
      'var ' + self.name + '_style = new OpenLayers.Style(' + self.name + 
        '_template)\n\t'
    )
    return html_style

  def uniqueVal(self):
    """Return the javascript code for unique values symbology"""
    styleMap = self.renderer.symbolMap()
    html_style = ['var ' + self.name + '_style = new OpenLayers.Style(\n\t\t']
    html_style.append('OpenLayers.Util.applyDefaults({ \n\t\t\t')
    if self.typeGeom == 0:
      html_style.append('pointRadius: "${getPoint}",\n\t\t\t')
      symbol = styleMap.values()[0]
      self.imagePNG(symbol)
      if self.svg:
	html_style.append('externalGraphic: "${getGraphic}"\n\t\t\t'\
	  '}, OpenLayers.Feature.Vector.style["default"]), {\n\t\t\t'\
	  'context: {\n\t\t\t\t'
	)
    if not self.svg:
      html_style.append('strokeColor: "${getStrokeColor}",\n\t\t\t'\
	'strokeOpacity: 1,\n\t\t\t'\
	'strokeWidth: "${getLineWidth}",\n\t\t\t'\
	'fillColor: "${getFillColor}",\n\t\t\t'\
	'fillOpacity: 1\n\t\t'\
	'}, OpenLayers.Feature.Vector.style["default"]), {\n\t\t\t'\
	'context: {\n\t\t\t\t'
      )
    if self.typeGeom == 0:
      #add style for stroke color value
      html_style.extend(self.addElementStyleUnique(styleMap,'Point'))
      if self.svg:
	html_style.extend(self.addElementStyleUnique(styleMap,'Graphic'))
    if not self.svg:
      #add style for stroke color value
      html_style.extend(self.addElementStyleUnique(styleMap,'StrokeColor'))
      #add style for fill color value
      html_style.extend(self.addElementStyleUnique(styleMap,'FillColor'))
      #add style for line width value
      html_style.extend(self.addElementStyleUnique(styleMap,'LineWidth'))
    #close the style
    html_style.append('\n\t\t\t}\n\t\t}\n\t);\n\t')
    return html_style

  def uniqueVal2(self):
    """Return the javascript code for unique values symbology"""
    styleMap = self.renderer.categories()
    html_style = ['var ' + self.name + '_style = new OpenLayers.Style(\n\t\t']
    html_style.append('OpenLayers.Util.applyDefaults({ \n\t\t\t')
    if self.typeGeom == 0:
      html_style.append('pointRadius: "${getPoint}",\n\t\t\t')
      ## TO CHECK FOR NEW SYMBOLOGY
      #symbol = styleMap.values()[0]
      #self.imagePNG(symbol)
      #if self.svg:
        #html_style.append('externalGraphic: "${getGraphic}"\n\t\t\t'\
          #'}, OpenLayers.Feature.Vector.style["default"]), {\n\t\t\t'\
          #'context: {\n\t\t\t\t'
        #)
    if not self.svg:
      html_style.append('strokeColor: "${getStrokeColor}",\n\t\t\t'\
                        'strokeOpacity: "${getOpacity}",\n\t\t\t')
      if self.typeGeom == 1 or self.typeGeom == 2:
        html_style.append('strokeWidth: "${getLineWidth}')
        if self.typeGeom == 1:
          html_style.append('"\n\t\t\t')
        else:
          html_style.append('",\n\t\t\t')
      if self.typeGeom == 0 or self.typeGeom == 2:
        html_style.append('fillColor: "${getFillColor}",\n\t\t\t'\
          'fillOpacity: "${getOpacity}"\n\t\t')
    html_style.append('}, OpenLayers.Feature.Vector.style["default"]), {\n\t\t\t'\
      'context: {\n\t\t\t\t')
    if self.typeGeom == 0:
      #add style for stroke color value
      html_style.extend(self.addElementStyleUnique2(styleMap,'Point'))
      if self.svg:
        html_style.extend(self.addElementStyleUnique2(styleMap,'Graphic'))
    if not self.svg:
      #add style for stroke color value
      html_style.extend(self.addElementStyleUnique2(styleMap,'Opacity'))
      #add style for stroke color value
      html_style.extend(self.addElementStyleUnique2(styleMap,'StrokeColor'))
      if self.typeGeom != 1:
        #add style for fill color value
        html_style.extend(self.addElementStyleUnique2(styleMap,'FillColor'))
      if self.typeGeom > 0:
        #add style for line width value
        html_style.extend(self.addElementStyleUnique2(styleMap,'LineWidth'))
    #close the style
    html_style.append('\n\t\t\t}\n\t\t}\n\t);\n\t')
    return html_style

  def addElementStyleUnique(self,styleMap,element):
    """ Function for the point size (used with vector point);
	it's used in uniqueVal function
    styleMap = stile map in qgis format
    nameField = the name of field for the classification
    """
    value=0
    # the higher number od styleMap
    higValue=len(styleMap)-1   
    #for each field in styleMap
    for z,y in styleMap.iteritems():
      if element == 'Point':
	valueStyle = str(y.pointSize())
      elif element == 'Graphic':
	self.imagePNG(y)
	valueStyle = '"' + str(self.nameSvg) + '"'
      elif element == 'StrokeColor':
        valueStyle = '"' + str(y.color().name()) + '"'
      elif element == 'LineWidth':
	valueStyle = str(y.lineWidth())
      elif element == 'FillColor':
	if y.brush().isOpaque():
	  valueStyle = '"' + str(y.fillColor().name()) + '"'
	else:
	  valueStyle = '"0"'
      # if the field is the first
      if (value==0):
	html_element = ['get' + element + ': function(feature) {\n\t\t\t\t\t' \
	+ 'if (feature.attributes.' + self.nameField + '=="' + z + '")' \
	+ '{\n\t\t\t\t\t\telement='+ valueStyle +';\n\t\t\t\t\t}']
	value=value+1
      # if the field is the last
      elif (value==higValue):
	html_element.append(' else if (feature.attributes.' + self.nameField + 
	'=="' + z + '"){\n\t\t\t\t\t\telement=' + valueStyle + ';\n\t\t\t\t\t'\
	+ '} else {\n\t\t\t\t\t\telement="NULL";\n\t\t\t\t\t}\n\t\t\t\t\t' \
	+ 'return element;\n\t\t\t\t},\n\t\t\t\t')
      else:
	html_element.append(' else if (feature.attributes.' + self.nameField +
	'=="' + z + '"){\n\t\t\t\t\t\telement=' + valueStyle + ';\n\t\t\t\t\t}')
	value=value+1
    #return the code
    return html_element
      

  def addElementStyleUnique2(self,styleMap,element):
    """ Function for the point size (used with vector point);
        it's used in uniqueVal function
    styleMap = stile map in qgis format
    nameField = the name of field for the classification
    """
    value=0
    # the higher number od styleMap
    higValue=len(styleMap)-1
    #for each field in styleMap
    for cat in styleMap:
      z = cat.value().toString()
      symbol = cat.symbol()
      self.checkSymbol2(symbol)
      style = dictV2(symbol.symbolLayer(0).properties())
      self.checkProprierties2(style)
      if element == 'Point':
        valueStyle = style['size']
      #to check for new style
      #elif element == 'Graphic':
        #self.imagePNG(y)
        #valueStyle = '"' + str(self.nameSvg) + '"'
      elif element == 'StrokeColor':
        try:
          valueStyle = '"rgb(%s)"' % ",".join(style['color_border'].split(',')[:-1])
        except:
          valueStyle = '"rgb(%s)"' % ",".join(style['color'].split(',')[:-1])
      elif element == 'LineWidth':
        try:
          valueStyle = style['width']
        except:
          valueStyle = style['width_border']
      elif element == 'FillColor':
        valueStyle = '"rgb(%s)"' % ",".join(style['color'].split(',')[:-1])
      elif element == 'Opacity':
        valueStyle = str(symbol.alpha())
      #check if " string is present in the values and replace with \"
      #(this fix for example OSM tags, data downloaded with QGIS OSM plugin)
      z=z.replace('"','\\"')
      # if the field is the first
      if (value==0):
        html_element = ['get' + element + ': function(feature) {\n\t\t\t\t\t' \
        + 'if (feature.attributes.' + self.nameField + '=="' + z + '")' \
        + '{\n\t\t\t\t\t\telement='+ valueStyle +';\n\t\t\t\t\t}']
        value=value+1
      # if the field is the last
      elif (value==higValue):
        html_element.append(' else if (feature.attributes.' + self.nameField + 
        '=="' + z + '"){\n\t\t\t\t\t\telement=' + valueStyle + ';\n\t\t\t\t\t'\
        + '} else {\n\t\t\t\t\t\telement="NULL";\n\t\t\t\t\t}\n\t\t\t\t\t' \
        + 'return element;\n\t\t\t\t},\n\t\t\t\t')
      else:
        html_element.append(' else if (feature.attributes.' + self.nameField +
        '=="' + z + '"){\n\t\t\t\t\t\telement=' + valueStyle + ';\n\t\t\t\t\t}')
        value=value+1
    #return the code
    return html_element


  def gradSymbol(self):
    """Return the javascript code for graduated symbology"""
    symbolsGrad = self.renderer.symbols()
    value = 0
    # the higher number od styleMap
    higValue = len(symbolsGrad) - 1
    html_style = ['var ' + self.name + '_style = new OpenLayers.Style({\n\t\t'\
    'fillOpacity: 1,\n\t\tstrokeOpacity: 1\n\t},{\n\t\trules: [\n\t\t\t']
    for symbol in symbolsGrad:
      html_style.append('new OpenLayers.Rule({\n\t\t\t\tfilter: new '\
      'OpenLayers.Filter.Comparison({\n\t\t\t\t\ttype: OpenLayers.Filter.'\
      'Comparison.BETWEEN,\n\t\t\t\t\tproperty: "' + self.nameField +
      '",\n\t\t\t\t\tlowerBoundary: ' + str(symbol.lowerValue()) +
      ',\n\t\t\t\t\tupperBoundary: ' + str(symbol.upperValue()) +
      '\n\t\t\t\t}),\n\t\t\t\tsymbolizer: { strokeColor: "' +
      symbol.color().name() + '",\n\t\t\t\t\tfillColor: "' +
      symbol.fillColor().name() + '",\n\t\t\t\t\tstrokeWidth: ' +
      str(symbol.lineWidth()) + '')
      if self.typeGeom == 0:
	html_style.append(',\n\t\t\t\t\tpointRadius: ' +
	str(symbol.pointSize()) + '')
      html_style.append('\n\t\t\t\t}\n\t\t\t})')
      if value != higValue:
	html_style.append(',\n\t\t\t')
      value = value + 1
    html_style.append('\n\t\t]\n\t});\n')
    return html_style

  def gradSymbol2(self):
    """Return the javascript code for graduated symbology"""
    symbolsGrad = self.renderer.symbols()
    ranges = self.renderer.ranges()
    value = 0
    # the higher number od styleMap
    higValue = len(symbolsGrad) - 1
    html_style = ['var ' + self.name + '_style = new OpenLayers.Style({\n\t\t'\
    'fillOpacity: 1,\n\t\tstrokeOpacity: 1\n\t},{\n\t\trules: [\n\t\t\t']
    for i in range(len(symbolsGrad)):
      self.checkSymbol2(symbolsGrad[i])
      style = dictV2(symbolsGrad[i].symbolLayer(0).properties())
      self.checkProprierties2(style)
      html_style.append('new OpenLayers.Rule({\n\t\t\t\tfilter: new '\
      'OpenLayers.Filter.Comparison({\n\t\t\t\t\ttype: OpenLayers.Filter.'\
      'Comparison.BETWEEN,\n\t\t\t\t\tproperty: "' + self.nameField + 
      '",\n\t\t\t\t\tlowerBoundary: ' + str(ranges[i].lowerValue()) + 
      ',\n\t\t\t\t\tupperBoundary: ' + str(ranges[i].upperValue()) + 
      '\n\t\t\t\t}),\n\t\t\t\tsymbolizer: {')
      if self.typeGeom == 1:
        html_style.append('\n\t\t\t\t\tstrokeColor: ' + 
                    '"rgb(%s)"' % ",".join(style['color'].split(',')[:-1]))
      else:
        html_style.append('\n\t\t\t\t\tstrokeColor: ' + 
                    '"rgb(%s)"' % ",".join(style['color_border'].split(',')[:-1]))
        html_style.append(',\n\t\t\t\t\tfillColor: ' + 
                    '"rgb(%s)"' % ",".join(style['color'].split(',')[:-1]))
      if self.typeGeom != 0:
        try:
          valueStyle = style['width']
        except:
          valueStyle = style['width_border']
        html_style.append(',\n\t\t\t\t\tstrokeWidth: ' + 
                          str(valueStyle) + '')
      if self.typeGeom == 0:
        html_style.append(',\n\t\t\t\t\tpointRadius: ' + 
                          str(style['size']) + '')
      html_style.append('\n\t\t\t\t}\n\t\t\t})')
      if value != higValue:
        html_style.append(',\n\t\t\t')
      value = value + 1
    html_style.append('\n\t\t]\n\t});\n')
    return html_style

  def contColor(self):
    """Return the javascript code for continuos color symbology"""
    minStyle = self.renderer.minimumSymbol()
    maxStyle = self.renderer.maximumSymbol()
    minValue = float(minStyle.lowerValue())
    maxValue = float(maxStyle.lowerValue())
    minColor = minStyle.fillColor()
    maxColor = maxStyle.fillColor()
    nClassField = self.renderer.classificationField()

    lineWidth = str(minStyle.lineWidth())
    strokeColor = str(minStyle.color().name())
    html_style = ['var ' + self.name + '_style = new OpenLayers.Style('] 
    html_style.append('\n\t\tOpenLayers.Util.applyDefaults({ \n\t\t\t')
    if self.typeGeom == 0:
      pointSize = str(minStyle.pointSize())
      html_style.append('pointRadius: "' + pointSize + '",\n\t\t\t')
    html_style.append('strokeColor: "' + lineWidth + '",\n\t\t\t'\
      'strokeOpacity: 1,\n\t\t\t'\
      'strokeWidth: "' + lineWidth + '",\n\t\t\t'\
      'fillColor: "${getFillColor}",\n\t\t\t'\
      'fillOpacity: 1\n\t\t'\
      '}, OpenLayers.Feature.Vector.style["default"]), {\n\t\t\t'\
      'context: {\n\t\t\t\t')

    feat = QgsFeature()
    allAttrs = self.provider.attributeIndexes()
    value = 0
    higValue = len(allAttrs)
    self.provider.select(allAttrs)
    while self.provider.nextFeature(feat):
      attrs = feat.attributeMap()
      if attrs.values()[nClassField]:
	valueFeat = attrs.values()[nClassField].toDouble()[0]
	#diffValue = 
	if (maxValue - minValue != 0):
	  red = str(maxColor.red() * ( valueFeat - minValue ) / 
	  ( maxValue - minValue ) + minColor.red() * ( maxValue - valueFeat ) /
	  ( maxValue - minValue ));
	  green = str(maxColor.green() * ( valueFeat - minValue ) / 
	  ( maxValue - minValue ) + minColor.green() * ( maxValue - valueFeat ) /
	  ( maxValue - minValue ));
	  blue =  str(maxColor.blue() * ( valueFeat - minValue ) / 
	  ( maxValue - minValue ) + minColor.blue() * ( maxValue - valueFeat ) /
	  ( maxValue - minValue ));
	else :
	  red = str(minColor.red());
	  green = str(minColor.green());
	  blue = str(minColor.blue());
	# if the field is the first
	if (value == 0):
	  html_style.append('getFillColor : function(feature) {\n\t\t\t\t\t' \
	  + 'if (feature.attributes.' + self.nameField + '=="' + str(valueFeat)
	  + '"){\n\t\t\t\t\t\telement= rgb('+ red +', '+ green +', '+ blue +
	  ');\n\t\t\t\t\t}')
	  value=value+1
	else:
	  html_style.append(' else if (feature.attributes.' + self.nameField +
	  '=="' + str(valueFeat) + '"){\n\t\t\t\t\t\telement=rgb('+ red +', '+ 
	  green +', '+ blue +');\n\t\t\t\t\t}')
	  value=value+1
    html_style.append(' else {\n\t\t\t\t\t\telement="NULL";\n\t\t\t\t\t}'\
    '\n\t\t\t\t\t return element;\n\t\t\t\t},\n\t\t\t\t\n\t\t\t}\n\t\t}\n\t);'\
    '\n\t')
    return html_style

  def imagePNG(self,style):
    name = str(style.pointSymbolName())
    typ = name.split(':')
    # DA CORREGGERE PER FAR FUNZIONARE SOTTO WIN
    nameImage = os2emxpath.basename(typ[1]).split('.')[0]
    actualSize = style.pointSize()
    if typ[0] == 'svg':
      if actualSize <= 50:
	style.setPointSize(50)
	image=style.getPointSymbolAsImage()
	style.setPointSize(actualSize)
      else:
	image=style.getPointSymbolAsImage()
      self.nameSvg = os.path.abspath(os.path.join(str(self.path), nameImage + 
      '.png'))
      if image.save(self.nameSvg,'png'):
	#set svg variable tu true
	self.svg = True
      else:
	raise Exception, "There are some problem in the conversion of symbol in png image\n"     
    return 0

  def checkSymbol2(self,symbol):
    """Check if a symbol has some problem for OpenLayers style"""
    #check how many symbols there are in a symbolset
    if symbol.symbolLayerCount() != 1:
      self.log += "WARNING: OGR2Layers support only a layer of the new symbology. "
      self.log += "         On vector <b>%s</b>, style type %s, first symbol is used <br />" % (
                  self.name, self.typeRend)
  
  def checkProprierties2(self,prop):
    """Check if the style of rendering it is supported by OpenLayers style"""
    if self.typeGeom == 0:
      if 'color' not in prop.keys() or 'color_border' not in prop.keys():
        raise Exception, "OGR2Layers doesn't support svg style\n"
      elif 'font' in prop.keys():
        raise Exception, "OGR2Layers doesn't support font style\n"
        #self.log += "WARNING: OGR2Layers doesn't support font style. "
        #self.log += "         On vector <b>%s</b>, font style moved to simple" %  self.name
    if self.typeGeom == 1:
      if prop['penstyle'] != 'solid':
        self.log += "WARNING: OGR2Layers support only solid style. "
        self.log += "         On vector <b>%s</b>, symbol style %s, moved to solid" % (
                    self.name, prop['penstyle'])
    elif self.typeGeom == 2:
      if prop['style'] != 'solid':
        self.log += "WARNING: OGR2Layers support only solid style. "
        self.log += "         On vector <b>%s</b>, symbol style %s, moved to solid" % (
                    self.name, prop['penstyle'])

  def retLog(self):
    """Return the log of vector style"""
    return self.log
