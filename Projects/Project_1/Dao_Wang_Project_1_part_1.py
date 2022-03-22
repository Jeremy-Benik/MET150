# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 15:03:16 2022

@author: Dao_Wang
"""
# Dao Wang
# 2022/03/10
# METR 150
# Project 1
# Part 1

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
# import datetime as dt

# Read in csv files
df_KGRB = pd.read_csv('KGRB_dao.csv',skiprows = [0,1,2,3,4,5,7])
# df_KGRB = df_KGRB[1:]
df_KMSY = pd.read_csv('KMSY_dao.csv',skiprows = [0,1,2,3,4,5,7])
# df_KMSY = df_KMSY[1:]

# Time
time_KGRB = pd.to_datetime(df_KGRB.Date_Time).dt.tz_convert('America/Chicago')
time_KMSY = pd.to_datetime(df_KMSY.Date_Time).dt.tz_convert('America/Chicago')
# Temperature
temp_KGRB = pd.to_numeric(df_KGRB.air_temp_set_1)
temp_KMSY = pd.to_numeric(df_KMSY.air_temp_set_1)
# Dew Point Temperature
dewt_KGRB = pd.to_numeric(df_KGRB.dew_point_temperature_set_1d)
dewt_KMSY = pd.to_numeric(df_KMSY.dew_point_temperature_set_1d)
# Wind Speed
wind_KGRB = pd.to_numeric(df_KGRB.wind_speed_set_1)
wind_KMSY = pd.to_numeric(df_KMSY.wind_speed_set_1)

# Wind Direction
wdir_KGRB = pd.to_numeric(df_KGRB.wind_direction_set_1)
wdir_KMSY = pd.to_numeric(df_KMSY.wind_direction_set_1)

# Get hour of the day
hour_KGRB = time_KGRB.dt.hour
hour_KMSY = time_KMSY.dt.hour

# Get month of the day
month_KGRB = time_KGRB.dt.month
month_KMSY = time_KMSY.dt.month

# Create an array with increment of 5 from 0 to 24*60
match_time = np.arange(0,24)

# Find Time Match for Temp
temp_2_KGRB = []
dewt_2_KGRB = []
wind_2_KGRB = []
wdir_2_KGRB = []

temp_2_KMSY = []
dewt_2_KMSY = []
wind_2_KMSY = []
wdir_2_KMSY = []
temp_3_KGRB = []
for i in range(0, len(match_time)):
    temp_2_KGRB.append(temp_KGRB[np.array(np.where(hour_KGRB == match_time[i])[0][:])].mean())
    dewt_2_KGRB.append(dewt_KGRB[np.array(np.where(hour_KGRB == match_time[i])[0][:])].mean())
    wind_2_KGRB.append(wind_KGRB[np.array(np.where(hour_KGRB == match_time[i])[0][:])].mean())
    wdir_2_KGRB.append(wdir_KGRB[np.array(np.where(hour_KGRB == match_time[i])[0][:])].mean())

    temp_2_KMSY.append(temp_KMSY[np.array(np.where(hour_KGRB == match_time[i])[0][:])].mean())
    dewt_2_KMSY.append(dewt_KMSY[np.array(np.where(hour_KGRB == match_time[i])[0][:])].mean())
    wind_2_KMSY.append(wind_KMSY[np.array(np.where(hour_KGRB == match_time[i])[0][:])].mean())
    wdir_2_KMSY.append(wdir_KMSY[np.array(np.where(hour_KGRB == match_time[i])[0][:])].mean())
    
temp_3_KGRB = []
hour_3_KGRB = []
temp_4_KGRB = np.zeros([12,24],float)

temp_3_KMSY = []
hour_3_KMSY = []
temp_4_KMSY = np.zeros([12,24],float)
for j in range(0, 12):
    temp_3_KGRB.append(temp_KGRB[np.array(np.where(month_KGRB == j+1)[0][:])])
    hour_3_KGRB.append(hour_KGRB[np.array(np.where(month_KGRB == j+1)[0][:])])
    
    temp_3_KMSY.append(temp_KMSY[np.array(np.where(month_KMSY == j+1)[0][:])])
    hour_3_KMSY.append(hour_KMSY[np.array(np.where(month_KMSY == j+1)[0][:])])
    
    for i in range(0, 24):
        temp_4_KGRB[j,i] = temp_3_KGRB[j][np.array(hour_3_KGRB[j] == match_time[i])].mean()
        temp_4_KMSY[j,i] = temp_3_KMSY[j][np.array(hour_3_KMSY[j] == match_time[i])].mean()
    
temp_4_KGRB = np.transpose(temp_4_KGRB)
temp_4_KMSY = np.transpose(temp_4_KMSY)

eb_KGRB = np.std(temp_4_KGRB,1)
eb_KMSY = np.std(temp_4_KMSY,1)



############### PLOTTING ###############
label = ['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']
# %%
ax1 = plt
ax1.figure(1, figsize=(8, 6))
ax1.grid()
ax1.plot(match_time, temp_2_KGRB, color = 'green',label = 'Air', linewidth = 3)
ax1.plot(match_time, dewt_2_KGRB, color = 'lime', label = 'Dew', linewidth = 3)
ax1.tick_params(axis = 'y', labelcolor = 'green', color = 'green')
ax1.xlabel('Time [hr]')
ax1.ylabel('Temperature [F]', color = 'green')
ax1.legend(loc = 'upper left')
# ax1.ylim(-30, 120)
ax1.twinx()
ax1.plot(match_time, wind_2_KGRB, color = 'darkgreen', label = 'wind', linewidth = 3)
ax1.tick_params(axis = 'y', labelcolor = 'darkgreen', color = 'darkgreen')
ax1.ylabel('Wind Speed [mph]', color = 'darkgreen')
ax1.legend(loc = 'upper right')
ax1.legend()
ax1.title('2021 Green Bay Air/ Dew Point Temperature [F]/ Wind Speed [mph]')
ax1.show()

# %%
ax2 = plt
ax2.figure(2, figsize=(8, 6))
ax2.grid()
ax2.plot(match_time, temp_2_KMSY, color = 'purple',label = 'Air', linewidth = 3)
ax2.plot(match_time, dewt_2_KMSY, color = 'orchid', label = 'Dew', linewidth = 3)
ax2.tick_params(axis = 'y', labelcolor = 'purple', color = 'purple')
ax2.xlabel('Time [hr]')
ax2.ylabel('Temperature [F]', color = 'purple')
ax2.legend(loc = 'upper left')
# ax2.ylim(-30, 120)
ax2.twinx()
ax2.plot(match_time, wind_2_KMSY, color = 'magenta', label = 'wind', linewidth = 3)
ax2.tick_params(axis = 'y', labelcolor = 'magenta', color = 'magenta')
ax2.ylabel('Wind Speed [mph]', color = 'magenta')
ax2.legend(loc = 'upper right')
ax2.legend()
ax2.title('2021 New Orlean Air/ Dew Point Temperature [F]/ Wind Speed [mph]')
ax2.show()

# %%
ax3 = plt
ax3.figure(3, figsize=(8, 6))
colors = iter(ax3.get_cmap('brg',12)(np.linspace(0,1,12)))
ax3.grid()
for i in range(0, 12):
    c = next(colors)
    ax3.plot(match_time,temp_4_KGRB[:,i],'-o', color = c, label = label[i])
    ax3.errorbar(match_time,temp_4_KGRB[:,i], yerr = eb_KGRB, ecolor = c, capsize = 5)
ax3.xlim(0, 24)
ax3.xlabel('Time [hr]')
ax3.ylabel('Temperature [F]')
ax3.legend(fontsize="xx-small",loc = 'upper right')
ax3.title('2021 Green Bay Diurnal Monthly Air Tempurature')
    
# %%
ax4 = plt
ax4.figure(4, figsize=(8, 6))
colors = iter(ax4.get_cmap('brg',12)(np.linspace(0,1,12)))
ax4.grid()
for i in range(0, 12):
    c = next(colors)
    ax4.plot(temp_4_KMSY[:,i],'-o', color = c, label = label[i])
    ax4.errorbar(match_time,temp_4_KMSY[:,i], yerr = eb_KMSY, ecolor = c, capsize = 5)
ax4.xlim(0, 24)
ax4.xlabel('Time [hr]')
ax4.ylabel('Temperature [F]')
ax4.legend(fontsize="xx-small",loc = 'upper right')
ax4.title('2021 New Orlean Diurnal Monthly Air Tempurature')

# %%
ax5 = plt
ax5.figure(5, figsize=(8, 6))
ax5.grid()
ax5.plot(match_time, temp_2_KGRB, color = 'green',label = 'GB Air', linewidth = 3)
ax5.plot(match_time, dewt_2_KGRB, color = 'lime', label = 'GB Dew', linewidth = 3)
ax5.plot(match_time, temp_2_KMSY, color = 'purple',label = 'NO Air', linewidth = 3)
ax5.plot(match_time, dewt_2_KMSY, color = 'orchid', label = 'NO Dew', linewidth = 3)
ax5.ylabel('Temperature [F]')
ax5.legend(loc = 'best')
ax5.twinx()
ax5.plot(match_time, wind_2_KGRB, color = 'darkgreen', label = 'GB Wind', linewidth = 3)
ax5.plot(match_time, wind_2_KMSY, color = 'magenta', label = 'NO Wind', linewidth = 3)
ax5.ylabel('Wind Speed [mph]')
ax5.legend(loc = 'best')
ax5.xlabel('Date [hr]')
ax5.legend()
ax5.title('2021 Green Bay/New Orlean Air/ Dew Point Temperature [F]/ Wind Speed [mph]')
ax5.show()










