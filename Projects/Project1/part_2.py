#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 11:08:22 2022

@author: jeremybenik
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from metpy.plots import SkewT

#This is reno data
jan_data_1 = []
jul_data_1 = []
with open('/Users/jeremybenik/Documents/Spring_2022/150/Projects/Project_1/January_2021_sounding_data.txt', 'r') as jan_open:
    for line in jan_open:
        jan_data_1.append(line.split())
with open('/Users/jeremybenik/Documents/Spring_2022/150/Projects/Project_1/July_sounding_text.txt', 'r') as jul_open:
    for line in jul_open:
        jul_data_1.append(line.split())
'''Thought process, find where TTAA is, then index 2 after to get to the pressures, then with that, I can get the data and idex to it using a for loop'''

# Skipping the first 10 rows since it had a bunch of uneccasry information
jan_data = jan_data_1[10:][:]
jul_data= jul_data_1[10:][:]

# Creating the titles of the data
titles = ['PRES', 'TMPC', 'DWPC', 'DRCT', 'SPED', 'HGHT']

# Defining pressure levels to use. I started at 700 since my station is at 849 hPa
#pres_levels = [sfc_pres_jul, 700, 500, 400, 300, 250, 200, 150, 100]

# 
loc = []
for i in range(len(jul_data)):
    if (jul_data[i][0] == 'TTAA') == True:
        loc.append(i)
pres_jul = [] #collecting the surface pressures
temp_jul = [] # I want i + 6, 1
dewt_jul = [] # I want i + 6, 2
dpdp_jul = []
sfc_temp_jul = []
sfc_pres_jul = []
sfc_dpt_jul = []
sfc_pres_jul = []
list_jul_data = []
temp_jul_all_levels = []
dwpt_jul_all_levels = []

for i in loc:
    list_jul_data.append(jul_data[i + 2:i + 14][:])
    
for i in range(len(list_jul_data)):
    sfc_pres_jul.append(list_jul_data[i][0][0])
    sfc_temp_jul.append(list_jul_data[i][0][1])
    sfc_dpt_jul.append(list_jul_data[i][0][2])
sfc_pres_jul_mean = np.float_(sfc_pres_jul).mean()
sfc_temp_jul_mean = np.float_(sfc_temp_jul).mean()
sfc_dpt_jul_mean = np.float_(sfc_dpt_jul).mean()


jul_t_700 = []
jul_t_500 = []
jul_t_400 = []
jul_t_300 = []
jul_t_250 = []
jul_t_200 = []
jul_t_150 = []
jul_t_100 = []

# %%
jul_dp_700 = []
jul_dp_500 = []
jul_dp_400 = []
jul_dp_300 = []
jul_dp_250 = []
jul_dp_200 = []
jul_dp_150 = []
jul_dp_100 = []

# %%
for i in range(len(list_jul_data)):
    jul_t_700.append(list_jul_data[i][4][1])
    jul_t_500.append(list_jul_data[i][5][1])
    jul_t_400.append(list_jul_data[i][6][1])
    jul_t_300.append(list_jul_data[i][7][1])
    jul_t_250.append(list_jul_data[i][8][1])
    jul_t_200.append(list_jul_data[i][9][1])
    jul_t_150.append(list_jul_data[i][10][1])
    jul_t_100.append(list_jul_data[i][11][1])
    #dewpoints
# %%
for i in range(len(list_jul_data)):
    if i == 25:
        continue
        jul_dp_300.append(list_jul_data[i][7][2])
    jul_dp_700.append(list_jul_data[i][4][2])
    jul_dp_500.append(list_jul_data[i][5][2])
    jul_dp_400.append(list_jul_data[i][6][2])
    jul_dp_300.append(list_jul_data[i][7][2])
    jul_dp_250.append(list_jul_data[i][8][2])
    jul_dp_200.append(list_jul_data[i][9][2])
    jul_dp_250.append(list_jul_data[i][10][2])
    jul_dp_100.append(list_jul_data[i][11][2])
# %%
jul_700 = np.nanmean(np.array(jul_t_700).astype(float))
jul_500 = np.nanmean(np.array(jul_t_500).astype(float))
jul_400 = np.nanmean(np.array(jul_t_400).astype(float))
jul_t_300[25] = float('NaN')
jul_300 = np.nanmean(np.array(jul_t_300).astype(float))
jul_t_250[25] = float('NaN')
jul_250 = np.nanmean(np.array(jul_t_250).astype(float))
jul_200 = np.nanmean(np.array(jul_t_200).astype(float))
jul_150 = np.nanmean(np.array(jul_t_150).astype(float))
jul_100 = np.nanmean(np.array(jul_t_100).astype(float))

# %%
jul_dp_700 = np.nanmean(np.array(jul_dp_700).astype(float))
jul_dp_500 = np.nanmean(np.array(jul_dp_500).astype(float))
jul_dp_400 = np.nanmean(np.array(jul_dp_400).astype(float))
#jul_dp_t_300[25] = float('NaN')
jul_dp_300 = np.nanmean(np.array(jul_dp_300).astype(float))
#jul_dp_t_250[25] = float('NaN')
jul_dp_250 = np.nanmean(np.array(jul_dp_250).astype(float))
jul_dp_200 = np.nanmean(np.array(jul_dp_200).astype(float))
jul_dp_150 = np.nanmean(np.array(jul_dp_150).astype(float))
jul_dp_100 = np.nanmean(np.array(jul_dp_100).astype(float))




# %% January 
loc = []
for i in range(len(jan_data)):
    if (jan_data[i][0] == 'TTAA') == True:
        loc.append(i)
pres_jan = [] #collecting the surface pressures
temp_jan = [] # I want i + 6, 1
dewt_jan = [] # I want i + 6, 2
dpdp_jan = []
sfc_temp_jan = []
sfc_pres_jan = []
sfc_dpt_jan = []
sfc_pres_jan = []
list_jan_data = []
temp_jan_all_levels = []
dwpt_jan_all_levels = []

for i in loc:
    list_jan_data.append(jan_data[i + 2:i + 14][:])
    
for i in range(len(list_jan_data)):
    sfc_pres_jan.append(list_jan_data[i][0][0])
    sfc_temp_jan.append(list_jan_data[i][0][1])
    sfc_dpt_jan.append(list_jan_data[i][0][2])
sfc_pres_jan_mean = np.float_(sfc_pres_jan).mean()
sfc_temp_jan_mean = np.float_(sfc_temp_jan).mean()
sfc_dpt_jan_mean = np.float_(sfc_dpt_jan).mean()


jan_t_700 = []
jan_t_500 = []
jan_t_400 = []
jan_t_300 = []
jan_t_250 = []
jan_t_200 = []
jan_t_150 = []
jan_t_100 = []

# %%
jan_dp_700 = []
jan_dp_500 = []
jan_dp_400 = []
jan_dp_300 = []
jan_dp_250 = []
jan_dp_200 = []
jan_dp_150 = []
jan_dp_100 = []

# %%
for i in range(len(list_jan_data)):
    jan_t_700.append(list_jan_data[i][4][1])
    jan_t_500.append(list_jan_data[i][5][1])
    jan_t_400.append(list_jan_data[i][6][1])
    jan_t_300.append(list_jan_data[i][7][1])
    jan_t_250.append(list_jan_data[i][8][1])
    jan_t_200.append(list_jan_data[i][9][1])
    jan_t_150.append(list_jan_data[i][10][1])
    jan_t_100.append(list_jan_data[i][11][1])
    #dewpoints
# %%
for i in range(len(list_jan_data)):
    if i == 5:
        continue
        jan_dp_250.append(list_jan_data[i][10][2])
    elif i == 33:
        continue
        jan_dp_250.append(list_jan_data[i][10][2])
    elif i == 45:
        continue
        jan_dp_250.append(list_jan_data[i][10][2])
    jan_dp_700.append(list_jan_data[i][4][2])
    jan_dp_500.append(list_jan_data[i][5][2])
    jan_dp_400.append(list_jan_data[i][6][2])
    jan_dp_300.append(list_jan_data[i][7][2])
    jan_dp_250.append(list_jan_data[i][8][2])
    jan_dp_200.append(list_jan_data[i][9][2])
    jan_dp_250.append(list_jan_data[i][10][2])
    jan_dp_100.append(list_jan_data[i][11][2])
# %%
jan_700 = np.nanmean(np.array(jan_t_700).astype(float))
jan_500 = np.nanmean(np.array(jan_t_500).astype(float))
jan_400 = np.nanmean(np.array(jan_t_400).astype(float))
jan_t_300[33] = float('NaN')
jan_300 = np.nanmean(np.array(jan_t_300).astype(float))
jan_t_200[33] = float('NaN')
jan_t_250[33] = float('NaN')
jan_250 = np.nanmean(np.array(jan_t_250).astype(float))
jan_200 = np.nanmean(np.array(jan_t_200).astype(float))
jan_t_150[5] = float('NaN')
jan_t_150[45] = float('NaN')
jan_150 = np.nanmean(np.array(jan_t_150).astype(float))
jan_t_100[5] = float('NaN')
jan_t_100[45] = float('NaN')
jan_100 = np.nanmean(np.array(jan_t_100).astype(float))

# %%
jan_dp_700 = np.nanmean(np.array(jan_dp_700).astype(float))
jan_dp_500 = np.nanmean(np.array(jan_dp_500).astype(float))
jan_dp_400 = np.nanmean(np.array(jan_dp_400).astype(float))
#jan_dp_t_300[25] = float('NaN')
jan_dp_300 = np.nanmean(np.array(jan_dp_300).astype(float))
#jan_dp_t_250[25] = float('NaN')
jan_dp_250 = np.nanmean(np.array(jan_dp_250).astype(float))
jan_dp_200 = np.nanmean(np.array(jan_dp_200).astype(float))
jan_dp_150 = np.nanmean(np.array(jan_dp_150).astype(float))
jan_dp_100 = np.nanmean(np.array(jan_dp_100).astype(float))

pres_levels = [sfc_pres_jan_mean, 700, 500, 400, 300, 250, 200, 150, 100]
temp_jan = [sfc_temp_jan_mean, jan_700, jan_500, jan_400, jan_300, jan_250, jan_200, jan_150, jan_100]
dwpt_jan = [sfc_dpt_jan_mean, jan_dp_700, jan_dp_500, jan_dp_400, jan_dp_300, jan_dp_250, jan_dp_200, jan_dp_150, jan_dp_100]


temp_jul = [sfc_temp_jul_mean, jul_700, jul_500, jul_400, jul_300, jul_250, jul_200, jul_150, jul_100]
dwpt_jul = [sfc_dpt_jul_mean, jul_dp_700, jul_dp_500, jul_dp_400, jul_dp_300, jul_dp_250, jul_dp_200, jul_dp_150, jul_dp_100]


temp_jan = np.array(temp_jan)
dwpt_jan = np.array(dwpt_jan)

temp_jul = np.array(temp_jul)
dwpt_jul = np.array(dwpt_jul)


ddp_jan = []
ddp_jul = []
for i in range(len(temp_jan)):
    dpdp_jan.append(temp_jan[i] - dwpt_jan[i])
    dpdp_jul.append(temp_jul[i] - dwpt_jul[i])

# %% Making the figure 
fig = plt.figure(figsize = (9, 9))
skew = SkewT(fig, rotation = 45)
# %
#plt.gca().invert_yaxis()
#plt.yscale('log')
skew.plot(pres_levels, temp_jan,  color = 'red', label = 'January Temperature (\N{DEGREE SIGN}C)', linestyle = '--')
skew.plot(pres_levels, temp_jul, color = 'red', label = 'July Temperature (\N{DEGREE SIGN}C)')

skew.plot(pres_levels, dwpt_jan, color = 'blue', label = 'January Dewpoint (\N{DEGREE SIGN}C)', linestyle = '--')
skew.plot(pres_levels, dwpt_jul,  color = 'blue', label = 'July Dewpoint (\N{DEGREE SIGN}C)')

skew.plot(pres_levels, dpdp_jan,  color = 'green', label = 'January Dewpoint Depression (\N{DEGREE SIGN}C)', linestyle = '--')
skew.plot(pres_levels, dpdp_jul,  color = 'green', label = 'July Dewpoint Depression (\N{DEGREE SIGN}C)')

#skew.yscale("log", base = 10)
skew.ax.set_ylim(1000, 100)
skew.ax.set_xlim(-30, 110)
skew.ax.set_ylabel('Pressure (hPa)', fontsize = 18)
skew.ax.set_xlabel('Temperature (\N{DEGREE SIGN}C)', fontsize = 18)
skew.ax.set_title('January Sounding Vs. July Sounding in Reno, NV 2021', fontsize = 18)
skew.ax.tick_params(axis='x', labelsize=12)
skew.ax.tick_params(axis='y', labelsize=12)
skew.plot_dry_adiabats(alpha = 0.2)
skew.plot_moist_adiabats(alpha = 0.2)
skew.plot_mixing_lines(alpha = 0.2)
#plt.yticks(ticks = major)
# plt.xlabel("Temperature (C)", fontsize = 18, fontweight = 'bold')
# plt.ylabel('Pressure (hPa)', fontsize = 18, fontweight = 'bold')
# plt.title("Sounding for January and July 2021 Reno, Nevada", fontsize = 18, fontweight = 'bold')
#plt.grid()
plt.legend()
plt.show()





