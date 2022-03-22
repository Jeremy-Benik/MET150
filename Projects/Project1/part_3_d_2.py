''' THIS IS FOR THE SECOND PART OF PART 3'''
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 16 18:53:28 2022

@author: jeremybenik
"""
# %% Importing necessary libraries
import netCDF4 as nc
import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
import datetime
import cartopy.feature as cfeature #Used to create the features for the map
import cartopy.crs as ccrs #used for the projections
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import matplotlib.ticker as mticker
from matplotlib import colorbar, colors
# %% Reading in the file
'''Calculate and plot the temperature anomaly for the warmest and coldest ONI months between 1991-2020
2015 November (warmest) 
2000 January (Coldest)
850 hPa and 100 hPa
'''
'''
/Users/jeremybenik/Documents/Spring_2022/150/Projects/Project_1/grad_students_only_1991_2020_air_temp.nc
/Users/jeremybenik/Documents/Spring_2022/150/Projects/Project_1/grad_students_only_1991_2020_air_temp_850.nc
/Users/jeremybenik/Documents/Spring_2022/150/Projects/Project_1/grad_students_only_1991_2020_air_temp_100.nc

2015 November (warmest) 
2000 January (Coldest)

'''
# %% Importing the dataset
df_850 = nc.Dataset('/Users/jeremybenik/Documents/Spring_2022/150/Projects/Project_1/grad_students_only_1991_2020_air_temp_850.nc', 'r')
df_850_xr = xr.open_dataset('/Users/jeremybenik/Documents/Spring_2022/150/Projects/Project_1/grad_students_only_1991_2020_air_temp_850.nc')

df_100 = nc.Dataset('/Users/jeremybenik/Documents/Spring_2022/150/Projects/Project_1/grad_students_only_1991_2020_air_temp_100.nc', 'r')
df_100_xr = xr.open_dataset('/Users/jeremybenik/Documents/Spring_2022/150/Projects/Project_1/grad_students_only_1991_2020_air_temp_100.nc')
# %% reading in vars and assigning them

# I want November and January means
# 2015 November (warmest) 
# 2000 January (Coldest)

#850 hpa
lat_850 = df_850.variables['lat'][:]
lon_850 = df_850.variables['lon'][:]
time_850 = df_850.variables['time'][:]
lev_850 = df_850.variables['level'][:]
air_850 = df_850.variables['air'][:, :, :, :]
# 100hpa
lat_100 = df_100.variables['lat'][:]
lon_100 = df_100.variables['lon'][:]
time_100 = df_100.variables['time'][:]
lev_100 = df_100.variables['level'][:]
air_100 = df_100.variables['air'][:, :, :, :]
# %% formatting the datetime
# time, level, lat, lon
fmt = '%Y-%m-%d %H:%M:%S.%f' #Creating the format for the initial date (1800-01-01 00:00.0)
s = '1800-01-01 00:00:0.0' #Soecifying the date used for the Julian day
# formatting the date
new_dt = datetime.datetime.strptime(s, fmt) # formatting the date
# defining times I want to add to the original time
times_850 = [] #creating an empty list used to append new dates to
for i in time_850: #creating a for loop used to iterate through all the dates and times
    times_850.append(new_dt + datetime.timedelta(hours = i)) #appending the date onto the new list times
jan_850_time = times_850[0::12]
nov_850_time = times_850[10::12]
#index 9 for january
# index 24 for nov
# %% Getting decadal averages
# January temps
temp_jan_850 = air_850[0::12, 0, :, :]
temp_jan_850 = np.array(temp_jan_850)
jan_850 = np.mean(temp_jan_850, axis = 0)

temp_jan_100 = air_100[0::12, 0, :, :]
temp_jan_100 = np.array(temp_jan_100)
jan_100 = np.mean(temp_jan_100, axis = 0)

# November temps
temp_nov_850 = air_850[10::12, 0, :, :]
temp_nov_850 = np.array(temp_nov_850)
nov_850 = np.mean(temp_nov_850, axis = 0)

temp_nov_100 = air_100[10::12, 0, :, :]
temp_nov_100 = np.array(temp_nov_100)
nov_100 = np.mean(temp_nov_100, axis = 0)

# %% Finding the month and day of the warmest and coldest montsh
jan_ano_850 = air_850[108, 0, :, :] - jan_850[:, :] #coldest
nov_ano_850 = air_850[-63, 0, :, :] - nov_850[:, :] #warmest

jan_ano_100 = air_100[108, 0, :, :] - jan_100[:, :] #coldest
nov_ano_100 = air_100[-63, 0, :, :] - nov_100[:, :] #warmest

# %% Creating the plot
vals = [jan_ano_850, nov_ano_850]
months = ['January 2000 Temperature Anomaly at 850 hPa between 1991 and 2020', 'November 2015 Temperature Anomaly at 850 hPa between 1991 and 2000']
for i in range(len(vals)):
    # Creating the plot
    fig = plt.figure(figsize = (10, 7.5)) #creating the figure and defining its size
    ax = plt.subplot(projection = ccrs.PlateCarree(central_longitude=180)) #defining the projection of it to be PlateCarree and creating a subplot
    ax.add_feature(cfeature.COASTLINE.with_scale('50m')) #adding Coastlines to the projection
    ax.add_feature(cfeature.STATES) #adding states to the map
    ax.add_feature(cfeature.RIVERS) #adding rivers to the map
    ax.add_feature(cfeature.BORDERS) #adding borders to the map
    
    #contouring the sea surface temperatures
    cf = ax.contourf(lon_850, lat_850, vals[i][:, :], 500, cmap=plt.cm.RdBu_r, transform=ccrs.PlateCarree(), levels = np.linspace(-13, 13, 500))
    #what I did here is assigned cf to contour the lines according to the lon, lat, and the sea surface temperature at time = 1.
    #cmap is defining the color map I want to use, the transform is saying which projection I want to display it on
    #contourf fills the contours in. Whereas contour just creates the contours. countour would be really useful for pressure
    #curves
    
    #creating the colorbar.
    cb = fig.colorbar(cf, orientation='horizontal', aspect=70, pad=0.05, extendrect='True') 
    #by assigning cb to colorbar, I can input the contours I'm using. Then I orient the colorbar horizontal.
    #aspect changes the aspect of the colorbar, pad is how far away the colorbar is, extendrect I'm not sure
    
    cb.set_label('Temperature (\N{DEGREE SIGN}C)', size = 'x-large', weight = 'bold') #setting the label of the colorbar
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
# %% 100 hPa plot
vals = [jan_ano_100, nov_ano_100]
months = ['January 2000 Temperature Anomaly at 100 hPa between 1991 and 2020', 'November 2015 Temperature Anomaly at 100 hPa between 1991 and 2000']
for i in range(len(vals)):
    # Creating the plot
    fig = plt.figure(figsize = (10, 7.5)) #creating the figure and defining its size
    ax = plt.subplot(projection = ccrs.PlateCarree(central_longitude=180)) #defining the projection of it to be PlateCarree and creating a subplot
    ax.add_feature(cfeature.COASTLINE.with_scale('50m')) #adding Coastlines to the projection
    ax.add_feature(cfeature.STATES) #adding states to the map
    ax.add_feature(cfeature.RIVERS) #adding rivers to the map
    ax.add_feature(cfeature.BORDERS) #adding borders to the map
    
    #contouring the sea surface temperatures
    cf = ax.contourf(lon_100, lat_100, vals[i][:, :], 500, cmap=plt.cm.RdBu_r, transform=ccrs.PlateCarree(), levels = np.linspace(-20, 20, 500))
    #what I did here is assigned cf to contour the lines according to the lon, lat, and the sea surface temperature at time = 1.
    #cmap is defining the color map I want to use, the transform is saying which projection I want to display it on
    #contourf fills the contours in. Whereas contour just creates the contours. countour would be really useful for pressure
    #curves
    
    #creating the colorbar.
    cb = fig.colorbar(cf, orientation='horizontal', aspect=70, pad=0.05, extendrect='True')
    #by assigning cb to colorbar, I can input the contours I'm using. Then I orient the colorbar horizontal.
    #aspect changes the aspect of the colorbar, pad is how far away the colorbar is, extendrect I'm not sure
    cb.set_label('Temperature (\N{DEGREE SIGN}C)', size = 'x-large', weight = 'bold') #setting the label of the colorbar
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
    #plt.savefig(f'/Users/jeremybenik/Documents/Spring_2022/150/Projects/Project_1/test{i + 2}.png')
    plt.show() #this is not completely necessary, but good syntax I believe.

