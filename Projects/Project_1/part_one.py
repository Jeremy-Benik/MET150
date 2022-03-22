import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import metpy.calc as mpcalc
from metpy.units import units
import datetime as dt
from dateutil import tz
import matplotlib.dates as pltd
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

# %% Seattle
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
#Seattle
temp1_KFHR = []
dew1_KFHR = []
wind2_KFHR = []

for i in range(0, 24):
    #Tonopah station
    temp1_KTPH.append(temp_KTPH[np.array(np.where(date_KTPH.hour == i)[0][:])].mean())
    dew1_KTPH.append(dew_KTPH[np.array(np.where(date_KTPH.hour == i)[0][:])].mean())
    wind2_KTPH.append(ws_KTPH[np.array(np.where(date_KTPH.hour == i)[0][:])].mean())
    #Seattle Station
    temp1_KFHR.append(temp_KFHR[np.array(np.where(date_KFHR.hour == i)[0][:])].mean())
    dew1_KFHR.append(dew_KFHR[np.array(np.where(date_KFHR.hour == i)[0][:])].mean())
    wind2_KFHR.append(ws_KFHR[np.array(np.where(date_KFHR.hour == i)[0][:])].mean())
    
    
fig, ax = plt.subplots(figsize = (15, 10))
ax5 = ax.twinx()
ax1 = ax.plot(np.arange(0, 24), temp1_KTPH, label = 'Temperature (\N{DEGREE SIGN}F) Tonopah', color = 'red')
ax2 = ax.plot(np.arange(0, 24), temp1_KFHR, label = 'Temperature (\N{DEGREE SIGN}F) Seattle', color = 'red', linestyle = '--')
ax3 = ax5.plot(np.arange(0, 24), wind2_KTPH, label = 'Wind Speed (mph) Tonopah', color = 'blue')
ax4 = ax5.plot(np.arange(0, 24), wind2_KFHR, label = 'Wind Speed (mph) Seattle', color = 'blue', linestyle = '--')
ax6 = ax.plot(np.arange(0, 24), dew1_KTPH, label = 'Dewpoint (\N{DEGREE SIGN}F) Tonopah', color = 'green')
ax7 = ax.plot(np.arange(0, 24), dew1_KFHR, label = 'Dewpoint (\N{DEGREE SIGN}F) Seattle', color = 'green', linestyle = '--')


ax.tick_params(axis='x', labelsize=20)
ax5.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='y', labelsize=20)
ax5.set_ylabel('Wind Speed (mph)', fontsize = 18, fontweight = 'bold')
ax.set_ylabel('Temperature (\N{DEGREE SIGN}F)', fontsize = 18, fontweight = 'bold')
ax.grid()
ax.set_title('Tonopah Airport (KTPH) and Seattle Airport Diurnal Cycle (Yearly Average)', fontsize = 18, fontweight = 'bold')
ax.set_xlabel('Date and Time (Local Time)', fontweight = 'bold', fontsize = 18)
ax.set_xlim(0, 23)
label = ax1 + ax2 + ax3 + ax4 + ax6 + ax7
labels = [i.get_label() for i in label]
ax.legend(label, labels)
plt.tight_layout()
plt.show()
# %%
temp2_KTPH = np.zeros([12, 24], float)
dew2_KTPH = []
wind3_KTPH = []
month_index_KTPH = []
hour_index_KTPH = []
temp_index_KTPH = []


temp2_KFHR = np.zeros([12, 24], float)
dew2_KFHR = []
wind3_KFHR = []
month_index_KFHR = []
hour_index_KFHR = []
temp_index_KFHR = []
# %%
for i in range(1, 13):
    temp_index_KTPH.append(temp_KTPH[date_KTPH.month == i])
    hour_index_KTPH.append(date_KTPH.hour[date_KTPH.month == i])
    
    
    temp_index_KFHR.append(temp_KFHR[date_KFHR.month == i])
    hour_index_KFHR.append(date_KFHR.hour[date_KFHR.month == i])
    #year_index.append(date.year[date.month == i])
    for j in range(0, 24):
        temp2_KTPH[i - 1, j] = temp_index_KTPH[i - 1][hour_index_KTPH[i - 1] == j].mean()
        temp2_KFHR[i - 1, j] = temp_index_KFHR[i - 1][hour_index_KFHR[i - 1] == j].mean()
        
        #temp3[i - 1, j] = temp_index[i - 1][year_index[i - 1] == j].mean()
temp2_KTPH = np.transpose(temp2_KTPH)
temp2_KFHR = np.transpose(temp2_KFHR)
# %%
labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
c= ['blue', 'pink', 'green', 'linen', 'teal', 'darkorange', 'red', 'brown', 'darkcyan', 'powderblue', 'azure', 'ivory']
# %% Tonopah graph
fig = plt.figure(figsize = (15, 10))
for i in range(0, 12):
    #plt.plot(temp2, '-o', color = c[i], label = )
    plt.errorbar(np.arange(1, 25), temp2_KTPH[:,i], yerr = np.std(temp2_KTPH[:,i]), capsize = 5, label = labels[i], color = c[i], linestyle = '--')
plt.xlabel('Month', fontsize = 12, fontweight = 'bold')
plt.ylabel('Temperature (F)', fontsize = 12, fontweight = 'bold')
plt.title('Monthly Diurnal Wind Speed (MPH) for 2017 in Tonopah, NV', fontsize = 18, fontweight = 'bold') 
plt.grid()
plt.legend()
plt.show()
# %% Seattle graph
fig = plt.figure(figsize = (15, 10))
for i in range(0, 12):
    #plt.plot(temp2, '-o', color = c[i], label = )
    plt.errorbar(np.arange(1, 25), temp2_KFHR[:,i], yerr = np.std(temp2_KFHR[:,i]), capsize = 5, label = labels[i], color = c[i], linestyle = '--', marker = 'o')
plt.xlabel('Month', fontsize = 12, fontweight = 'bold')
plt.ylabel('Temperature (F)', fontsize = 12, fontweight = 'bold')
plt.title('Monthly Diurnal Wind Speed (MPH) for 2017 in Seattle, WA', fontsize = 18, fontweight = 'bold') 
plt.grid()
plt.legend()
plt.show()
        
    
    
    



