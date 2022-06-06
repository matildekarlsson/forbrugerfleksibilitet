# -*- coding: utf-8 -*-
"""
Created on Sun Jun  5 12:20:10 2022

@author: mie_h
"""
# -*- coding: utf-8 -*-
"""
Created on Fri May 20 16:54:16 2022

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


test = pd.read_csv('obj_list.csv', sep = ';')

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
DK1_19 = DK1_2019[::-1]
DK2_19 = DK2_2019[::-1]
time_19 = time_2019[::-1]

# også for de andre år

plt.figure()
#plt.title('Elspot prices')
#plt.plot(time_2021,DK1_2021,color='red', markersize=2, label='DK1')
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

Mat_21 = Mat_21_DK2

mean_21_DK1 = np.mean(Mat_21,axis = 0)
mean_21_DK2 = np.mean(Mat_21_DK2,axis = 0)

plt.figure()
#plt.title('Hourly spot price DK1')
#plt.plot(mean_21_DK1,color='green', markersize=2, label='DK1 2021')
plt.plot(mean_21_DK2,color='blue', markersize=2)
plt.xlabel('Time på døgnet')
plt.ylabel('DKK/MWh')
#plt.grid()
#plt.legend()


#Lav til CSV filer
'''
mDK1_21 = [[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]+DK1_21]
mat_month_21 = [[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]+month_21]

Mat_dk1_21 = np.reshape(mDK1_21,[366,24])
Mat_month_21 = np.reshape(mat_month_21,[366,24])


np.savetxt("spot_DK1_21.csv", 
           Mat_21,
           delimiter =", ", 
           fmt ='% s')

np.savetxt("SPOT_DK1_21.csv", 
           Mat_dk1_21,
           delimiter =", ", 
           fmt ='% s')

np.savetxt("month_21.csv", 
           Mat_month_21,
           delimiter =", ", 
           fmt ='% s')
'''

## natopladning
natopladning_ekstra =[]
y_list_ekstra = []
objekt_ekstra = []
objekt_ekstra_pulje = []
for i in range(len(Mat_21_DK2)):
    #vand_varmepumpe, obj = OptVand(Mat_21[i,:],59,4,3,2,7,59/3)
    if Mat_time_21[i,0].dayofweek == 4:
        w = 6 #kl 06 om morgenen tages bilen i brug
        w1 = 15+1 # kl 15 sættes bilen til opladning igen
        m = 50 #60 elbiler sidder til ekstra natopladning fredag morgen
        M = m*10/1000
        x,y,o = OptWeekend(Mat_21_DK2[i,:],w,24,1,w,0,10,11)
    elif Mat_time_21[i,0].dayofweek == 5:
        w = 6 #kl 06 om morgenen tages bilen i brug
        w1 = 19+1 # kl 20 sættes bilen til opladning igen
        m = 15 #25 elbiler sidder til ekstra natopladning lørdag morgen
        x,y,o = OptWeekend(Mat_21_DK2[i,:],w,24,1,w,0,10,11)
        #EVT TJEK OM w=6 betyder den oplader til og med time 6?
        M = m*10/1000 #MW
    elif Mat_time_21[i,0].dayofweek == 6:
        w = 6 #kl 06 om morgenen tages bilen i brug
        w1 = 15+1 # kl 15 sættes bilen til opladning igen
        m = 30 #30 elbiler sidder til ekstra opladning søndag aften
        x,y,o = OptWeekend(Mat_21_DK2[i,:],w,w1,w1,23,0,10,11)
        M = m*10/1000 #MW
    else:
        w = 6
        w1 = 19+1
        m = 0
        x,y,o = OptWeekend(Mat_21_DK2[i,:],w,24,10,15,0,0,11)
        M = m*10/1000 #MW
    indx = y.tolist().index(max(y.tolist()))
    natopladning_ekstra.append([indx,w-1,M])
    # w laves om til index, sådan så w=kl6 = index 5
    y_list_ekstra.append(y.tolist())
    objekt_ekstra.append(o)
    objekt_ekstra_pulje.append(o*m)


## natopladning
natopladning =[]
y_list = []
objekt = []
objekt_pulje = []
for i in range(len(Mat_21_DK2)):
    #vand_varmepumpe, obj = OptVand(Mat_21[i,:],59,4,3,2,7,59/3)
    if Mat_time_21[i,0].dayofweek == 4:
        w = 6 #kl 06 om morgenen tages bilen i brug
        w1 = 15+1 # kl 15 sættes bilen til opladning igen
        m = 190 #230 elbiler sidder til natopladning om fredagen
        # 230 fra 00-06 og 115 ish fra 15-24
        x,y,o = OptWeekend(Mat_21_DK2[i,:],w,w1,10,15,10,0,11)
        M = m*10/1000 #MW
    elif Mat_time_21[i,0].dayofweek == 5:
        w = 6 #kl 06 om morgenen tages bilen i brug
        w1 = 19+1 # kl 19 sættes bilen til opladning igen
        m = 195 #230 elbiler sidder til natopladning om lørdagen
        x,y,o = OptWeekend(Mat_21_DK2[i,:],w,w1,10,15,10,0,11)
        M = m*10/1000 #MW
    elif Mat_time_21[i,0].dayofweek == 6:
        w = 6 #kl 06 om morgenen tages bilen i brug
        w1 = 15+1 # kl 15 sættes bilen til opladning igen
        m = 180 #230 elbiler sidder til natopladning om søndagen
        x,y,o = OptWeekend(Mat_21_DK2[i,:],w,w1,10,15,10,0,11)
        M = m*10/1000 #MW
    else:
        w = 6
        w1 = 19+1
        m = 240
        x,y,o = OptWeekend(Mat_21_DK2[i,:],w,w1,10,15,10,0,11)
        M = m*10/1000 #MW
    indx = y.tolist().index(max(y.tolist()))
    natopladning.append([indx,w-1,M])
    # w laves om til index, sådan så w=kl6 = index 5
    y_list.append(y.tolist())
    objekt.append(o)
    objekt_pulje.append(o*m)



print('Årlig udgift spotoptimeret nattilsluttet elbil DK1: ',sum(objekt), ' DKK')

objekt_dag = []
dagsopladning =[]
time_list = []
objekt_dag_pulje = []
for i in range(len(Mat_21_DK2)):
    #vand_varmepumpe, obj = OptVand(Mat_21[i,:],59,4,3,2,7,59/3)
    if Mat_time_21[i,0].dayofweek == 4:
        w = 9+1 #kl 09 om morgenen sættes bilen til opladning 
        w1 = 13 # kl 13 frakobles bilen
        m = 60 #38 elbiler sidder til dagsopladning om fredagen
        x,time,o = OptWeekend(Mat_21_DK2[i,:],6,19,w,w1,0,10,11)
        M = m*10/1000 #MW
    elif Mat_time_21[i,0].dayofweek == 5:
        w = 8+1 #kl 09 om morgenen sættes bilen til opladning 
        w1 = 15 # kl 13 frakobles bilen
        m = 90 #antal elbiler sidder til dagsopladning om lørdagen
        x,time,o = OptWeekend(Mat_21_DK2[i,:],6,19,w,w1,0,10,11)
        M = m*10/1000 #MW
    elif Mat_time_21[i,0].dayofweek == 6:
        w = 7+1 #tidspunkt for hvornår bilen sættes til opladning
        w1 = 13 # kl 13 frakobles bilenn
        m = 90 #antal elbiler sidder til dagsopladning om søndagen
        x,time,o = OptWeekend(Mat_21_DK2[i,:],6,19,w,w1,0,10,11)
        M = m*10/1000 #MW
    else:
        w = 9+1
        w1 = 15
        m = 60
        x,time,o = OptWeekend(Mat_21_DK2[i,:],6,19,w,w1,0,10,11)
        M = m*10/1000 #MW
    indx = time.tolist().index(max(time.tolist()))
    dagsopladning.append([indx,w1-1,M])
    # w laves om til index, sådan så w=kl6 = index 5
    time_list.append(time.tolist())
    objekt_dag.append(o)
    objekt_dag_pulje.append(o*m)

plt.figure()
plt.bar(np.arange(0,24,1),y_list[4+7])
#plt.ylim([0,1.7])
plt.title('Elbil spotoptimeret natopladning mandag')

print('Årlig udgift spotoptimeret dagstilsluttet elbil DK1: ',sum(objekt_dag), ' DKK')

print('Gns årlig spotoptimeret udigft: ', (sum(objekt_pulje)+sum(objekt_ekstra_pulje)+sum(objekt_dag_pulje))/300 )
