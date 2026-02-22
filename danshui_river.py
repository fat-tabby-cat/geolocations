#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 22 21:14:03 2026

@author: fattabby
配合文章：https://blogs.slat.org/node/1042
"""
#淡水河主流線型 #source: Geofabrik
import geopandas as gpd
#taiwan_waterway_shapefile=gpd.read_file("/home/fattabby/下載/taiwan-260221-free.shp/gis_osm_water_a_free_1.shp")
taiwan_all_others=gpd.read_file("/home/fattabby/下載/taiwan-260221.osm.pbf",engine="pyogrio", use_arrow=True,layer = "other_relations")
#taiwan_all_others=gpd.read_file("/home/fattabby/下載/taiwan-260221.osm.pbf",layer = "other_relations")
waterways=taiwan_all_others[(taiwan_all_others["type"]=="waterway")]
danshui_river_main=waterways[waterways['name'].isin(['淡水河', '大漢溪','新店溪','基隆河'])]
danshui_river_main2=waterways[waterways['name'].isin(['淡水河'])]
#danshui_river_main2.to_file("/home/fattabby/下載/danshui_main.dbf")
#cf https://gis.stackexchange.com/questions/464336/change-geopandas-geometry-from-geometrycollection-to-multipolygon
danshui_river_main2["geometries"] = danshui_river_main2.apply(lambda x: [g for g in x.geometry.geoms], axis=1)
danshui_river_main2 = danshui_river_main2.explode(column="geometries").drop(columns="geometry").set_geometry("geometries").rename_geometry("geometry")
danshui_river_main2=danshui_river_main2.set_crs(epsg=4326)
danshui_river_main2=danshui_river_main2.to_crs(3826)
danshui_river_main2.to_file("/home/fattabby/下載/danshui_main.shp")
#%%處理淡水河途經行政區 source: 我國政府開放資料
twn_boundary=gpd.read_file("/home/fattabby/Nextcloud/twroad/villages/VILLAGE_NLSC_11401031.shp")
twn_boundary=twn_boundary.to_crs(3826)
river_passedby = gpd.clip(twn_boundary, danshui_river_main2)
river_passedby=river_passedby.VILLCODE.to_list()
complex_boundary=twn_boundary[twn_boundary["VILLCODE"].isin(river_passedby)]
complex_boundary.to_file("/home/fattabby/Nextcloud/twroad/river_passedby.shp")

#%%處理地圖DEM的部份
#code source https://gis.stackexchange.com/questions/444062/clipping-raster-geotiff-with-a-vector-shapefile-in-python
import rasterio
from rasterio.mask import mask
#import geopandas as gpd
inshp = "/home/fattabby/Nextcloud/twroad/river_passedby.shp"
inRas = '/home/fattabby//Nextcloud/twroad/不分幅_全台及澎湖DEM/dem_20m.tif'
outRas = '/home/fattabby//Nextcloud/twroad/不分幅_全台及澎湖DEM/ClippedSmallRaster_whole.tif'

Vector=gpd.read_file(inshp)

#Vector=Vector[Vector['HYBAS_ID']==6060122060] # Subsetting to my AOI

with rasterio.open(inRas) as src:
    Vector=Vector.to_crs(src.crs)
    # print(Vector.crs)
    out_image, out_transform=mask(src,Vector.geometry,crop=True)
    out_meta=src.meta.copy() # copy the metadata of the source DEM
    
out_meta.update({
    "driver":"Gtiff",
    "height":out_image.shape[1], # height starts with shape[1]
    "width":out_image.shape[2], # width starts with shape[2]
    "transform":out_transform
})
              
with rasterio.open(outRas,'w',**out_meta) as dst:
    dst.write(out_image)
    
    
from rasterio.plot import show
import matplotlib.pyplot as plt
#cf GOOGLE AI
#cf https://help.marine.copernicus.eu/en/articles/5051975-how-to-open-and-visualize-geotiff-files-using-python
# Open the TIFF file
tiff_file_path = '/home/fattabby//Nextcloud/twroad/不分幅_全台及澎湖DEM/ClippedSmallRaster_whole.tif'
with rasterio.open(tiff_file_path) as src:
    # Plot the image using rasterio.plot.show()
    show(src, title="Danshui River Map")
    plt.show()
#%%若同時要繪製多條水系的圖
danshui_river=waterways[(waterways["other_tags"].str.contains('淡水河'))]
danshui_river.plot()

danshui_dajia_river_remix=waterways[(waterways["other_tags"].str.contains('淡水河|大甲溪',regex=True))]
danshui_dajia_river_remix.plot()

#%%打開從高度表匯出的shapefile
danshui_export=gpd.read_file("/home/fattabby/桌面/danshui_3d.shp")
danshui_export.geometry[0].wkt
