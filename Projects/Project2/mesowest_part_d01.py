#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 11 10:57:22 2022

@author: jeremybenik
"""

# %% Importing necessary libraries
import netCDF4 as nc
import matplotlib.pyplot as plt
import glob
import numpy as np
import pandas as pd
import wrf
import metpy.calc as mpcalc
from metpy.units import units
# %% Importing the wrfinput files and the csv
wrfin = nc.Dataset('/Volumes/Data/School/SJSU/Spring_2022/150/Projects/Project_2/wrfinputs/run_1/wrfinput_d01')
# %% Using wrf ll to xy to find the mesowest stations on the grids
print('Finding the indexes for the station')
south_north_station_1_u = wrf.ll_to_xy(wrfin, 38.784597, -120.310514, timeidx = 0, squeeze = False, meta = False, stagger = 'u')[1]
west_east_stag_1_u = wrf.ll_to_xy(wrfin, 38.784597, -120.310514, timeidx = 0, squeeze = False, meta = False, stagger = 'u')[0]

south_north_stag_1_v = wrf.ll_to_xy(wrfin, 38.784597, -120.310514, timeidx = 0, squeeze = False, meta = False, stagger = 'v')[1]
west_east_station_1_v = wrf.ll_to_xy(wrfin, 38.784597, -120.310514, timeidx = 0, squeeze = False, meta = False, stagger = 'v')[0]

south_north_station_1 = wrf.ll_to_xy(wrfin, 38.784597, -120.310514, timeidx = 0, squeeze = False, meta = False, stagger = 'm')[1]
west_east_station_1 = wrf.ll_to_xy(wrfin, 38.784597, -120.310514, timeidx = 0, squeeze = False, meta = False, stagger = 'm')[0]

print('reading in the wrfout files')
path = r'/Volumes/Data/School/SJSU/Spring_2022/150/Projects/Project_2/wrfout_first_run/'
rain = []
u = []
v = []
t = []
ht = []
lat = []
lon = []
times = []
t2 = []
u10 = []
v10 = []
filenames = glob.glob(path + 'wrfout_d01_2021-12*')
for filename in filenames:
    wrfout = nc.Dataset(filename)
    xtime = wrfout.variables['XTIME'][:]
    t2.append(wrfout.variables['T2'][0, south_north_station_1, west_east_station_1])
    u10.append(wrfout.variables['U10'][0, south_north_station_1, west_east_station_1])
    v10.append(wrfout.variables['V10'][0, south_north_station_1, west_east_station_1])
    u.append(wrf.getvar(wrfout, "ua", None, units = "m/s"))
    v.append(wrf.getvar(wrfout, "va", None, units = "m/s"))
    t.append(wrf.getvar(wrfout, "temp", None, units = "K"))
    ht.append(wrf.getvar(wrfout, "z", units = "m", msl = False))
    times.append(wrfout.variables['Times'][:])
    # print(wrfout)
    rain.append(wrfout.variables['RAINC'][0, south_north_station_1, west_east_station_1] + 
                wrfout.variables['RAINNC'][0, south_north_station_1, west_east_station_1])


# %% Making them numpy arrays to work with 
u = np.array(u)
u = u[:, :, south_north_station_1, west_east_station_1]
v = np.array(v)
v = v[:, :, south_north_station_1, west_east_station_1]
t = np.array(t)
t = t[:, :, south_north_station_1, west_east_station_1]
t -= 273.15
ht = np.array(ht)
ht = ht[:, :, south_north_station_1, west_east_station_1]
t2 = np.array(t2)
t2 -= 273.15

# %% Interplevels

df1 = ['2021-12-23 00:00 UTC',
               '2021-12-23 03:00 UTC',
               '2021-12-23 06:00 UTC',
               '2021-12-23 09:00 UTC',
               '2021-12-23 12:00 UTC',
               '2021-12-23 15:00 UTC',
               '2021-12-23 18:00 UTC',
               '2021-12-23 21:00 UTC',
               '2021-12-24 00:00 UTC',
               '2021-12-24 03:00 UTC', 
               '2021-12-24 06:00 UTC',
               '2021-12-24 09:00 UTC', 
               '2021-12-24 12:00 UTC',
               '2021-12-24 15:00 UTC', 
               '2021-12-24 18:00 UTC',   
               '2021-12-24 21:00 UTC', 
               '2021-12-25 00:00 UTC',
               '2021-12-25 03:00 UTC',
               '2021-12-25 06:00 UTC',
               '2021-12-25 09:00 UTC',
               '2021-12-25 12:00 UTC',
               '2021-12-25 15:00 UTC',
               '2021-12-25 18:00 UTC',
               '2021-12-25 21:00 UTC',
               '2021-12-26 00:00 UTC']
# %% Reading in the csv and plotting it compared to the wrfout file
df = pd.read_csv('/Volumes/Data/School/SJSU/Spring_2022/150/Projects/Project_2/SKBC1.csv', skiprows = [0, 1, 2, 3, 4, 5, 7])
date = df['Date_Time']
df.index = pd.to_datetime(date, format="%m/%d/%Y %H:%M UTC")
df1 = pd.to_datetime(df1, format = "%Y-%m-%d %H:%M UTC")
wind = df['wind_speed_set_1'].values * units.mph
dire = df['wind_direction_set_1'].values * units.degrees
u, v = mpcalc.wind_components(wind, dire)
temp = df['air_temp_set_1']
temp = (temp - 32) * (5/9)
# %% Creating the figure for temperature 
fig, ax = plt.subplots(figsize = (15, 8))
ax.plot(df.index, temp, color = 'red', label = 'Observation Temperature')
ax.plot(df1, t2, color = 'blue', label = 'Wrfout File')
ax.set_ylabel('Temperature (C)', fontsize = 12, fontweight = 'bold')
ax.set_xlabel('Time (UTC)', fontsize = 12, fontweight = 'bold')
ax.set_title('Temperature (Observations vs. Wrfout file) d01', fontsize = 18, fontweight = 'bold')
ax.tick_params(axis='both', labelsize=10)
ax.set_xlim(df1[0], df1[-1])
ax.legend()
ax.grid()
plt.show()
# %% U winds
fig, ax = plt.subplots(figsize = (15, 8))
ax.plot(df.index, u, color = 'red', label = 'Observation U Wind')
ax.plot(df1, u10, color = 'blue', label = 'Wrfout File')
ax.set_ylabel('Wind Speed (m/s)', fontsize = 12, fontweight = 'bold')
ax.set_xlabel('Time (UTC)', fontsize = 12, fontweight = 'bold')
ax.set_title('U Wind (Observations vs. Wrfout file) d01', fontsize = 18, fontweight = 'bold')
ax.tick_params(axis='both', labelsize=10)
ax.set_xlim(df1[0], df1[-1])
ax.legend()
ax.grid()
plt.show()
# %% V winds
fig, ax = plt.subplots(figsize = (15, 8))
ax.plot(df.index, v, color = 'red', label = 'Observation V Wind')
ax.plot(df1, v10, color = 'blue', label = 'Wrfout File')
ax.set_ylabel('Wind Speed (m/s)', fontsize = 12, fontweight = 'bold')
ax.set_xlabel('Time (UTC)', fontsize = 12, fontweight = 'bold')
ax.set_title('V Wind (Observations vs. Wrfout file) d01', fontsize = 18, fontweight = 'bold')
ax.tick_params(axis='both', labelsize=10)
ax.set_xlim(df1[0], df1[-1])
ax.legend()
ax.grid()
plt.show()
# %% V winds
fig, ax = plt.subplots(figsize = (15, 8))
ax.plot(df.index, (df['precip_accum_set_1'] - 15.77) * 25.4, color = 'red', label = 'Observation Precipitation')
ax.plot(df1, rain, color = 'blue', label = 'Wrfout File')
ax.set_ylabel('Precipitation (mm)', fontsize = 12, fontweight = 'bold')
ax.set_xlabel('Time (UTC)', fontsize = 12, fontweight = 'bold')
ax.set_title('Accumulated Precipitation (mm) (Observations vs. Wrfout file) d01', fontsize = 18, fontweight = 'bold')
ax.tick_params(axis='both', labelsize=10)
ax.set_xlim(df1[0], df1[-1])
ax.legend()
ax.grid()
plt.show()

# %% Doing it for the second run with modified physics

print('reading in the wrfout files')
path_2 = r'/Volumes/Data/School/SJSU/Spring_2022/150/Projects/Project_2/wrfout_second_run/'
rain_2 = []
u_2 = []
v_2 = []
t_2 = []
ht_2 = []
lat_2 = []
lon_2 = []
times_2 = []
t2_2 = []
u10_2 = []
v10_2 = []
filenames = glob.glob(path_2 + 'wrfout_d01_2021-12*')
for filename in filenames:
    wrfout = nc.Dataset(filename)
    xtime = wrfout.variables['XTIME'][:]
    t2_2.append(wrfout.variables['T2'][0, south_north_station_1, west_east_station_1])
    u10_2.append(wrfout.variables['U10'][0, south_north_station_1, west_east_station_1])
    v10_2.append(wrfout.variables['V10'][0, south_north_station_1, west_east_station_1])
    u_2.append(wrf.getvar(wrfout, "ua", None, units = "m/s"))
    v_2.append(wrf.getvar(wrfout, "va", None, units = "m/s"))
    t_2.append(wrf.getvar(wrfout, "temp", None, units = "K"))
    ht_2.append(wrf.getvar(wrfout, "z", units = "m", msl = False))
    times_2.append(wrfout.variables['Times'][:])
    # print(wrfout)
    rain_2.append(wrfout.variables['RAINC'][0, south_north_station_1, west_east_station_1] + 
                wrfout.variables['RAINNC'][0, south_north_station_1, west_east_station_1])

# %% Making them numpy arrays to work with 
u_2 = np.array(u_2)
u_2 = u_2[:, :, south_north_station_1, west_east_station_1]
v_2 = np.array(v_2)
v_2 = v_2[:, :, south_north_station_1, west_east_station_1]
t_2 = np.array(t_2)
t_2 = t_2[:, :, south_north_station_1, west_east_station_1]
t_2 -= 273.15
ht_2 = np.array(ht_2)
ht_2 = ht_2[:, :, south_north_station_1, west_east_station_1]
t2_2 = np.array(t2_2)
t2_2 -= 273.15


# %% Reading in the csv and plotting it compared to the wrfout file
df = pd.read_csv('/Volumes/Data/School/SJSU/Spring_2022/150/Projects/Project_2/SKBC1.csv', skiprows = [0, 1, 2, 3, 4, 5, 7])
date = df['Date_Time']
df.index = pd.to_datetime(date, format="%m/%d/%Y %H:%M UTC")
df1 = pd.to_datetime(df1, format = "%Y-%m-%d %H:%M UTC")
wind = df['wind_speed_set_1'].values * units.mph
dire = df['wind_direction_set_1'].values * units.degrees
u_meso, v_meso = mpcalc.wind_components(wind, dire)
temp = df['air_temp_set_1']
temp = (temp - 32) * (5/9)
# %% Creating the figure for temperature 
fig, ax = plt.subplots(figsize = (15, 8))
ax.plot(df.index, temp, color = 'red', label = 'Observation Temperature')
ax.plot(df1, t2_2, color = 'blue', label = 'Wrfout File')
ax.set_ylabel('Temperature (C)', fontsize = 12, fontweight = 'bold')
ax.set_xlabel('Time (UTC)', fontsize = 12, fontweight = 'bold')
ax.set_title('Temperature (Observations vs. Wrfout file) d01', fontsize = 18, fontweight = 'bold')
ax.tick_params(axis='both', labelsize=10)
ax.set_xlim(df1[0], df1[-1])
ax.legend()
ax.grid()
plt.show()
# %% U winds
fig, ax = plt.subplots(figsize = (15, 8))
ax.plot(df.index, u_meso, color = 'red', label = 'Observation U Wind')
ax.plot(df1, u10_2, color = 'blue', label = 'Wrfout File')
ax.set_ylabel('Wind Speed (m/s)', fontsize = 12, fontweight = 'bold')
ax.set_xlabel('Time (UTC)', fontsize = 12, fontweight = 'bold')
ax.set_title('U Wind (Observations vs. Wrfout file) d01', fontsize = 18, fontweight = 'bold')
ax.tick_params(axis='both', labelsize=10)
ax.set_xlim(df1[0], df1[-1])
ax.legend()
ax.grid()
plt.show()
# %% V winds
fig, ax = plt.subplots(figsize = (15, 8))
ax.plot(df.index, v_meso, color = 'red', label = 'Observation V Wind')
ax.plot(df1, v10_2, color = 'blue', label = 'Wrfout File')
ax.set_ylabel('Wind Speed (m/s)', fontsize = 12, fontweight = 'bold')
ax.set_xlabel('Time (UTC)', fontsize = 12, fontweight = 'bold')
ax.set_title('V Wind (Observations vs. Wrfout file) d01', fontsize = 18, fontweight = 'bold')
ax.tick_params(axis='both', labelsize=10)
ax.set_xlim(df1[0], df1[-1])
ax.legend()
ax.grid()
plt.show()
# %% V winds
fig, ax = plt.subplots(figsize = (15, 8))
ax.plot(df.index, (df['precip_accum_set_1'] - 15.77) * 25.4, color = 'red', label = 'Observation Precipitation')
ax.plot(df1, rain_2, color = 'blue', label = 'Wrfout File')
ax.set_ylabel('Precipitation (mm)', fontsize = 12, fontweight = 'bold')
ax.set_xlabel('Time (UTC)', fontsize = 12, fontweight = 'bold')
ax.set_title('Accumulated Precipitation (mm) (Observations vs. Wrfout file) d01', fontsize = 18, fontweight = 'bold')
ax.tick_params(axis='both', labelsize=10)
ax.set_xlim(df1[0], df1[-1])
ax.legend()
ax.grid()
plt.show()


# %% Plotting both runs to see what they are like
fig, ax = plt.subplots(figsize = (15, 8))
ax.plot(df.index, temp, color = 'red', label = 'Observation Temperature')
ax.plot(df1, t2, color = 'green', label = 'Regular Physics Wrfout')
ax.plot(df1, t2_2, color = 'blue', label = 'Modified Physics Wrfout')
ax.set_ylabel('Temperature (C)', fontsize = 12, fontweight = 'bold')
ax.set_xlabel('Time (UTC)', fontsize = 12, fontweight = 'bold')
ax.set_title('Temperature (Observations vs. Wrfout file) d01', fontsize = 18, fontweight = 'bold')
ax.tick_params(axis='both', labelsize=10)
ax.set_xlim(df1[0], df1[-1])
ax.legend()
ax.grid()
plt.show()
# %% U winds
fig, ax = plt.subplots(figsize = (15, 8))
ax.plot(df.index, u_meso, color = 'red', label = 'Observation U Wind')
ax.plot(df1, u10, color = 'green', label = 'Regular Physics Wrfout')
ax.plot(df1, u10_2, color = 'blue', label = 'Modified Physics Wrfout')
ax.set_ylabel('Wind Speed (m/s)', fontsize = 12, fontweight = 'bold')
ax.set_xlabel('Time (UTC)', fontsize = 12, fontweight = 'bold')
ax.set_title('U Wind (Observations vs. Wrfout file) d01', fontsize = 18, fontweight = 'bold')
ax.tick_params(axis='both', labelsize=10)
ax.set_xlim(df1[0], df1[-1])
ax.legend()
ax.grid()
plt.show()
# %% V winds
fig, ax = plt.subplots(figsize = (15, 8))
ax.plot(df.index, v_meso, color = 'red', label = 'Observation V Wind')
ax.plot(df1, v10, color = 'green', label = 'Regular Physics Wrfout')
ax.plot(df1, v10_2, color = 'blue', label = 'Modified Physics Wrfout')
ax.set_ylabel('Wind Speed (m/s)', fontsize = 12, fontweight = 'bold')
ax.set_xlabel('Time (UTC)', fontsize = 12, fontweight = 'bold')
ax.set_title('V Wind (Observations vs. Wrfout file) d01', fontsize = 18, fontweight = 'bold')
ax.tick_params(axis='both', labelsize=10)
ax.set_xlim(df1[0], df1[-1])
ax.legend()
ax.grid()
plt.show()
# %% V winds
fig, ax = plt.subplots(figsize = (15, 8))
ax.plot(df.index, (df['precip_accum_set_1'] - 15.77) * 25.4, color = 'red', label = 'Observation Precipitation')
ax.plot(df1, rain, color = 'green', label = 'Regular Physics Wrfout')
ax.plot(df1, rain_2, color = 'blue', label = 'Modified Physics Wrfout')
ax.set_ylabel('Precipitation (mm)', fontsize = 12, fontweight = 'bold')
ax.set_xlabel('Time (UTC)', fontsize = 12, fontweight = 'bold')
ax.set_title('Accumulated Precipitation (mm) (Observations vs. Wrfout file) d01', fontsize = 18, fontweight = 'bold')
ax.tick_params(axis='both', labelsize=10)
ax.set_xlim(df1[0], df1[-1])
ax.legend()
ax.grid()
plt.show()
