#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 11 21:40:11 2026

@author: fattabby
"""
#source: https://data.humdata.org/dataset/hotosm_chn_railways
import geopandas as gpd
#前處理
china_railways=gpd.read_file("/home/fattabby/下載/hotosm_chn_railways_lines_shp/hotosm_chn_railways_lines_shp.shp")
#抓杭溫高速鐵路的資料
hangzhou_wenzhou_hs=china_railways[(china_railways["name"]=="杭温高速铁路")]
hangzhou_wenzhou_hs.to_file("/home/fattabby/下載/hangzhou_wenzhou_hs.shp")
