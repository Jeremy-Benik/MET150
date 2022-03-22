#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 16 15:47:23 2022

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
# %% files 
'''
/Users/jeremybenik/Documents/Spring_2022/150/Projects/Project_1/grad_students_only_1991_2020_air_temp.nc
/Users/jeremybenik/Documents/Spring_2022/150/Projects/Project_1/grad_students_only_1991_2020_air_temp_850.nc
/Users/jeremybenik/Documents/Spring_2022/150/Projects/Project_1/grad_students_only_1991_2020_air_temp_100.nc
'''
# %% Importing files
df_850 = nc.Dataset('/Users/jeremybenik/Documents/Spring_2022/150/Projects/Project_1/grad_students_only_1991_2020_air_temp_850.nc', 'r')
df_850_xr = xr.open_dataset('/Users/jeremybenik/Documents/Spring_2022/150/Projects/Project_1/grad_students_only_1991_2020_air_temp_850.nc')

df_100 = nc.Dataset('/Users/jeremybenik/Documents/Spring_2022/150/Projects/Project_1/grad_students_only_1991_2020_air_temp_100.nc', 'r')
df_100_xr = xr.open_dataset('/Users/jeremybenik/Documents/Spring_2022/150/Projects/Project_1/grad_students_only_1991_2020_air_temp_100.nc')




print(df_850_xr)

# I want January and July means
lat_850 = df_850.variables['lat'][:]
lon_850 = df_850.variables['lon'][:]
time_850 = df_850.variables['time'][:]
lev_850 = df_850.variables['level'][:]
air_850 = df_850.variables['air'][:, :, :, :]

lat_100 = df_100.variables['lat'][:]
lon_100 = df_100.variables['lon'][:]
time_100 = df_100.variables['time'][:]
lev_100 = df_100.variables['level'][:]
air_100 = df_100.variables['air'][:, :, :, :]
# time, level, lat, lon
fmt = '%Y-%m-%d %H:%M:%S.%f' #Creating the format for the initial date (1800-01-01 00:00.0)
s = '1800-01-01 00:00:0.0' #Soecifying the date used for the Julian day
# formatting the date
new_dt = dt.datetime.strptime(s, fmt) # formatting the date
# defining times I want to add to the original time
times = [] #creating an empty list used to append new dates to
for i in time_850: #creating a for loop used to iterate through all the dates and times
    times.append(new_dt + dt.timedelta(hours = i)) #appending the date onto the new list times
jan_time = times[0::12]
jul_time = times[6::12]


temp_jan_850 = air_850[0::12, :, :]
temp_jan_850 = np.array(temp_jan_850)
jan_850 = np.mean(temp_jan_850, axis = 0)
temp_jul_850 = air_850[6::12, :, :]
temp_jul_850 = np.array(temp_jul_850)
jul_850 = np.mean(temp_jul_850, axis = 0)
# %% 100 hpa
# time, level, lat, lon
fmt = '%Y-%m-%d %H:%M:%S.%f' #Creating the format for the initial date (1800-01-01 00:00.0)
s = '1800-01-01 00:00:0.0' #Soecifying the date used for the Julian day
# formatting the date
new_dt = dt.datetime.strptime(s, fmt) # formatting the date
# defining times I want to add to the original time
times = [] #creating an empty list used to append new dates to
for i in time_100: #creating a for loop used to iterate through all the dates and times
    times.append(new_dt + dt.timedelta(hours = i)) #appending the date onto the new list times
jan_time = times[0::12]
jul_time = times[6::12]


temp_jan_100 = air_100[0::12, :, :]
temp_jan_100 = np.array(temp_jan_100)
jan_100 = np.mean(temp_jan_100, axis = 0)
temp_jul_100 = air_100[6::12, :, :]
temp_jul_100 = np.array(temp_jul_100)
jul_100 = np.mean(temp_jul_100, axis = 0)


# %%
months = ["January Mean Temperature (\N{DEGREE SIGN}C) at 850 hPa 1991-2020", "July Mean Temperature (\N{DEGREE SIGN}C) at 850 hPa 1991-2020"]
vals = [jan_850, jul_850]
months_100 = ["January Mean Temperature (\N{DEGREE SIGN}C) at 100 hPa 1991-2020", "July Mean Temperature (\N{DEGREE SIGN}C) at 100 hPa 1991-2020"]
vals_100 = [jan_100, jul_100]
# %% Creating the figure
for i in range(len(vals)):
    # Creating the plot
    fig = plt.figure(figsize = (12, 12)) #creating the figure and defining its size
    ax = plt.subplot(projection = ccrs.PlateCarree(central_longitude=180)) #defining the projection of it to be PlateCarree and creating a subplot
    ax.add_feature(cfeature.COASTLINE.with_scale('50m')) #adding Coastlines to the projection
    ax.add_feature(cfeature.STATES) #adding states to the map
    ax.add_feature(cfeature.RIVERS) #adding rivers to the map
    ax.add_feature(cfeature.BORDERS) #adding borders to the map
    
    #contouring the sea surface temperatures
    cf = ax.contourf(lon_850, lat_850, vals[i][0, :, :], 200, cmap=plt.cm.RdBu_r, transform=ccrs.PlateCarree(), levels = np.linspace(-50, 50, 200))
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


# %% 100 hpa graph
for i in range(len(vals)):
    # Creating the plot
    fig = plt.figure(figsize = (12, 12)) #creating the figure and defining its size
    ax = plt.subplot(projection = ccrs.PlateCarree(central_longitude=180)) #defining the projection of it to be PlateCarree and creating a subplot
    ax.add_feature(cfeature.COASTLINE.with_scale('50m')) #adding Coastlines to the projection
    ax.add_feature(cfeature.STATES) #adding states to the map
    ax.add_feature(cfeature.RIVERS) #adding rivers to the map
    ax.add_feature(cfeature.BORDERS) #adding borders to the map
    
    #contouring the sea surface temperatures
    cf = ax.contourf(lon_100, lat_100, vals_100[i][0, :, :], 200, cmap=plt.cm.RdBu_r, transform=ccrs.PlateCarree(), levels = np.linspace(-90, -40, 200))
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
    ax.set_title(label = months_100[i], fontweight = 'bold', fontsize = 18)
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
    
    
    
    
    
    
    
    
    
    
    
    
    '''
    
    
# %% Now doing the temp anomaly part for 850 and 100
'''
/Users/jeremybenik/Documents/Spring_2022/150/Projects/Project_1/grad_students_only_1991_2020_air_temp.nc
/Users/jeremybenik/Documents/Spring_2022/150/Projects/Project_1/grad_students_only_1991_2020_air_temp_850.nc
/Users/jeremybenik/Documents/Spring_2022/150/Projects/Project_1/grad_students_only_1991_2020_air_temp_100.nc
'''
# %% Importing files
df_850 = nc.Dataset('/Users/jeremybenik/Documents/Spring_2022/150/Projects/Project_1/grad_students_only_1991_2020_air_temp_850.nc', 'r')
df_850_xr = xr.open_dataset('/Users/jeremybenik/Documents/Spring_2022/150/Projects/Project_1/grad_students_only_1991_2020_air_temp_850.nc')

df_100 = nc.Dataset('/Users/jeremybenik/Documents/Spring_2022/150/Projects/Project_1/grad_students_only_1991_2020_air_temp_100.nc', 'r')
df_100_xr = xr.open_dataset('/Users/jeremybenik/Documents/Spring_2022/150/Projects/Project_1/grad_students_only_1991_2020_air_temp_100.nc')

print(df_850_xr)

# I want January and July means
lat_850 = df_850.variables['lat'][:]
lon_850 = df_850.variables['lon'][:]
time_850 = df_850.variables['time'][:]
lev_850 = df_850.variables['level'][:]
air_850 = df_850.variables['air'][:, :, :, :]

lat_100 = df_100.variables['lat'][:]
lon_100 = df_100.variables['lon'][:]
time_100 = df_100.variables['time'][:]
lev_100 = df_100.variables['level'][:]
air_100 = df_100.variables['air'][:, :, :, :]
# time, level, lat, lon
fmt = '%Y-%m-%d %H:%M:%S.%f' #Creating the format for the initial date (1800-01-01 00:00.0)
s = '1800-01-01 00:00:0.0' #Soecifying the date used for the Julian day
# formatting the date
new_dt = dt.datetime.strptime(s, fmt) # formatting the date
# defining times I want to add to the original time
times = [] #creating an empty list used to append new dates to
for i in time_850: #creating a for loop used to iterate through all the dates and times
    times.append(new_dt + dt.timedelta(hours = i)) #appending the date onto the new list times
jan_time = times[0::12]
jul_time = times[6::12]


temp_jan_850 = air_850[0::12, :, :]
temp_jan_850 = np.array(temp_jan_850)
jan_850 = np.mean(temp_jan_850, axis = 0)
temp_jul_850 = air_850[6::12, :, :]
temp_jul_850 = np.array(temp_jul_850)
jul_850 = np.mean(temp_jul_850, axis = 0)
# %% 100 hpa
# time, level, lat, lon
fmt = '%Y-%m-%d %H:%M:%S.%f' #Creating the format for the initial date (1800-01-01 00:00.0)
s = '1800-01-01 00:00:0.0' #Soecifying the date used for the Julian day
# formatting the date
new_dt = dt.datetime.strptime(s, fmt) # formatting the date
# defining times I want to add to the original time
times = [] #creating an empty list used to append new dates to
for i in time_100: #creating a for loop used to iterate through all the dates and times
    times.append(new_dt + dt.timedelta(hours = i)) #appending the date onto the new list times
jan_time = times[0::12]
jul_time = times[6::12]


temp_jan_100 = air_100[0::12, :, :]
temp_jan_100 = np.array(temp_jan_100)
jan_100 = np.mean(temp_jan_100, axis = 0)
temp_jul_100 = air_100[6::12, :, :]
temp_jul_100 = np.array(temp_jul_100)
jul_100 = np.mean(temp_jul_100, axis = 0)



# =============================================================================
# dec_ano = air_temp[np.where(time == datetime.datetime(1957, 12, 1, 0, 0))[0][0], :, :] - dec[:, :]
# nov_ano = air_temp[np.where(time == datetime.datetime(1955, 11, 1, 0, 0))[0][0], :, :] - nov[:, :]
# =============================================================================


# %%
months = ["January Mean Temperature (C) at 850 hPa 1991-2020", "July Mean Temperature (C) at 850 hPa 1991-2020"]
vals = [jan_850, jul_850]
months_100 = ["January Mean Temperature (C) at 100 hPa 1991-2020", "July Mean Temperature (C) at 100 hPa 1991-2020"]
vals_100 = [jan_100, jul_100]
# %% Creating the figure
for i in range(len(vals)):
    # Creating the plot
    fig = plt.figure(figsize = (12, 12)) #creating the figure and defining its size
    ax = plt.subplot(projection = ccrs.PlateCarree(central_longitude=180)) #defining the projection of it to be PlateCarree and creating a subplot
    ax.add_feature(cfeature.COASTLINE.with_scale('50m')) #adding Coastlines to the projection
    ax.add_feature(cfeature.STATES) #adding states to the map
    ax.add_feature(cfeature.RIVERS) #adding rivers to the map
    ax.add_feature(cfeature.BORDERS) #adding borders to the map
    
    #contouring the sea surface temperatures
    cf = ax.contourf(lon_850, lat_850, vals[i][0, :, :], 200, cmap=plt.cm.RdBu_r, transform=ccrs.PlateCarree(), levels = np.linspace(-50, 50, 200))
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


# %% 100 hpa graph
for i in range(len(vals)):
    # Creating the plot
    fig = plt.figure(figsize = (12, 12)) #creating the figure and defining its size
    ax = plt.subplot(projection = ccrs.PlateCarree(central_longitude=180)) #defining the projection of it to be PlateCarree and creating a subplot
    ax.add_feature(cfeature.COASTLINE.with_scale('50m')) #adding Coastlines to the projection
    ax.add_feature(cfeature.STATES) #adding states to the map
    ax.add_feature(cfeature.RIVERS) #adding rivers to the map
    ax.add_feature(cfeature.BORDERS) #adding borders to the map
    
    #contouring the sea surface temperatures
    cf = ax.contourf(lon_100, lat_100, vals_100[i][0, :, :], 200, cmap=plt.cm.RdBu_r, transform=ccrs.PlateCarree(), levels = np.linspace(-50, 50, 200))
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
    ax.set_title(label = months_100[i], fontweight = 'bold', fontsize = 18)
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
'''











