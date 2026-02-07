#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  7 21:11:25 2026

@author: fattabby
"""

#shapefile source: https://data.humdata.org/m/dataset/hotosm_chn_roads
import geopandas as gpd
#import pandas as pd

# Load the shapefile into a GeoDataFrame
# GeoPandas can also read zipped shapefiles directly
gdf = gpd.read_file("/home/fattabby/下載/hotosm_chn_roads_lines_shp/hotosm_chn_roads_lines_shp.shp")

#make an example
#yygs=gdf[gdf["name"]=="甬莞高速"] #我要知道中國的高速在公路等級（英文）是哪種類別
#road_ext=set(gdf["highway"].unique()) #motorway, motorway_link
motorways = gdf[(gdf['highway'] == 'motorway') | (gdf['highway'] == 'motorway_link')]

motorways.to_file("/home/fattabby/下載/motorways.shp")
#%%if motorways sliced ok, please do below
motorways=gpd.read_file("/home/fattabby/下載/motorways.shp")

'''
# Filter by a specific attribute value (e.g., selecting all features where "NAME" is "California")
filtered_gdf = gdf[gdf['NAME'] == 'California']

# Filter using multiple conditions (e.g., "POPULATION" > 10000)
filtered_gdf = gdf[(gdf['NAME'] == 'California') & (gdf['POPULATION'] > 10000)]

# Filter by a list of values using .isin()
id_list = [1000, 1005, 4354]
filtered_gdf = gdf[gdf['OBJECTID'].isin(id_list)]

# View the filtered data
print(filtered_gdf.head())

# Optionally, save the filtered data to a new shapefile
filtered_gdf.to_file("path/to/output/filtered_shapefile.shp")
'''