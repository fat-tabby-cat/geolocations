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
hangzhou_wenzhou_hs.to_file("/home/fattabby/下載/hangzhou_wenzhou_hs_orig.shp")
#%%用命令列修圖
#因為第三列的資料有問題，所以我把它清掉
hangzhou_wenzhou_hs2=hangzhou_wenzhou_hs.drop(hangzhou_wenzhou_hs.index[[-1]])
#知道第二列線段的經緯度值
hangzhou_wenzhou_hs2.iloc[0].geometry.wkt
#output:'LINESTRING (120.6843718 28.0717455, 120.6851567 28.0717212, 120.6868004 28.0715734, 120.6881804 28.0714648, 120.6888603 28.0714379, 120.6934563 28.0714466, 120.6947348 28.0714651, 120.6953718 28.0714821, 120.6959299 28.0714969, 120.6980259 28.0715527, 120.7183476 28.0720932)'
hangzhou_wenzhou_hs2.iloc[1].geometry.wkt
#output:'LINESTRING (120.7192258 28.0721166, 120.7206746 28.0721547)'

linestring_new='LINESTRING (120.6843718 28.0717455, 120.6851567 28.0717212, 120.6868004 28.0715734, 120.6881804 28.0714648, 120.6888603 28.0714379, 120.6934563 28.0714466, 120.6947348 28.0714651, 120.6953718 28.0714821, 120.6959299 28.0714969, 120.6980259 28.0715527, 120.7183476 28.0720932,120.7192258 28.0721166, 120.7206746 28.0721547)'
#錯誤的方式
hangzhou_wenzhou_hs2.iloc[0].geometry.wkt=linestring_new
'''
output:
---------------------------------------------------------------------------
AttributeError                            Traceback (most recent call last)
Cell In[19], line 1
----> 1 hangzhou_wenzhou_hs2.iloc[0].geometry.wkt=linestring_new

AttributeError: property 'wkt' of 'LineString' object has no setter
'''
'''
以下是正確的語法，參考自
# Source - https://stackoverflow.com/a/61658263
# Posted by martinfleis, modified by community. See post 'Timeline' for change history
# Retrieved 2026-02-12, License - CC BY-SA 4.0

from shapely.wkt import loads

string = 'MULTIPOLYGON (((37.2905 55.80199, 37.29542 55.803, 37.29663 55.8032, 37.29777 55.80335, 37.29864 55.80345, 37.29969 55.80352, 37.30356 55.80356, 37.30327 55.80318, 37.30292 55.80248, 37.30278 55.80127, 37.30235 55.79863, 37.29822 55.79763, 37.29447 55.79672, 37.29441 55.79679, 37.29412 55.79671, 37.29417 55.79663, 37.29321 55.79641, 37.29326 55.79806, 37.2905 55.80199)))'
geom = loads(string)
df.loc[145, 'geometry'] = geom
'''
from shapely.wkt import loads
geom = loads(linestring_new)
print("before", hangzhou_wenzhou_hs2.iloc[0].geometry.wkt)
hangzhou_wenzhou_hs2.loc[9,'geometry']=geom
print("after", hangzhou_wenzhou_hs2.iloc[0].geometry.wkt)
hangzhou_wenzhou_hs2.plot()
#因為第一個我已經把資料加好了，最後一個我也不要了
hangzhou_wenzhou_hs2=hangzhou_wenzhou_hs2.drop(hangzhou_wenzhou_hs2.index[[-1]])
hangzhou_wenzhou_hs2.loc[9,'geometry']=geom
hangzhou_wenzhou_hs2.plot()
