# -*- coding: utf-8 -*-
"""
Created on Mon Apr  4 10:15:11 2022

@author: mie_h
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#fcr_2021 = pd.read_csv('regelleistug_fcr_2021.csv',sep=';',decimal=",")
fcr_2021 = pd.read_csv('FCR_data_2021.csv',sep=';')


fcr_2021 = fcr_2021.rename(columns={"DK_SETTLEMENTCAPACITY_PRICE_[EUR/MW]": "price_DK1","DK_IMPORT(-)_EXPORT(+)_[MW]": "import_DK1"})

ny_test = np.arange(0,len(fcr_2021)-6,6)
liste = []
liste2 = []

for i in ny_test:
    if (fcr_2021.DATE_FROM[i] == fcr_2021.DATE_FROM[i+7]):
        liste.append(i+6)
        print('i =',i)
        print('fejl ved: ',fcr_2021.DATE_FROM[i])

for i in liste:
    if (fcr_2021.TENDER_NUMBER[i] == 2):
        liste2.append(i)
        print('slet række ',i,' til række ',i+5)

ny_df = fcr_2021.drop([liste2[0],liste2[0]+1,liste2[0]+2,liste2[0]+3,liste2[0]+4,liste2[0]+5,
               liste2[1],liste2[1]+1,liste2[1]+2,liste2[1]+3,liste2[1]+4,liste2[1]+5,
               liste2[2],liste2[2]+1,liste2[2]+2,liste2[2]+3,liste2[2]+4,liste2[2]+5,
               liste2[3],liste2[3]+1,liste2[3]+2,liste2[3]+3,liste2[3]+4,liste2[3]+5,
               liste2[4],liste2[4]+1,liste2[4]+2,liste2[4]+3,liste2[4]+4,liste2[4]+5],inplace=False)
ny_df = ny_df.set_index([pd.Series(np.arange(0,2190,1))])


newdf = pd.DataFrame(np.repeat(ny_df.values, 4, axis=0))
newdf.columns = ny_df.columns

hours = pd.date_range(start='2021-01-01 00:00:00', periods=8760, freq="1 h")
"""
plt.figure(figsize=(15,5))
plt.plot(hours[432:],newdf.price_DK1[432:],'o',markersize=2)
"""
pris = pd.to_numeric(newdf.price_DK1, errors='coerce')
mængde = pd.to_numeric(newdf.import_DK1, errors='coerce')

plt.figure(figsize=(15,5))
plt.plot(hours,(pris*7.44)/4,'o',markersize=2,color='blue')
plt.title('Pris af FCR 2021')
plt.xlabel('Tidspunkt på året')
plt.ylabel('Pris [DKK/MW/h]')
#plt.ylim(200,1000)
#plt.grid()
np.mean((pris*7.44)/4)

plt.figure(figsize=(10,5))
plt.plot(hours[432:432+24],pris[432:432+24],'o',markersize=2,color='blue')
plt.title('Pris af FCR DK1 2021 op- og nedregulering (symmetrisk ydelse)')
plt.xlabel('Tidspunkt på året')
plt.ylabel('Pris [EUR/MW]')

daily = np.mean(np.reshape(pris.to_numpy()[432:],[347,24]),axis = 0)

plt.figure(figsize=(8,5))
plt.plot(daily,'o-',color='blue')
plt.title('Pris af FCR DK1 på daglig basis')
plt.xlabel('Tidspunkt på dagen')
plt.ylabel('Pris [EUR/MW]')

plt.figure(figsize=(15,5))
plt.plot(hours,mængde,'o',markersize=2,color='blue')
plt.title('Import/eksport af FCR DK1 2021')
plt.xlabel('Tidspunkt på året')
plt.ylabel('Mængde eksporteret [MW]')

#newdf.price_DK1.astype('float64')



'''
test = np.arange(0,len(ny_df)-6,6)
liste3 = []
#liste1 = []
liste4 = []

for i in test:
    liste3.append(ny_df.DATE_FROM[i] == ny_df.DATE_FROM[i+2] == ny_df.DATE_FROM[i+4] == ny_df.DATE_FROM[i+5])
    if (ny_df.DATE_FROM[i] == ny_df.DATE_FROM[i+7]):
        print('i =',i)
        print('fejl ved: ',ny_df.DATE_FROM[i])

for i in range(len(ny_df)):
    if (ny_df.TENDER_NUMBER[i] == 2):
        liste4.append(i)
        print('tender 2 ved i =',i)
        print('fejl ved: ',ny_df.DATE_FROM[i])


for i in liste:
    if (fcr_2021.TENDER_NUMBER[i] == 2):
        liste2.append(i)
        print('slet række ',i,' til række ',i+5)



for i in liste2:
    fcr_2021.drop[i, i+1, i+2,i+3,i+4,i+5,i+6]

hours = pd.date_range(start='2021-01-01 00:00:00', periods=8760, freq="1 h")



'''
