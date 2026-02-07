#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  7 21:11:25 2026

@author: fattabby
"""

#shapefile source: https://data.humdata.org/m/dataset/hotosm_chn_roads
import geopandas as gpd
#import pandas as pd
gdf = gpd.read_file("/home/fattabby/下載/hotosm_chn_roads_lines_shp/hotosm_chn_roads_lines_shp.shp")

#make an example
#yygs=gdf[gdf["name"]=="甬莞高速"] #我要知道中國的高速在公路等級（英文）是哪種類別
#road_ext=set(gdf["highway"].unique()) #motorway, motorway_link
motorways = gdf[(gdf['highway'] == 'motorway') | (gdf['highway'] == 'motorway_link')]

motorways.to_file("/home/fattabby/下載/motorways.shp")
#%%if motorways sliced ok, please do below
motorways=gpd.read_file("/home/fattabby/下載/motorways.shp")

shenhai_expway=motorways[motorways['name'] == '沈海高速']
shenhai_expway.to_file("/home/fattabby/下載/shenhai_expway.shp")
