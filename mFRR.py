import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


#mFRR rådigheds betaling 
#---------------- Load data -------------- ###########
df_DK1 = pd.read_csv('mFRRDK1_2021.csv', sep = ',')
df_DK2 = pd.read_csv('mFRRDK2_2021.csv', sep = ',')

timedf = df_DK1.HourDK

#laver tidslisten om med datetime
times = pd.to_datetime(timedf)

UpDK1 = df_DK1.mFRR_UpPurchased
DownDK1 = df_DK1.mFRR_DownPurchased
UpDK2 = df_DK2.mFRR_UpPurchased
DownDK2 = df_DK2.mFRR_DownPurchased

##-------------------------Undersøger    mFRR   timebaseret!!!------------###
x = [23,22,21,20,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,0]


MatrixDK1 = np.mean(UpDK1.to_numpy().reshape(-1,24),axis = 0)
MatrixDK2 = np.mean(UpDK2.to_numpy().reshape(-1,24), axis = 0)


###----------------------------------PRISER------------------------------####

UpDK1_Price = df_DK1.mFRR_UpPriceDKK
DownDK1_Price = df_DK1.mFRR_DownPriceDKK
UpDK2_Price = df_DK2.mFRR_UpPriceDKK
DownDK2_Price = df_DK2.mFRR_DownPriceDKK


plt.figure(figsize=(9,5))
#plt.title('Prices DK1 mFRR regulation')
plt.plot(times,UpDK1_Price,'o',color='red', markersize=2, label='Opregulering')
plt.plot(times,DownDK1_Price,'o',color='blue', markersize=2, label='Nedregulering')
#plt.ylim(0,80)
plt.xlabel('Tidspunkt på året')
plt.ylabel('DKK per MWh/h')
#plt.grid()
plt.legend()




plt.figure(figsize=(9,5))
#plt.title('Prices DK2 mFRR regulation')
plt.plot(times,UpDK2_Price,'o',color='red', markersize=2,label='Opregulering')
plt.plot(times,DownDK2_Price,'o',color='blue', markersize=2,label='Nedregulering')
plt.xlabel('Tidspunkt på året')
plt.ylabel('DKK per MWh/h')
#plt.grid()
plt.legend()




#mFRR aktiverede reserve _____________________________________________________


df_DK1a = pd.read_csv('realtimeDK1_2021.csv', sep = ',')
df_DK2a = pd.read_csv('realtimeDK2_2021.csv', sep = ',')


timedfa = df_DK1a.HourDK

#laver tidslisten om med datetime
timesa = pd.to_datetime(timedfa)

UpDK1a = df_DK1a.RegulatingPowerUp
DownDK1a = df_DK1a.RegulatingPowerDown
UpDK2a = df_DK2a.RegulatingPowerUp
DownDK2a = df_DK2a.RegulatingPowerDown

UpDK1a_Price = df_DK1a.BalancingPowerPriceUpDKK
DownDK1a_Price = df_DK1a.BalancingPowerPriceDownDKK
UpDK2a_Price = df_DK2a.BalancingPowerPriceUpDKK
DownDK2a_Price = df_DK2a.BalancingPowerPriceDownDKK



#-------------------------Hourly activated regulation --------------------



x = [23,22,21,20,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,0]


MatrixDK1a_Up = np.mean(UpDK1a[0:8736].to_numpy().reshape(-1,24),axis = 0)
MatrixDK2a_Up = np.mean(UpDK2a[0:8736].to_numpy().reshape(-1,24), axis = 0)

MatrixDK1a_Down = np.mean(DownDK1a[0:8736].to_numpy().reshape(-1,24),axis = 0)
MatrixDK2a_Down = np.mean(DownDK2a[0:8736].to_numpy().reshape(-1,24), axis = 0)




#---------------Prices for activated ---------------------------

plt.figure(figsize=(9,5))
#plt.title('Prices DK1 mFRR activated regulation')
plt.plot(timesa,UpDK1a_Price,'o',color='red', markersize=2, label='Opregulering')
plt.plot(timesa,DownDK1a_Price,'o',color='blue', markersize=2, label='Nedregulering')
#plt.ylim(-200,4000)
plt.xlabel('Tidspunkt på året')
plt.ylabel('DKK per MWh/h')
#plt.grid()
plt.legend()


plt.figure(figsize=(9,5))
#plt.title('Prices DK2 mFRR activated regulation')
plt.plot(timesa,UpDK2a_Price,'o',color='red', markersize=2,label='Opregulering')
plt.plot(timesa,DownDK2a_Price,'o',color='blue', markersize=2,label='Nedregulering')
#plt.ylim(-200,4000)
plt.xlabel('Tidspunkt på året')
plt.ylabel('DKK per MWh/h')
#plt.grid()
plt.legend()
