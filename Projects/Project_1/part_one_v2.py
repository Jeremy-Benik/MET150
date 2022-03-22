'''THIS IS THE CODE TO USE FOR THE PLOTS '''
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 18:29:26 2022

@author: jeremybenik
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# %% Tonopah
KTPH = pd.read_csv('/Users/jeremybenik/Documents/Spring_2022/150/Projects/Project_1/KTPH_yearly_tonopah.csv', skiprows = [0, 1, 2, 3, 4, 5, 7])
KTPH['Date_Time'] = pd.to_datetime(KTPH['Date_Time']) #converts the data to a datetime format
KTPH['Date_Time'] = KTPH['Date_Time'].dt.tz_convert('America/Los_Angeles') #This converts the data to los angeles timezone
date = KTPH['Date_Time'] #setting date to the date values assigned above
KTPH.index = pd.to_datetime(date,format="%Y-%m-%d %H:%M:%S-%H:%M")
date_KTPH = pd.DatetimeIndex(KTPH.index)
date_KTPH = date_KTPH[116::] #First time starts at date[116]

temp_KTPH = KTPH['air_temp_set_1'][116::]
rh_KTPH = KTPH['relative_humidity_set_1'][116::]
ws_KTPH = KTPH['wind_speed_set_1'][116::]
wdir_KTPH = KTPH['wind_direction_set_1'][116::]
dew_KTPH = KTPH['dew_point_temperature_set_1'][116::]

# %% Friday Harbor Airport
KFHR = pd.read_csv('/Users/jeremybenik/Documents/Spring_2022/150/Projects/Project_1/KFHR_seattle_station_friday_harbor_airp.csv', skiprows = [0, 1, 2, 3, 4, 5, 7])

KFHR['Date_Time'] = pd.to_datetime(KFHR['Date_Time']) #converts the data to a datetime format
KFHR['Date_Time'] = KFHR['Date_Time'].dt.tz_convert('America/Los_Angeles') #This converts the data to los angeles timezone
date = KFHR['Date_Time'] #setting date to the date values assigned above
KFHR.index = pd.to_datetime(date,format="%Y-%m-%d %H:%M:%S-%H:%M")
date_KFHR = pd.DatetimeIndex(KFHR.index)
date_KFHR = date_KFHR[116::] #First time starts at date[116]

temp_KFHR = KFHR['air_temp_set_1'][116::]
rh_KFHR = KFHR['relative_humidity_set_1'][116::]
ws_KFHR = KFHR['wind_speed_set_1'][116::]
wdir_KFHR = KFHR['wind_direction_set_1'][116::]
dew_KFHR = KFHR['dew_point_temperature_set_1'][116::]


# %% Calculating hourly averages
#Date starts at 116 (01-01 00:00)
# Tonopah
temp1_KTPH = []
dew1_KTPH = []
wind2_KTPH = []
#Friday Harbor Airport
temp1_KFHR = []
dew1_KFHR = []
wind2_KFHR = []

for i in range(0, 24):
    #Tonopah station
    temp1_KTPH.append(temp_KTPH[np.array(np.where(date_KTPH.hour == i)[0][:])].mean())
    dew1_KTPH.append(dew_KTPH[np.array(np.where(date_KTPH.hour == i)[0][:])].mean())
    wind2_KTPH.append(ws_KTPH[np.array(np.where(date_KTPH.hour == i)[0][:])].mean())
    #Friday Harbor Airport Station
    temp1_KFHR.append(temp_KFHR[np.array(np.where(date_KFHR.hour == i)[0][:])].mean())
    dew1_KFHR.append(dew_KFHR[np.array(np.where(date_KFHR.hour == i)[0][:])].mean())
    wind2_KFHR.append(ws_KFHR[np.array(np.where(date_KFHR.hour == i)[0][:])].mean())
    
# %% This is the plot for the t, wind speed, and dewpoint for both locations, Diurnal cycle (Yearly average)
fig, ax = plt.subplots(figsize = (15, 10))
ax5 = ax.twinx()
ax1 = ax.plot(np.arange(0, 24), temp1_KTPH, label = 'Temperature (\N{DEGREE SIGN}F) Tonopah Airport (KTPH)', color = 'red')
ax2 = ax.plot(np.arange(0, 24), temp1_KFHR, label = 'Temperature (\N{DEGREE SIGN}F) Friday Harbor Airport (KFHR)', color = 'red', linestyle = '--')
ax3 = ax5.plot(np.arange(0, 24), wind2_KTPH, label = 'Wind Speed (mph) Tonopah Airport (KTPH)', color = 'blue')
ax4 = ax5.plot(np.arange(0, 24), wind2_KFHR, label = 'Wind Speed (mph) Friday Harbor Airport (KFHR)', color = 'blue', linestyle = '--')
ax6 = ax.plot(np.arange(0, 24), dew1_KTPH, label = 'Dewpoint (\N{DEGREE SIGN}F) Tonopah Airport (KTPH)', color = 'green')
ax7 = ax.plot(np.arange(0, 24), dew1_KFHR, label = 'Dewpoint (\N{DEGREE SIGN}F) Friday Harbor Airport (KFHR)', color = 'green', linestyle = '--')


ax.tick_params(axis='x', labelsize=20)
ax5.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='y', labelsize=20)
ax5.set_ylabel('Wind Speed (mph)', fontsize = 18, fontweight = 'bold')
ax.set_ylabel('Temperature (\N{DEGREE SIGN}F)', fontsize = 18, fontweight = 'bold')
ax.grid()
ax.set_title('Tonopah Airport (KTPH) and Friday Harbor Airport Airport (KFHR) Diurnal Cycle (2021 Yearly Average)', fontsize = 18, fontweight = 'bold')
ax.set_xlabel('Hour (Local Time)', fontweight = 'bold', fontsize = 18)
ax.set_xlim(0, 23)
label = ax1 + ax2 + ax3 + ax4 + ax6 + ax7
labels = [i.get_label() for i in label]
ax.legend(label, labels, prop={'size': 12})
plt.tight_layout()
plt.savefig('/Users/jeremybenik/Documents/Spring_2022/150/Projects/Project_1/Images/Part_1/Tonopah_seattle_diurnal_yearly_cycle.png')
plt.show()


# %% Calculating the monthly mean temperature
# Tonopah
temp2_KTPH = np.zeros([12, 24], float)
dew2_KTPH = np.zeros([12, 24], float)
ws2_KTPH = np.zeros([12, 24], float)
wind3_KTPH = []
month_index_KTPH = []
hour_index_KTPH = []
temp_index_KTPH = []
dew_index_KTPH = []
ws_index_KTPH = []

temp2_KFHR = np.zeros([12, 24], float)
dew2_KFHR = np.zeros([12, 24], float)
ws2_KFHR = np.zeros([12, 24], float)
month_index_KFHR = []
hour_index_KFHR = []
temp_index_KFHR = []
dew_index_KFHR = []
ws_index_KFHR = []
# %%
for i in range(1, 13):
    temp_index_KTPH.append(temp_KTPH[date_KTPH.month == i])
    dew_index_KTPH.append(dew_KTPH[date_KTPH.month == i])
    ws_index_KTPH.append(ws_KTPH[date_KTPH.month == i])
    hour_index_KTPH.append(date_KTPH.hour[date_KTPH.month == i])
    
    
    temp_index_KFHR.append(temp_KFHR[date_KFHR.month == i])
    dew_index_KFHR.append(dew_KFHR[date_KFHR.month == i])
    ws_index_KFHR.append(ws_KFHR[date_KFHR.month == i])
    hour_index_KFHR.append(date_KFHR.hour[date_KFHR.month == i])
    #year_index.append(date.year[date.month == i])
    for j in range(0, 24):
        temp2_KTPH[i - 1, j] = temp_index_KTPH[i - 1][hour_index_KTPH[i - 1] == j].mean()
        temp2_KFHR[i - 1, j] = temp_index_KFHR[i - 1][hour_index_KFHR[i - 1] == j].mean()
        
        
        dew2_KFHR[i - 1, j] = dew_index_KFHR[i - 1][hour_index_KFHR[i - 1] == j].mean()
        dew2_KTPH[i - 1, j] = dew_index_KTPH[i - 1][hour_index_KTPH[i - 1] == j].mean()
        
        ws2_KFHR[i - 1, j] = ws_index_KFHR[i - 1][hour_index_KFHR[i - 1] == j].mean()
        ws2_KTPH[i - 1, j] = ws_index_KTPH[i - 1][hour_index_KTPH[i - 1] == j].mean()
        
temp2_KTPH = np.transpose(temp2_KTPH)
temp2_KFHR = np.transpose(temp2_KFHR)

dew2_KTPH = np.transpose(dew2_KTPH)
dew2_KFHR = np.transpose(dew2_KFHR)

ws2_KTPH = np.transpose(ws2_KTPH)
ws2_KFHR = np.transpose(ws2_KFHR)
# %%
labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
#c= ['blue', 'pink', 'green', 'linen', 'teal', 'darkorange', 'red', 'black', 'darkcyan', 'powderblue', 'azure', 'ivory']
# %% Tonopah Temperature
c = ['darkblue', 'slateblue', 'green', 'lime', 'darkorange', 'red', 'brown', 'black', 'purple', 'fuchsia', 'palevioletred', 'blue']
fig = plt.figure(figsize = (15, 10))
for i in range(0, 12):
    #plt.plot(temp2, '-o', color = c[i], label = )
    plt.plot(np.arange(0, 24), temp2_KTPH[:,i], label = labels[i], color = c[i])
plt.xlabel('Hour (Local Time)', fontsize = 18, fontweight = 'bold')
plt.ylabel('Temperature (\N{DEGREE SIGN}F)', fontsize = 18, fontweight = 'bold')
plt.title('2021 Monthly Diurnal Temperature (\N{DEGREE SIGN}F) at Tonopah Airport, NV (KTPH)', fontsize = 18, fontweight = 'bold') 
plt.grid()

plt.xlim(0, 23)
ax = plt.subplot(111)
plt.xticks(fontsize = 18)
plt.yticks(fontsize = 18)
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

# Put a legend to the right of the current axis
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), prop={'size': 12})
plt.tight_layout()
plt.savefig('/Users/jeremybenik/Documents/Spring_2022/150/Projects/Project_1/Images/Part_1/Tonopah_diurnal_temp_hour.png')

plt.show()
# %% Tonopah Dewpoint
fig = plt.figure(figsize = (15, 10))
for i in range(0, 12):
    #plt.plot(temp2, '-o', color = c[i], label = )
    plt.plot(np.arange(0, 24), dew2_KTPH[:,i], label = labels[i], color = c[i])
plt.xlabel('Hour (Local Time)', fontsize = 18, fontweight = 'bold')
plt.ylabel('Dewpoint Temperature (\N{DEGREE SIGN}F)', fontsize = 18, fontweight = 'bold')
plt.title('2021 Monthly Diurnal Dewpoint Temperature (\N{DEGREE SIGN}F) at Tonopah Airport, NV (KTPH)', fontsize = 18, fontweight = 'bold') 
plt.grid()
ax = plt.subplot(111)
plt.xlim(0, 23)
plt.xticks(fontsize = 18)
plt.yticks(fontsize = 18)
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

# Put a legend to the right of the current axis
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), prop={'size': 12})
plt.tight_layout()
plt.savefig('/Users/jeremybenik/Documents/Spring_2022/150/Projects/Project_1/Images/Part_1/Tonopah_diurnal_dew_temp_hour.png')
plt.show()
# %% Tonopah Wind Speeds
fig = plt.figure(figsize = (15, 10))
for i in range(0, 12):
    #plt.plot(temp2, '-o', color = c[i], label = )
    plt.plot(np.arange(0, 24), ws2_KTPH[:,i], label = labels[i], color = c[i])
plt.xlabel('Hour (Local Time)', fontsize = 18, fontweight = 'bold')
plt.ylabel('Wind Speed (mph)', fontsize = 18, fontweight = 'bold')
plt.title('2021 Monthly Diurnal Wind Speeds (mph) at Tonopah Airport, NV (KTPH)', fontsize = 18, fontweight = 'bold') 
plt.grid()

plt.xlim(0, 23)
ax = plt.subplot(111)
plt.xticks(fontsize = 18)
plt.yticks(fontsize = 18)
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

# Put a legend to the right of the current axis
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), prop={'size': 12})
plt.tight_layout()
plt.savefig('/Users/jeremybenik/Documents/Spring_2022/150/Projects/Project_1/Images/Part_1/Tonopah_diurnal_wind_speed_hour.png')
plt.show()
# %% Friday Harbor Airport Temperature 
fig = plt.figure(figsize = (15, 10))
for i in range(0, 12):
    #plt.plot(temp2, '-o', color = c[i], label = )
    plt.plot(np.arange(0, 24), temp2_KFHR[:,i], label = labels[i], color = c[i])
plt.xlabel('Hour (Local Time)', fontsize = 18, fontweight = 'bold')
plt.ylabel('Temperature (\N{DEGREE SIGN}F)', fontsize = 18, fontweight = 'bold')
plt.title('2021 Monthly Diurnal Temperature (\N{DEGREE SIGN}F) at Friday Harbor Airport, WA (KFHR)', fontsize = 18, fontweight = 'bold') 
plt.grid()

plt.xlim(0, 23)
ax = plt.subplot(111)
plt.xticks(fontsize = 18)
plt.yticks(fontsize = 18)
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

# Put a legend to the right of the current axis
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), prop={'size': 12})
plt.tight_layout()
plt.savefig('/Users/jeremybenik/Documents/Spring_2022/150/Projects/Project_1/Images/Part_1/seattle_diurnal_temp_hour.png')
plt.show()
# %% Friday Harbor Airport Dewpoint
fig = plt.figure(figsize = (15, 10))
for i in range(0, 12):
    #plt.plot(temp2, '-o', color = c[i], label = )
    plt.plot(np.arange(0, 24), dew2_KFHR[:,i], label = labels[i], color = c[i])
plt.xlabel('Hour (Local Time)', fontsize = 18, fontweight = 'bold')
plt.ylabel('Dewpoint Temperature (\N{DEGREE SIGN}F)', fontsize = 18, fontweight = 'bold')
plt.title('2021 Monthly Diurnal Dewpoint Temperature (\N{DEGREE SIGN}F) at Friday Harbor Airport, WA (KFHR)', fontsize = 18, fontweight = 'bold') 
plt.grid()

ax = plt.subplot(111)
plt.xlim(0, 23)
plt.xticks(fontsize = 18)
plt.yticks(fontsize = 18)
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

# Put a legend to the right of the current axis
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), prop={'size': 12})
plt.tight_layout()
plt.savefig('/Users/jeremybenik/Documents/Spring_2022/150/Projects/Project_1/Images/Part_1/Seattle_diurnal_dew_temp_hour.png')
plt.show()
# %% Friday Harbor Airport Winds
fig = plt.figure(figsize = (15, 10))
for i in range(0, 12):
    #plt.plot(temp2, '-o', color = c[i], label = )
    plt.plot(np.arange(0, 24), ws2_KFHR[:,i], label = labels[i], color = c[i])
plt.xlabel('Hour (Local Time)', fontsize = 18, fontweight = 'bold')
plt.ylabel('Wind Speed (mph)', fontsize = 18, fontweight = 'bold')
plt.title('2021 Monthly Diurnal Wind Speeds (mph) at Friday Harbor Airport, WA (KFHR)', fontsize = 18, fontweight = 'bold') 
plt.grid()

ax = plt.subplot(111)
plt.xlim(0, 23)
plt.xticks(fontsize = 18)
plt.yticks(fontsize = 18)
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

# Put a legend to the right of the current axis
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), prop={'size': 12})
plt.tight_layout()
plt.savefig('/Users/jeremybenik/Documents/Spring_2022/150/Projects/Project_1/Images/Part_1/seattle_diurnam_wind_speed_hour.png')

plt.show()
# %% Creating the error bar plots Temperature
temp3_KTPH = []
dew3_KTPH =[]

temp3_KFHR = []
dew3_KFHR =[]
for i in range(1, 13):
    #Tonopah station
    temp3_KTPH.append(temp_KTPH[np.array(np.where(date_KTPH.month == i)[0][:])].mean())
    dew3_KTPH.append(dew_KTPH[np.array(np.where(date_KTPH.month == i)[0][:])].mean())
    #Friday Harbor Airport Station
    temp3_KFHR.append(temp_KFHR[np.array(np.where(date_KFHR.month == i)[0][:])].mean())
    dew3_KFHR.append(dew_KFHR[np.array(np.where(date_KFHR.month == i)[0][:])].mean())

# %%
# Tonopah and Friday Harbor Airport
fig = plt.figure(figsize = (15, 10))
plt.errorbar(np.arange(1, 13), temp3_KTPH, yerr = np.std(temp3_KTPH), capsize = 5, label = 'Tonopah Airport (KTPH) Temperature (\N{DEGREE SIGN}F)', color = 'blue', linestyle = '--', marker = 'o')
plt.errorbar(np.arange(1, 13), temp3_KFHR, yerr = np.std(temp3_KFHR), capsize = 5, label = 'Friday Harbor Airport (KFHR) Temperature (\N{DEGREE SIGN}F)', color = 'red', linestyle = '--', marker = 'o')
plt.xlabel('Month', fontsize = 18, fontweight = 'bold')
plt.ylabel('Temperature (F)', fontsize = 18, fontweight = 'bold')
plt.title('2021 Temperature (\N{DEGREE SIGN}F) Comparison with Error Bars for Tonopah, NV and Friday Harbor Airport, WA', fontsize = 18, fontweight = 'bold') 
ax = plt.subplot(111)
plt.xticks(fontsize = 18)
plt.yticks(fontsize = 18)
box = ax.get_position()
plt.xlim(0.5,12.5)
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

# Put a legend to the right of the current axis
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.legend(prop={'size': 12})
plt.grid()
plt.savefig('/Users/jeremybenik/Documents/Spring_2022/150/Projects/Project_1/Images/Part_1/error_bars_temp.png')

plt.show()
# %%
# Tonopah and Friday Harbor Airport
fig = plt.figure(figsize = (15, 10))
plt.errorbar(np.arange(1, 13), dew3_KTPH, yerr = np.std(dew3_KTPH), capsize = 5, label = 'Tonopah Airport (KTPH) Dewpoint Temperature (\N{DEGREE SIGN}F)', color = 'blue', linestyle = '--', marker = 'o')
plt.errorbar(np.arange(1, 13), dew3_KFHR, yerr = np.std(dew3_KFHR), capsize = 5, label = 'Friday Harbor Airport (KFHR) Dewpoint Temperature (\N{DEGREE SIGN}F)', color = 'red', linestyle = '--', marker = 'o')
plt.xlabel('Month', fontsize = 18, fontweight = 'bold')
plt.ylabel('Temperature (F)', fontsize = 18, fontweight = 'bold')
plt.title('2021 Site Comparison of Dewpoint Temperature (\N{DEGREE SIGN}F) with Error Bars for Tonopah, NV and Friday Harbor Airport, WA', fontsize = 18, fontweight = 'bold') 
plt.grid()
plt.xticks(fontsize = 18)
plt.yticks(fontsize = 18)
plt.xlim(0.5,12.5)
# Put a legend to the right of the current axis
plt.legend(prop={'size': 12})
ax.grid()

plt.savefig('/Users/jeremybenik/Documents/Spring_2022/150/Projects/Project_1/Images/Part_1/error_bars_dew_temp.png')

plt.show()










