#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 10:38:59 2022

@author: jeremybenik
"""
# %%
import xarray as xr #This will be used to open the nc file
import matplotlib.pyplot as plt #this will be used for plotting the data and creating the plots
import numpy as np #this was not really used
import cartopy.feature as cfeature #Used to create the features for the map
import cartopy.crs as ccrs #used for the projections

#opening the dataset and seeing what's inside of it
df = xr.open_dataset('/Users/jeremybenik/Documents/Spring_2022/150/Projects/Project_1/ncep_monthly_air_temp_1950_1959.nc') #opening the dataset using xarray and defining it as df
print(df) #printing out df to see what's inside of it
#It would appear this file looks like a nice intro type file for me to plot. 
#latitude and longitude appear to be in a nice unit format with degrees

#defining my variables
lat = df.variables['lat'][:] #defining my latitude variable
lon = df.variables['lon'][:] #defining my longitude variable
time = df.variables['time'] #defining my time variable
sst = df.variables['air'][:, :, :] #defining the sea surface temperature

lon, lat = np.meshgrid(lon, lat) #This supposedly makes the 1D arrays into a 2D array. Not necessary for the code to work

#jan_temp = air_temp[0::12, :, :].mean(1).mean(1)
#print(time[1]) #time at 1 is 2001, 2, 16
#converting 
#sst = sst - 273.15 #converting sst from Kelvin to Celcius.
FH = 1#defining a forecast hour (I don't think this is necessary)


#making my map
fig = plt.figure(figsize = (12, 12)) #creating the figure and defining its size
ax = plt.subplot(projection = ccrs.PlateCarree(central_longitude=180)) #defining the projection of it to be PlateCarree and creating a subplot
ax.add_feature(cfeature.COASTLINE.with_scale('50m')) #adding Coastlines to the projection
ax.add_feature(cfeature.STATES) #adding states to the map
ax.add_feature(cfeature.RIVERS) #adding rivers to the map
ax.add_feature(cfeature.BORDERS) #adding borders to the map

#contouring the sea surface temperatures
cf = ax.contourf(lon, lat, sst[0, :, :], cmap=plt.cm.RdBu_r, transform=ccrs.PlateCarree())
#what I did here is assigned cf to contour the lines according to the lon, lat, and the sea surface temperature at time = 1.
#cmap is defining the color map I want to use, the transform is saying which projection I want to display it on
#contourf fills the contours in. Whereas contour just creates the contours. countour would be really useful for pressure
#curves

#creating the colorbar.
cb = fig.colorbar(cf, orientation='horizontal', aspect=70, pad=0.05, extendrect='True')
#by assigning cb to colorbar, I can input the contours I'm using. Then I orient the colorbar horizontal.
#aspect changes the aspect of the colorbar, pad is how far away the colorbar is, extendrect I'm not sure

cb.set_label('Celcius', size = 'x-large') #setting the label of the colorbar

#setting the title of the graph
ax.set_title('Monthly Mean of Air Temperature (second timestep)', fontweight = 'bold', fontsize = 18)
#shift the center of the map so I don't have that line in the middle. 
ax.add_feature(cfeature.COASTLINE.with_scale('50m')) #adding Coastlines to the projection
ax.add_feature(cfeature.STATES) #adding states to the map
ax.add_feature(cfeature.RIVERS) #adding rivers to the map
ax.add_feature(cfeature.BORDERS)
#saving the image to pc (not necessary which is why I commented it out)
#plt.savefig('C:/Users/Rubix/Pictures/Sea_Surface_Temperatures_For_2-16-2001.png')

plt.show() #this is not completely necessary, but good syntax I believe. 




