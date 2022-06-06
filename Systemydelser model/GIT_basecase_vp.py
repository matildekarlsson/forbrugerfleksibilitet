# -*- coding: utf-8 -*-
"""
Created on Sun Jun  5 12:32:33 2022

@author: mie_h

Kilder:

 https://styrdinvarmepumpe.dk/DataanalyserSDVPForskELprojekt12075.pdf    s. 18
 file:///C:/Users/mie_h/Downloads/2017-04_Varmebehov_dimensionering.pdf  s. 10
 http://www.roslev-fjernvarme.dk/Styringstabel.asp

"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from GIT_spot_vp import DK1_21, DK2_21



#anden fordeling i juni. juli og august

vand = [200,200,200,200,400,700,750,600,600,600,500,450,400,400,400,350,450,550,700,650,400,350,250,200]
rum = [3250,3400,3400,3600,3600,3350,3250,3350,3400,3250,3000,2850,2800,2800,2700,2750,2750,2750,2750,2900,2900,2950,3000,3000]
summer_perc = [0.05,0.06,0.08,0.1,0.15,0.6,0.75,0.45,0.25,0.15,0.1]
summer = []
rum_perc = []

plt.figure(figsize=(10,5))
plt.plot(vand, color = 'blue', label='Varmtvand')
plt.plot(rum, color = 'red', label='Rumvarme')
plt.legend()
plt.ylabel('Gennemsnitlig effekt [W]')
plt.xlabel('Time i døgnet')
plt.title('Gennemsnitlig varmtvands- og rumvarmeforbrug')

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

month_percent = [0.146,0.138,0.128,0.096,0.058,0.035,0.026,0.025,0.042,0.071,0.103,0.132]
antal_dage_22 = [31,28,31,30,31,30,31,31,30,31,30,31]
cum_dage_22 = np.cumsum(antal_dage_22)

varmepumpe = []
varmepumpe_luft = []
daily_percent_luft = []
month_forbrug = []
month_forbrug_luft = []
daily_percent_winter = []
daily_percent_summer = []
daily_percent_summer_gns = []
daily_percent_winter_gns = []
month = 0

for i in range(24):
    #summer.append(summer_perc[i]*vand[i]+(1-summer_perc[i])*rum[i])
    #rum_perc.append(vand[i]/(vand[i]+rum[i]))
    daily_percent_winter.append((vand[i]+rum[i])/(np.sum(vand)+np.sum(rum)))
    daily_percent_summer.append((vand[i]*4+rum[i])/(4*np.sum(vand)+np.sum(rum)))
    daily_percent_luft.append(rum[i]/np.sum(rum))
    daily_percent_winter_gns.append((væske_p+vand_p)*daily_percent_winter[i] 
                                    + luft_p*daily_percent_luft[i])
    daily_percent_summer_gns.append((væske_p+vand_p)*daily_percent_summer[i] 
                                    + luft_p*daily_percent_luft[i])
    #daily_percent_summer.append()

daily_amount_morning = (3*np.sum(daily_percent_summer_gns[3:8])+9*np.sum(daily_percent_winter_gns[3:8]))/12
daily_amount_morning = (np.sum(daily_percent_summer_gns[3:8])+np.sum(daily_percent_winter_gns[3:8]))/2
print('Daglig procent forbrug i tidsrummet 3 til 7: ',daily_amount_morning)

plt.figure()
plt.plot(daily_percent_winter,color='blue',label='Luft/væske-til-vand vinter')
plt.plot(daily_percent_summer,color='red',label='Luft/væske-til-vand sommer')
plt.plot(daily_percent_luft,color='gold',label='Luft-til-luft')
plt.plot(daily_percent_winter_gns,color='cyan',label = 'Gennemsnit vinter')
plt.plot(daily_percent_summer_gns,color='purple',label = 'Gennemsnit sommer')
plt.ylim([0.025,0.065])
plt.legend()

plt.figure(figsize=(10,5))
plt.plot(100*np.array(daily_percent_winter),color='blue',label='Luft/væske-til-vand vinter')
plt.plot(100*np.array(daily_percent_summer),color='red',label='Luft/væske-til-vand sommer')
plt.plot(100*np.array(daily_percent_luft),color='gold',label='Luft-til-luft')
plt.plot(100*np.array(daily_percent_winter_gns),color='cyan',label = 'Gennemsnit vinter')
plt.plot(100*np.array(daily_percent_summer_gns),color='purple',label = 'Gennemsnit sommer')
plt.ylim([2,7])
plt.ylabel('% af dagens forbrug')
plt.xlabel('Time på dagen')
plt.legend()


month_forbrug_gns = []
for i in range(len(month_percent)):
    month_forbrug.append(month_percent[i]*gns_elforbrug)
    month_forbrug_luft.append(month_percent[i]*gns_elforbrug_luft)
    month_forbrug_gns.append(month_percent[i]*gns_elforbrug_gns)

varmepumpe_gns = []
for k in range(12):
    for i in range(antal_dage_22[k]):
        for j in range(24):
            if k > 4 and k < 8:
                varmepumpe.append((month_forbrug[k]/antal_dage_22[k])*daily_percent_summer[j] )
                varmepumpe_luft.append((month_forbrug_luft[k]/antal_dage_22[k])*daily_percent_luft[j] )
                varmepumpe_gns.append((month_forbrug_gns[k]/antal_dage_22[k])*daily_percent_summer_gns[j])
            else:
                varmepumpe.append((month_forbrug[k]/antal_dage_22[k])*daily_percent_winter[j] )
                varmepumpe_luft.append((month_forbrug_luft[k]/antal_dage_22[k])*daily_percent_luft[j] )
                varmepumpe_gns.append((month_forbrug_gns[k]/antal_dage_22[k])*daily_percent_winter_gns[j])


timer = pd.date_range(start='2021-01-01 00:00', periods=8760, freq="1 h")


plt.figure(figsize=(15,5))
plt.plot(timer,varmepumpe,color='blue',label='Væske/luft-til-vand')
plt.plot(timer,varmepumpe_luft,color='gold',label='Luft-til-luft')
plt.plot(timer,varmepumpe_gns,color='lightgreen',label='Gennemsnit',alpha=0.8)
plt.ylabel('Timelgit forbrug [kWh/h]')
plt.xlabel('Tidspunkt på året')
plt.title('Timeligt elforbrug til varmepumpe over et år')
plt.legend()

np.sum(varmepumpe[:24])

'''
COP = 4
varmepumpe_elforbrug = [x / COP for x in varmepumpe]
varmepumpe_elforbrug_luft = [x / COP for x in varmepumpe_luft]
'''

timer = pd.date_range(start='2021-01-01 00:00', periods=8760, freq="1 h")


plt.figure(figsize=(15,5))
plt.plot(timer,varmepumpe)
plt.ylabel('kWh/h')
plt.xlabel('Tidspunkt på året')
plt.title('Elforbrug luft-til-vand varmepumpe')

plt.figure(figsize=(10,5))
plt.plot(timer[0:25],varmepumpe_gns[0:25])
plt.ylabel('kWh/h')
plt.xlabel('Tidspunkt på året')
plt.title('Vinterdag')

plt.figure(figsize=(10,5))
plt.plot(timer[4488:4513],varmepumpe_gns[4488:4513])
plt.ylabel('kWh/h')
plt.xlabel('Tidspunkt på året')
plt.title('Sommerdag')

plt.figure(figsize=(15,5))
plt.plot(timer,varmepumpe_luft)
plt.ylabel('kWh/h')
plt.xlabel('Tidspunkt på året')
plt.title('Elforbrug luft-til-luft varmepumpe')

plt.figure(figsize=(10,5))
plt.plot(timer[0:25],varmepumpe_luft[0:25])
plt.ylabel('kWh/h')
plt.xlabel('Tidspunkt på året')
plt.title('Vinterdag luft-til-luft')

plt.figure(figsize=(10,5))
plt.plot(timer[4488:4513],varmepumpe_luft[4488:4513])
plt.ylabel('kWh/h')
plt.xlabel('Tidspunkt på året')
plt.title('Sommerdag luft-til-luft')
      
            
##################################################################
                ###### BASE CASE VARMEPUMPER  ########
##################################################################

varmeudgift_gns_DK1 = []
varmeudgift_gns_DK2 = []


for i in range(8760):
    varmeudgift_gns_DK1.append((varmepumpe_gns[i]/1000)*DK1_21[i])
    varmeudgift_gns_DK2.append((varmepumpe_gns[i]/1000)*DK2_21[i])

gns_yearly_DK1 = np.sum(varmeudgift_gns_DK1)
gns_yearly_DK2 = np.sum(varmeudgift_gns_DK2)

print('Årlig udgift gennemsnitlig varmepumpe DK1: ',gns_yearly_DK1)  
print('Årlig udgift gennemsnitlig varmepumpe DK2: ',gns_yearly_DK2)




varmeudgift_luft_DK1 = []
varmeudgift_vand_DK1 = []
varmeudgift_luft_DK2 = []
varmeudgift_vand_DK2 = []

for i in range(8760):
    varmeudgift_luft_DK1.append((varmepumpe_luft[i]/1000)*DK1_21[i])
    varmeudgift_vand_DK1.append((varmepumpe[i]/1000)*DK1_21[i])
    varmeudgift_luft_DK2.append((varmepumpe_luft[i]/1000)*DK2_21[i])
    varmeudgift_vand_DK2.append((varmepumpe[i]/1000)*DK2_21[i])

luft_yearly_DK1 = np.sum(varmeudgift_luft_DK1)
vand_yearly_DK1 = np.sum(varmeudgift_vand_DK1)
luft_yearly_DK2 = np.sum(varmeudgift_luft_DK2)
vand_yearly_DK2 = np.sum(varmeudgift_vand_DK2)

print('Årlig udgift luft-til-luft DK1: ',luft_yearly_DK1)  
print('Årlig udgift luft/væske-til-vand DK1: ', vand_yearly_DK1)  
print('Årlig udgift luft-til-luft DK2: ',luft_yearly_DK2)  
print('Årlig udgift luft/væske-til-vand DK2: ', vand_yearly_DK2)
