# -*- coding: utf-8 -*-

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
      nameFields.append(fields[i].name())
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
