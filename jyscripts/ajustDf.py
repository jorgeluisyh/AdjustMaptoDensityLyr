from ValuestJsonF import *
# x= CreateFeatJson("-78 -15 -77 -14 NaN NaN", "setimo")
# fj = x.main()

def mean(*args):
    if type(args[0]) == int:
        return sum(args)/float(len(args))
    else:
        return sum(args[0])/float(len(args[0]))

def ajustar(mx,wcz,wcm):
	'''mxd, wildcarzoom,wildcardchange'''
	mxd  = arcpy.mapping.MapDocument(mx)
	datf = arcpy.mapping.ListDataFrames(mxd)[0]
	arcpy.env.workspace=os.path.dirname(mx)

	lyrzoom  = arcpy.mapping.ListLayers(mxd,'{}*'.format(wcz))[0]
	in_layer  = arcpy.mapping.ListLayers(mxd,'{}*'.format(wcm))[0]

	xtent = datf.extent
	name =os.path.basename(mx).split('.mxd')[0]
	x= CreateFeatJson(xtent, name)
	fj = x.main()
	valf = x.v

	x_ini = mean([i[0] for i in arcpy.da.SearchCursor(lyrzoom,["SHAPE@X","SHAPE@Y"])])
	y_ini = mean([i[1] for i in arcpy.da.SearchCursor(lyrzoom,["SHAPE@X","SHAPE@Y"])])

	# fc_correc = arcpy.SelectLayerByLocation_management(in_layer,"INTERSECT",x.main()).getOutput(0)
	# x_correc = mean([i[0] for i in arcpy.da.SearchCursor(fc_correc,["SHAPE@X","SHAPE@Y"])])
	# y_correc = mean([i[1] for i in arcpy.da.SearchCursor(fc_correc,["SHAPE@X","SHAPE@Y"])])
	arcpy.SelectLayerByLocation_management(in_layer,"INTERSECT",x.main())
	x_correc = mean([i[0] for i in arcpy.da.SearchCursor(in_layer,["SHAPE@X","SHAPE@Y"])])
	y_correc = mean([i[1] for i in arcpy.da.SearchCursor(in_layer,["SHAPE@X","SHAPE@Y"])])

	difx = x_correc - x_ini
	dify = y_correc - y_ini

	storesc = datf.scale
	valf = [float(i) for i in valf]
	rxy = [str( valf[0]+ difx), str( valf[1]+ dify), str( valf[2]+ difx), str(valf[3]+ dify)]
	textextent = "{} {} {} {} NaN NaN NaN NaN".format(rxy[0],rxy[1],rxy[2],rxy[3])
	datf.extent =textextent
	datf.scale= storesc
	arcpy.SelectLayerByAttribute_management(in_layer,"CLEAR_SELECTION")
	arcpy.RefreshActiveView()
	mxd.saveACopy(name+"_1.mxd")

if __name__ == '__main__':
	mapa = r"D:\JYUPANQUI\ayudas\jcruz\mapas\12102.mxd"
	ajustar(mapa,"MANZANAS1_S","MANZANAS_PERU")