#############################################
#       OGR2Layers Plugin (c)  for Quantum GIS
#       (c) Copyright Luca Delucchi 2010
#       Authors: Luca DELUCCHI
#       Email: lucadelucchi_at_gmail_dot_com
#
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

def fieldsName(layer):
    """ Read all the fields of a vector; it's used in createQuery
    layer = input layer
    """
    #dataprovider for the layer
    vprovider = layer.dataProvider()
    #fields of a layer (in number)
    fields = vprovider.fields()
    nameFields=[]
    for i in fields:
        #add the name of field
        nameFields.append(i.name())
    #return a list with the name of fields
    return nameFields

def nameAttrField(layer,n):
    """ Function for the name of field used in "Unique Value" symbology;
        it's used in createStyle
    layer = the layer
    n = the number of field used to unique value classification
    """
    # return the provider
    vprovider = layer.dataProvider()
    # return all the fields
    fields = vprovider.fields()
    #return the name of field
    return fields[n].name()

def dictV2(dic):
    """Return good dictionary from style properties of V2rendering"""
    output = {}
    for k in dic:
        output[str(k)]=str(dic[k])
    return output
