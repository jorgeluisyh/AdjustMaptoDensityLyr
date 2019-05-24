import arcpy
import json
import os
############### Code to convert two pair  ################
############### of coordinates to feature ################
############### Code made by J. Yupanqui  ################

arcpy.env.overwriteOutput=True

xfolder = os.path.dirname(__file__)
rutajsonpol=os.path.join(xfolder,"JsonPol.json")

# rutafcpol= r'D:\TEMP\prueba_mzs\prueba_json.shp'
# rutafcpol= r'D:\JYUPANQUI\ayudas\jcruz\featurejson\jyscripts\features.gdb\jsonfeature'
rutafcpol= os.path.join(xfolder,"features.gdb","jsonfeature")
code = 'CODIGO'
outFc = {"pol": rutafcpol}

class CreateFeatJson(object):
  def __init__(self,extent,vquery,fc=rutafcpol,code=code,rjson=rutajsonpol):
    self.extent=extent
    self.vquery= vquery
    self.code = code
    self.rutafcpol=fc
    self.outFc = {"pol": self.rutafcpol}
    self.rutajsonpol=rjson
    self.sql = "{} = '{}'".format(self.code,self.vquery)

  def delRows(self,geom):
    with arcpy.da.UpdateCursor(self.outFc[geom], ["OID@"], self.sql) as cursorUC:
        for x in cursorUC:
            cursorUC.deleteRow()
    del cursorUC

  def loadData( self,geom, array,):
    # feature = {"pnt": self.jsonfiles.gpt, "lin": self.jsonfiles.gpl, "pol": self.jsonfiles.gpo}
    feature = {"pol": self.rutajsonpol}
    jsonOpen = open(feature[geom], "r")
    jsonLoad = json.load(jsonOpen)
    jsonOpen.close()
    jsonLoad["features"] = array
    print jsonLoad
    json2shp = arcpy.AsShape(jsonLoad, True)
  
    self.delRows(geom)
    arcpy.Append_management(json2shp, self.outFc[geom], "NO_TEST")
    # return json2shp

  def getFeature(self,extent,vquery):
    #extent string as this format "minx miny maxx maxy"

    coords = lambda xin, yin, xfi, yfi :    [[[xin, yfi],
                                            [xfi, yfi],
                                            [xfi, yin],
                                            [xin, yin],
                                            [xin, yfi]]]

    if 'NaN' in str(extent):
      xy =str(extent).split(' NaN')[0]
    else:
      xy = extent

    v= xy.split(" ")
    self.v = v

    # rows = {"FID": 0,
    #         "Id": 0,
    #         "CODIGO": "PRIMERO"}
    rows = {"CODIGO": vquery}
    container  = []
    coordinates= coords(v[0],v[1],v[2],v[3])
    itemFeatures = {"attributes": rows, "geometry": {"rings": coordinates}}
    container.append(itemFeatures)

    self.loadData("pol",container)

  def main(self):
    self.getFeature(self.extent,self.vquery)
    return arcpy.MakeFeatureLayer_management(self.rutafcpol,"square",self.sql).getOutput(0)

if __name__ == '__main__':
  x= CreateFeatJson("-77 -14 -76 -13", "segundo")
  x.main()

