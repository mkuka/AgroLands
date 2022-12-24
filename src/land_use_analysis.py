# -*- coding: utf-8 -*-
"""
Created on Thu Dec  9 10:13:41 2021

@author: Kuka
"""
import csv
import rasterio as rio
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd
import itertools
import pyproj
from shapely import ops as shpops
import rasterio.plot as rioplt
from rasterio import features
from shapely.geometry import Polygon, Point


# Load the image using the rasterio library. 
path_2004 = '..\data\polygonclip_20211207232419_873250894\CDL_2004_clip_20211207232419_873250894.tif'
path_2008 = '..\data\polygonclip_20211207232419_873250894\CDL_2008_clip_20211207232419_873250894.tif'
path_2012 = '..\data\polygonclip_20211207232419_873250894\CDL_2012_clip_20211207232419_873250894.tif'
path_2016 = '..\data\polygonclip_20211207232419_873250894\CDL_2016_clip_20211207232419_873250894.tif'
path_2020 = '..\data\polygonclip_20211207232419_873250894\CDL_2020_clip_20211207232419_873250894.tif'



dataset_img_2004 = rio.open(path_2004)

dataset_img_2008 = rio.open(path_2008)
dataset_img_2012 = rio.open(path_2012)
dataset_img_2016 = rio.open(path_2016)
dataset_img_2020 = rio.open(path_2020)

years=['2004','2008','2012','2016','2020']
datasets = [dataset_img_2004, dataset_img_2008,
            dataset_img_2012, dataset_img_2016, dataset_img_2020]


# Affine transformation matrix
for i in range(len(datasets)):
    affine_matrix = datasets[i].transform
    print(affine_matrix)


# Find maximum of value count to set the maximum y value of the plot
dics = []
def y_limit():
    max_val = [max(dics[i].values()) for i in range(len(dics))]
    y_lim = max(max_val)
    return y_lim

# Create a bar plot for each year. 
def Create_bar_plot(datasets):
    for i in range(len(datasets)):
        band = datasets[i].read(1)
        unique, counts = np.unique(band, return_counts=True)
        create_plots(unique, counts,i)
        
def create_plots(value, counts,i):
    dic = dict(zip(value, counts))
    dics.append(dic)
    fig = plt.figure(figsize=(12, 3))
    ax = fig.add_axes([0, 0, 1, 1])
    plt.ylim(0, y_limit())
    xpos = np.arange(len(value))
    plt.xticks(xpos, value)
    plt.title("-Count of pixels for "+years[i])
    ax.bar(xpos, counts)
    plt.show()
    
       
Create_bar_plot(datasets)    

# Get top five most frequent pixel values and land usage of them.

#pixel size
def pixel_size():
    print("pixel size is {0}".format(dataset_img_2004.width*dataset_img_2004.height))
pixel_size()


region_df = pd.read_csv('C:\\USD\\DM\\Programming_Project_3\\region_stats.csv')


def get_landusage_data():
    for a in range(len(dics)):
        key_list = list(dics[a].keys())
        # print(key_list)
        for i in range(len(key_list)):
            if (key_list[i] not in region_df['Value'].values):
                # print(key_list[i] )
                del dics[a][key_list[i]]
    return dics
            
list1=get_landusage_data()
def sort_pixelvalue_count():
    list_dic = []
    for i in range(len(list1)):
        
        sort_dict = {k: b for k, b in sorted(
            list1[i].items(), key=lambda element: element[1], reverse=True)}
        # sort_dict= dict(sorted((value,key) for (key,value) in dics[i].items()))
        top5_val = dict(itertools.islice(sort_dict.items(), 5))

        print(top5_val)
        list_dic.append(top5_val)
    return list_dic

sorted_list1=sort_pixelvalue_count()
def find_landusage():
    
    for a in range(len(sorted_list1)):
        # list out keys and values separately
        key_list = list(sorted_list1[a].keys())
        land_usage = []
        for i in range(len(key_list)):
            # print(key_list[i])
            # if (key_list[i] in region_df['Value'].values):
            #     print(key_list[i])
            index = region_df.index[region_df['Value'] == key_list[i]].tolist()
                # print(index)
            land_usage.append(region_df[' Category'][index[0]])
        print()
        print(land_usage)
find_landusage()
#################
# Top five most frequent pixel values are 1, 5, 176, 121, and 141.	 
# Land usage of the top five most frequent pixel values are Corn, Soybeans, 
# Grass/Pasture, Developed/Open Space, and Deciduous Forest
# Size of each pixel is 900 geotiff meters
###################               


#Load the county boundaries into geopandas.
county_gdf = gpd.read_file('C:\\USD\\DM\\Programming_Project_3\\cb_2018_us_county_5m\\cb_2018_us_county_5m.shp')

# get geodataframe for IOWA.
IOWA_county_gdf=county_gdf.loc[(county_gdf['STATEFP']=='19')]

# Black Hawk-013
# Butler-023
# Franklin-069
# Carroll-027
# Webster-187
IA_county_gpd = IOWA_county_gdf[IOWA_county_gdf['COUNTYFP'].isin(['023','013','069','027','187'])]


# list_county =['013','023','069','027','187']
counties={'013':'Black Hawk','023':'Butler','069':'Franklin','027':'Carroll','187':'Webster'} 

# Create five shapely polygons 
def create_polygon():
    for i in counties.keys():
        gdf=IA_county_gpd.loc[(IA_county_gpd['COUNTYFP']==i)]
        p=gdf['geometry'].values
        print(p)
        
      
create_polygon()

# Project the boundaries into UTM Zone 15. 
def projec_cal(gdf):
   WGS84 = pyproj.CRS('EPSG:4269')
   img_crs = pyproj.CRS(str(dataset_img_2004.crs))
   proj_fun = pyproj.Transformer.from_crs(WGS84,img_crs,always_xy=True).transform
   boundary_proj=shpops.transform(proj_fun,gdf['geometry'].iloc[0])
   return boundary_proj

listb=[]
def find_x_y_boundary(i): 
    gdf=IA_county_gpd.loc[(IA_county_gpd['COUNTYFP']==i)] 
    boundary_proj=projec_cal(gdf)
    listb.append(boundary_proj)
    ext_x = [pt[0] for pt in list(boundary_proj.exterior.coords)]
    ext_y = [pt[1] for pt in list(boundary_proj.exterior.coords)]
    county_size = boundary_proj.area
    return ext_x,ext_y,county_size

def draw_boundary():
    for dataset in datasets:
        fig =plt.figure()
        ax=fig.add_subplot(1,1,1)
        rioplt.show(dataset,ax=ax)
        for i in counties.keys():        
            ext_x,ext_y,a=find_x_y_boundary(i)
            ax.plot(ext_x,ext_y,'-b')
        fig.show()

draw_boundary()

# size of each county in square meters
def size_county():
    
    county_size={'013':[],'023':[],'069':[],'027':[],'187':[]} 
    keys=[key for key in counties.keys()]
    values=[value for value in counties.values()]
    for i in range(len(keys)):
        
        ext_x,ext_y,a=find_x_y_boundary(keys[i])
        print("size of {0} county is {1}".format(values[i],a))
        county_size[keys[i]].append(a)
       
    return county_size
size_county()   
       




