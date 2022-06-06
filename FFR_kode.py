
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


ffr = pd.read_csv('FFR_2021.csv', sep = ';',header=0,decimal=",")
ffr_22 = pd.read_csv('ffrpurchaseddk2.csv')
ffr.columns=ffr_22.columns

df_FFR_22 =ffr_22.iloc[23:2758]
df_FFR_21 =ffr.iloc[:6001]

time_FFR_21 = pd.to_datetime(df_FFR_21.HourDK)

del df_FFR_21['HourUTC']
del df_FFR_22['HourUTC']

#indsæt 24 værdier d 23. februar
df_23_02 = pd.DataFrame(data={'HourDK':pd.date_range(start='02-23-2022 00:00', 
                 end='02-23-2022 23:00',freq='1 h'),'FFR_Purchased':np.zeros(24),
                'FFR_AcceptedMW':np.zeros(24),'FFR_MarginalPriceEUR':np.zeros(24)})

dFFR = pd.concat([df_FFR_22[:1272],df_23_02,df_FFR_22[1272:],df_FFR_21],ignore_index=True)
dFFR['FFR_MarginalPriceEUR'] = dFFR['FFR_MarginalPriceEUR'].fillna(0)

FFR = dFFR.FFR_MarginalPriceEUR

FFR_mat = np.reshape(np.array(FFR),[365,24])


time_FFR = pd.to_datetime(dFFR.HourDK)

plt.figure(figsize=[8,5])
plt.plot(time_FFR,dFFR.FFR_MarginalPriceEUR,'o',markersize=2,color='blue')
plt.ylabel('MW/h')
plt.xlabel('time')
plt.title('Accepted FFR amount (DK2)')

plt.figure(figsize=[8,5])
plt.plot(time_FFR,FFR,'o',markersize=2,color='blue')
plt.ylabel('EUR/MW/h')
plt.xlabel('time')
plt.title('FFR price (DK2)')
plt.ylim([0,100])


plt.figure(figsize=[9,5])
plt.plot(time_FFR_21,df_FFR_21.FFR_AcceptedMW,'o',markersize=2,color='blue')
plt.ylabel('MW/h')
plt.xlabel('Tidspunkt på året')
plt.title('Accepteret mængde FFR 2021 (DK2)')

plt.figure(figsize=[9,5])
plt.plot(time_FFR_21,df_FFR_21.FFR_MarginalPriceEUR*7.44,'o',markersize=2,color='blue')
plt.ylabel('DKK/MW/h')
plt.xlabel('Tidspunkt på året')
plt.title('FFR rådighedsbetaling 2021 (DK2)')




