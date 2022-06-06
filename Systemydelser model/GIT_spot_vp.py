# -*- coding: utf-8 -*-
"""
Created on Sun Jun  5 12:08:05 2022

@author: mie_h
"""

import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from MIP_elbil import OptCoh, OptWeekend, OptVandEL
#mFRR
#---------------- Load data -------------- ###########
df_DK1 = pd.read_csv('Elspot_DK1.csv', sep = ',')
df_DK2 = pd.read_csv('Elspot_DK2.csv', sep = ',')

timedf = df_DK1.HourDK

#laver tidslisten om med datetime
DK1_2022 = []
time_2022 = []
DK1_2021 = []
time_2021 = []

DK2_2022 = []
DK2_2021 = []


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



# også for de andre år

plt.figure()
plt.title('Elspot prices')
plt.plot(time_2021,DK1_2021,color='red', markersize=2, label='DK1')
plt.plot(time_2021,DK2_2021,color='blue', markersize=2, label='DK2')
plt.xlabel('time')
plt.ylabel('DKK/MWh')
plt.legend()


DK1_21 = DK1_2021[::-1]
DK2_21 = DK2_2021[::-1]
time_21 = time_2021[::-1]

month_21 = []
for i in range(len(time_21)):
    month_21.append(time_21[i].month)


DK1_21m = np.array(DK1_21)
DK2_21m = np.array(DK2_21)
time_21m = np.array(time_21) 
month_21m = np.array(month_21)

Mat_21_DK2 = np.reshape(DK2_21m,[365,24])
Mat_21_DK1 = np.reshape(DK1_21m,[365,24])
Mat_time_21 = np.reshape(time_21m,[365,24])
Mat_month_21 = np.reshape(month_21m,[365,24])

Mat_21 = Mat_21_DK1

mean_21_DK1 = np.mean(Mat_21,axis = 0)
mean_21_DK2 = np.mean(Mat_21_DK2,axis = 0)

plt.figure()
plt.title('Hourly spot price DK1')
plt.plot(mean_21_DK1,color='green', markersize=2, label='DK1 2021')
plt.plot(mean_21_DK2,color='blue', markersize=2, label='DK2 2021')
plt.xlabel('time')
plt.ylabel('DKK/MWh')
plt.grid()
plt.legend()




################################################
################################################
#######                                 ########   
#######           VARMEPUMPER           ########
#######                                 ########   
################################################
################################################


month_percent = [0.146,0.138,0.128,0.096,0.058,0.035,0.026,0.025,0.042,0.071,0.103,0.132]
gns_varmeforbrug = 12000 #kWh om året
gns_varmeforbrug_luft = 9000 #kWh om året 

væske_vand = 5246 #kWh forbrug væske-til-vand om året
luft_vand = 5746 #kWh forbrug luft-til-vand om året
luft_luft = 3732 #kWh forbrug luft-til-luft om året

væske_p = 0.36 # procent andel af væske-til-vand i puljen
vand_p = 0.43 # procent andel af luft-til-vand i puljen
luft_p = 0.21 # procent andel af luft-til-luft i puljen

gns_elforbrug = 5500 #kWh om året
gns_elforbrug_luft = 3700 #kWh om året 
gns_elforbrug_gns = væske_p*væske_vand + vand_p*luft_vand+luft_p*luft_luft 

antal_dage = [31,28,31,30,31,30,31,31,30,31,30,31]
months = ['jan', 'feb', 'mar', 'apr', 'maj', 'jun', 'jul', 'aug', 'sep', 'okt', 'nov', 'dec']

month_daily_vand = []
month_daily_luft = []

el_daily_vand = []
el_daily_luft = []
el_daily_gns = []
for i in range(12):
    month_daily_vand.append((month_percent[i]*gns_varmeforbrug)/antal_dage[i])
    month_daily_luft.append((month_percent[i]*gns_varmeforbrug_luft)/antal_dage[i])
    el_daily_vand.append((month_percent[i]*gns_elforbrug)/antal_dage[i])
    el_daily_luft.append((month_percent[i]*gns_elforbrug_luft)/antal_dage[i])
    el_daily_gns.append((month_percent[i]*gns_elforbrug_gns)/antal_dage[i])

plt.figure(figsize=(10,5))
plt.plot(months,el_daily_vand,'o-', label='Væske/luft-til-vand')
plt.plot(months,el_daily_luft,'o-',label='Luft-til-luft')
plt.plot(months,el_daily_gns,'o-', label='Vægtet gennemsnit')
plt.ylabel('Dagligt elforbrug [kWh/dag/varmepumpe]')
plt.xlabel('Tidspunkt på året')
plt.ylim([0,30])
plt.legend()



#vand_varmepumpe, obj = OptVandEL(Mat_21[0,:],el_daily_vand[0],5,3,2,7,el_daily_vand[0]/3)

vand_list = []
obj_list = []
diff = []
forbrug = []

for i in range(len(Mat_time_21)):
    amount = el_daily_gns[Mat_time_21[i,0].month-1]
    vand_varmepumpe, obj = OptVandEL(Mat_21_DK2[i,:],amount,7,3.33,3,7,amount*0.2364)
    vand_list.append(vand_varmepumpe)
    obj_list.append(obj)
    diff.append(sum(vand_varmepumpe)-amount)
    forbrug.append(sum(vand_varmepumpe))
aarlig_udgift_vand = sum(obj_list) # = XX DKK i udgift til luft-til-vand varmepumpe


print(aarlig_udgift_vand*700)

plt.bar(np.arange(0,24,1),vand_list[1])
plt.ylim([0,2.4])
plt.title('Varmepumpe spotoptimeret måned: '+str(Mat_time_21[17,0].month))

varme = np.reshape(np.array(vand_list),[365,24])

df_varmepumpe = pd.DataFrame(data=varme)
df_varmepumpe.to_csv('Varmepumpe_input_8_3_8_3_7_025.csv', index=False)


np.savetxt("varme_januar.csv", 
           varme,
           delimiter =", ", 
           fmt ='% s')

plt.figure()
plt.bar(np.arange(0,24,1),varme[1][:]*0.8,color='blue',label='Forbrug')
plt.xlabel("Time på døgnet")
plt.ylabel("kWh")
plt.title("Spotprisoptimeret forbrug 2. januar")
plt.ylim([0,2.1])
plt.legend()

plt.figure()
plt.bar(np.arange(0,24,1),varme[139][:]*0.8,color='blue',label='Forbrug')
plt.xlabel("Time på døgnet")
plt.ylabel("kWh")
plt.title("Spotprisoptimeret forbrug 20. maj")
plt.ylim([0,2.1])
plt.legend()



