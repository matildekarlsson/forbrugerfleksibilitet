# -*- coding: utf-8 -*-
"""
Created on Sun Jun  5 12:21:49 2022

@author: mie_h
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df_DK1 = pd.read_csv('Elspot_DK1.csv', sep = ',')
df_DK2 = pd.read_csv('Elspot_DK2.csv', sep = ',')

timedf = df_DK1.HourDK

#laver tidslisten om med datetime
DK1_2022 = []
time_2022 = []
DK1_2021 = []
time_2021 = []
DK1_2020 = []
time_2020 = []
DK1_2019 = []
time_2019 = []
DK1_2018 = []
time_2018 = []

DK2_2022 = []
DK2_2021 = []
DK2_2020 = []
DK2_2019 = []
DK2_2018 = []

times = pd.to_datetime(timedf)


for i in range(len(times)):     
    if times[i].year == 2022:
        DK1_2022.append(df_DK1.SpotPriceDKK[i])
        DK2_2022.append(df_DK2.SpotPriceDKK[i])
        time_2022.append(times[i])
    if times[i].year == 2021:
        DK1_2021.append(df_DK1.SpotPriceDKK[i])
        DK2_2021.append(df_DK2.SpotPriceDKK[i])
        time_2021.append(times[i])
    if times[i].year == 2020:
        DK1_2020.append(df_DK1.SpotPriceDKK[i])
        DK2_2020.append(df_DK2.SpotPriceDKK[i])
        time_2020.append(times[i])
    if times[i].year == 2019:
        DK1_2019.append(df_DK1.SpotPriceDKK[i])
        DK2_2019.append(df_DK2.SpotPriceDKK[i])
        time_2019.append(times[i])
    if times[i].year == 2018:
        DK1_2018.append(df_DK1.SpotPriceDKK[i])
        DK2_2018.append(df_DK2.SpotPriceDKK[i])
        time_2018.append(times[i])

# De skal lige vendes om
DK1_18 = DK1_2018[::-1]
DK2_18 = DK2_2018[::-1]
time_18 = time_2018[::-1]

DK1_19 = DK1_2019[::-1]
DK2_19 = DK2_2019[::-1]
time_19 = time_2019[::-1]

DK1_20 = DK1_2020[::-1]
DK2_20 = DK2_2020[::-1]
time_20 = time_2020[::-1]

DK1_21 = DK1_2021[::-1]
DK2_21 = DK2_2021[::-1]
time_21 = time_2021[::-1]

DK1_22 = DK1_2022[::-1]
DK2_22 = DK2_2022[::-1]
time_22 = time_2022[::-1]

# også for de andre år

plt.figure()
plt.title('Elspot prices')
plt.plot(time_2021,DK1_2021,color='red', markersize=2, label='DK1')
plt.plot(time_2021,DK2_2021,color='blue', markersize=2, label='DK2')
plt.xlabel('time')
plt.ylabel('DKK/MWh')
plt.legend()

Mat_21_DK2 = np.reshape(DK2_21,[365,24])
Mat_21_DK1 = np.reshape(DK1_21,[365,24])
Mat_time_21 = np.reshape(time_21,[365,24])


Hverdag = pd.read_csv('Opladning_man_til_tor.csv', sep = ';',header=None)
Fredag = pd.read_csv('Opladning_fre.csv', sep = ';',header=None)
Lørdag = pd.read_csv('Opladning_lør.csv', sep = ';',header=None)
Søndag = pd.read_csv('Opladning_søn.csv', sep = ';',header=None)

gns_opladning = 10 #kWh antager at en bil i gns skal oplade 10 kWh hver dag  

hverdag = []
fredag = []
lørdag = []
søndag = []

for i in range(24):
    hverdag.append(Hverdag.iloc[i,0]*(gns_opladning/float(np.sum(Hverdag))))
    fredag.append(Fredag.iloc[i,0]*(gns_opladning/float(np.sum(Fredag))))
    lørdag.append(Lørdag.iloc[i,0]*(gns_opladning/float(np.sum(Lørdag))))
    søndag.append(Søndag.iloc[i,0]*(gns_opladning/float(np.sum(Søndag))))
    

'''
hverdag = Hverdag.iloc[:,0].tolist()
fredag = Fredag.iloc[:,0].tolist()
lørdag = Lørdag.iloc[:,0].tolist()
søndag = Søndag.iloc[:,0].tolist()
'''
plt.figure(figsize=(15,5))
plt.plot(Søndag,color='blue')
plt.title('Opladningsmønster søndag')
plt.xlabel('Hour of the day')
plt.ylabel('kWh/time')

uge = hverdag*4 + fredag + lørdag + søndag
opladning_21 = fredag + lørdag + søndag + 51*uge + 4*hverdag + fredag
mat_opladning_21 = np.reshape(opladning_21,[365,24])

plt.figure(figsize=(15,5))
plt.plot(uge,color='blue')
plt.xlabel('Time på ugen')
plt.ylabel('kWh/time')


elbil_udgift_DK1 = []
elbil_udgift_DK2 = []

for i in range(365):
    for j in range(24):
        elbil_udgift_DK1.append((mat_opladning_21[i,j]/1000)*Mat_21_DK1[i,j])
        elbil_udgift_DK2.append((mat_opladning_21[i,j]/1000)*Mat_21_DK2[i,j])

elbil_yearly_DK1 = np.sum(elbil_udgift_DK1)
elbil_yearly_DK2 = np.sum(elbil_udgift_DK2)

print('Base case årlig udgift elbiler DK1: ',elbil_yearly_DK1,' DKK')
print('Base case årlig udgift elbiler DK2: ',elbil_yearly_DK2,' DKK')


