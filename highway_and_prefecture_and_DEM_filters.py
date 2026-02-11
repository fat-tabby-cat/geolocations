#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 11 22:57:05 2026

@author: fattabby
"""
#圖資來源：政府開放資料（細節待補）
import geopandas as gpd
twn_boundary=gpd.read_file("/home/fattabby/下載/villages/VILLAGE_NLSC_11401031.shp")
boundary_list=['臺北市', '新北市','宜蘭縣','桃園市','基隆市']
north_taiwan=twn_boundary[twn_boundary["COUNTYNAME"].isin(boundary_list)]
north_taiwan.to_file("/home/fattabby/下載/north_taiwan.shp")

#%%省道圖資
#north_taiwan=gpd.read_file("/home/fattabby/convert_wgs84.shp")
north_taiwan=north_taiwan.to_crs(4326)
highways=gpd.read_file("/home/fattabby/下載/shengdao/ROAD_國省道(含快速公路).shp")
highways=highways.to_crs(4326)
boundary_list=["台9","台9丁","台7","台3"]
complex_highways=highways[highways["ROADNUM"].isin(boundary_list)]
highways2 = gpd.clip(complex_highways, north_taiwan)
highways2.to_file("/home/fattabby/下載/highways2.shp")
complex_boundary=gpd.clip(north_taiwan,highways2)
complex_towncode=complex_boundary.VILLCODE.to_list()
complex_boundary=north_taiwan[north_taiwan["VILLCODE"].isin(complex_towncode)]
complex_boundary.to_file("/home/fattabby/下載/north_taiwan_union.shp")
#%%處理地圖DEM的部份
#code source https://gis.stackexchange.com/questions/444062/clipping-raster-geotiff-with-a-vector-shapefile-in-python
import rasterio
from rasterio.mask import mask
#import geopandas as gpd

inshp = "/home/fattabby/下載/north_taiwan_union.shp"
inRas = '/home/fattabby/下載/不分幅_全台及澎湖DEM/dem_20m.tif'
outRas = '/home/fattabby/下載/不分幅_全台及澎湖DEM/ClippedSmallRaster.tif'

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
    
