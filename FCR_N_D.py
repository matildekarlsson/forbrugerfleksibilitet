import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


#FCR N og D - PRISER 
#----------------------------Load data -----------------------------############
df_FCR = pd.read_csv('FCRND_2021.csv', sep = ',')
FCR_D = df_FCR.FCR_D_UpPriceDKK
# Hov FCR-D er ku opregulering indtil videre 
FCR_N = df_FCR.FCR_N_PriceDKK

timedf = df_FCR.HourDK
#laver tidslisten om med datetime
times = pd.to_datetime(timedf)


plt.figure(figsize=(15,5))
plt.title('FCR-D regulation prices')
plt.plot(times,FCR_D,'o',color='blue', markersize=2)
plt.xlabel('Tidspunkt på året')
plt.ylabel('DKK per MWh/h')
plt.legend()

np.mean(FCR_N)

plt.figure(figsize=(15,5))
plt.title('DK2 FCR-N regulation prices')
plt.plot(times,FCR_N,'o',color='blue', markersize=2)
plt.xlabel('Tidspunkt på året')
plt.ylabel('DKK per MWh/h')
#plt.ylim(0,200)
plt.legend()


#np.savetxt("FCR_N_accepteret.csv", np.transpose([times, FCR_N]), delimiter=",", fmt = '% s')
