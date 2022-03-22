#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 12 17:39:12 2022

@author: jeremybenik
"""

# %% Importing necessary libraries
import netCDF4 as nc
import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
import cartopy.feature as cfeature #Used to create the features for the map
import cartopy.crs as ccrs #used for the projections
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import matplotlib.ticker as mticker
# %% Reading in the data

# reading in the data
df = nc.Dataset('/Users/jeremybenik/Documents/Spring_2022/150/Projects/Project_1/ncep_monthly_air_temp_1950_1959.nc') #this uses netcdf to open the file
df_xr = xr.open_dataset('/Users/jeremybenik/Documents/Spring_2022/150/Projects/Project_1/ncep_monthly_air_temp_1950_1959.nc') # this uses xarray to better visualize the data
# %% Reading in the variables
lat = df.variables['lat'][:] #defining lat as lat. 90 - -90
lon = df.variables['lon'][:] #defining lon as lon 0 - 360
time = df.variables['time'][:] #defining the time as time
air_temp = df.variables['air'][:, :, :] #defining the air temp as air_temp. it has time, lat, lon
# %% Converting the time to a more useable format since it's in Julian day2
fmt = '%Y-%m-%d %H:%M:%S.%f' #Creating the format for the initial date (1800-01-01 00:00.0)
s = '1800-01-01 00:00:0.0' #Soecifying the date used for the Julian day
# formatting the date
new_dt = dt.datetime.strptime(s, fmt) # formatting the date
# defining times I want to add to the original time
times = [] #creating an empty list used to append new dates to
for i in time: #creating a for loop used to iterate through all the dates and times
    times.append(new_dt + dt.timedelta(hours = i)) #appending the date onto the new list times
time = times[0:145]

# temp average of that month for every year
jan_temp = air_temp[0::12, :, :]
apr_temp = air_temp[3::12, :, :]
jul_temp = air_temp[6::12, :, :]
oct_temp = air_temp[9::12, :, :]
# Setting the temps as a usable format for the graphs

# January
jan_temp = np.array(jan_temp)
jan = np.mean(jan_temp, axis = 0)

# April
apr_temp = np.array(apr_temp)
apr = np.mean(apr_temp, axis = 0)

# July
jul_temp = np.array(jul_temp)
jul = np.mean(jul_temp, axis = 0)

# October
oct_temp = np.array(oct_temp)
oct_t = np.mean(oct_temp, axis = 0)

months = ["January Monthly Mean Temperature (\N{DEGREE SIGN}C) 1950-1959", "April Monthly Mean Temperature (\N{DEGREE SIGN}C) 1950-1959", 
          "July Monthly Mean Temperature (\N{DEGREE SIGN}C) 1950-1959", "October Monthly Mean Temperature (\N{DEGREE SIGN}C) 1950-1959"]
vals = [jan, apr, jul, oct_t]
for i in range(len(vals)):
    # Creating the plot
    fig = plt.figure(figsize = (12, 12)) #creating the figure and defining its size
    ax = plt.subplot(projection = ccrs.PlateCarree(central_longitude=180)) #defining the projection of it to be PlateCarree and creating a subplot
    ax.add_feature(cfeature.COASTLINE.with_scale('50m')) #adding Coastlines to the projection
    ax.add_feature(cfeature.STATES) #adding states to the map
    ax.add_feature(cfeature.RIVERS) #adding rivers to the map
    ax.add_feature(cfeature.BORDERS) #adding borders to the map
    
    #contouring the sea surface temperatures
    cf = ax.contourf(lon, lat, vals[i][:, :], 1000, cmap=plt.cm.RdBu_r, transform=ccrs.PlateCarree(), levels = np.linspace(-65, 40, 1000))
    #what I did here is assigned cf to contour the lines according to the lon, lat, and the sea surface temperature at time = 1.
    #cmap is defining the color map I want to use, the transform is saying which projection I want to display it on
    #contourf fills the contours in. Whereas contour just creates the contours. countour would be really useful for pressure
    #curves
    
    #creating the colorbar.
    cb = fig.colorbar(cf, orientation='horizontal', aspect=70, pad=0.05, extendrect='True') 
    #by assigning cb to colorbar, I can input the contours I'm using. Then I orient the colorbar horizontal.
    #aspect changes the aspect of the colorbar, pad is how far away the colorbar is, extendrect I'm not sure
    
    cb.set_label('Temperature (\N{DEGREE SIGN}C)', size = 'x-large', weight = 'bold') #setting the label of the colorbar
    cb.ax.tick_params(labelsize=14)
    
    #setting the title of the graph
    ax.set_title(label = months[i], fontweight = 'bold', fontsize = 18)
    #shift the center of the map so I don't have that line in the middle. 
    ax.add_feature(cfeature.COASTLINE.with_scale('50m')) #adding Coastlines to the projection
    ax.add_feature(cfeature.STATES) #adding states to the map
    ax.add_feature(cfeature.RIVERS) #adding rivers to the map
    ax.add_feature(cfeature.BORDERS)
    
    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                      linewidth=2, color='gray', alpha=0.5, linestyle='--')
    gl.xlabels_top = False
    #gl.ylabels_left = True
    #gl.xlines = False
    gl.xlocator = mticker.FixedLocator(range(-180, 180, 30))
    gl.ylocator = mticker.FixedLocator(range(-90, 90, 30))
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
    gl.ylabel_style = {'size': 15, 'color': 'gray'}
    gl.ylabel_style = {'color': 'black', 'weight': 'bold'}
    gl.xlabel_style = {'size': 15, 'color': 'gray'}
    gl.xlabel_style = {'color': 'black', 'weight': 'bold'}
    
    #saving the image to pc (not necessary which is why I commented it out)
    #plt.savefig('C:/Users/Rubix/Pictures/Sea_Surface_Temperatures_For_2-16-2001.png')
    plt.show() #this is not completely necessary, but good syntax I believe.









