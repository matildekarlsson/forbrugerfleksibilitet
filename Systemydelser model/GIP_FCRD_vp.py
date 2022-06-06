# -*- coding: utf-8 -*-
"""
Created on Sun Jun  5 12:13:59 2022

@author: mie_h
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from GIT_spot_vp import varme, Mat_21_DK2, Mat_time_21


mængde_vp_mat = []
pris_vp_mat = []
# kun for dag 1
for j in range(len(Mat_21_DK2)):
    mængde_vp = []
    pris_vp = []
    for i in range(24):
        if varme[j][i]>0 and i<23:
            mængde_vp.append(min(8/3.8 - varme[j][i+1],varme[j][i])*0.8) #500 varmepumper i puljen
            pris_vp.append(Mat_21_DK2[j,i+1]-Mat_21_DK2[j,i])
        elif i == 23:
            mængde_vp.append(0)
            pris_vp.append(1000)
        else:
            mængde_vp.append(0)
            pris_vp.append(1000)
    mængde_vp_mat.append(mængde_vp)
    pris_vp_mat.append(pris_vp)

'''
mængde_vp_mat = []
pris_vp_mat = []
# kun for dag 1
for j in range(len(Mat_21)):
    mængde_vp = []
    pris_vp = []
    for i in range(24):
        if varme[j][i]>0 and i<23 and i>0:
            mængde_vp.append(min(8/3.8 - varme[j][i+1],varme[j][i]-mængde_vp[i-1])*0.8) #500 varmepumper i puljen
            pris_vp.append(Mat_21_DK2[j,i+1]-Mat_21_DK2[j,i])
        elif i == 23:
            mængde_vp.append(0)
            pris_vp.append(1000)
        elif i ==0:
            mængde_vp.append(min(8/3.8 - varme[j][i+1],varme[j][i])*0.8) #500 varmepumper i puljen
            pris_vp.append(Mat_21_DK2[j,i+1]-Mat_21_DK2[j,i])
        else:
            mængde_vp.append(0)
            pris_vp.append(1000)
    mængde_vp_mat.append(mængde_vp)
    pris_vp_mat.append(pris_vp)
'''

mængde_vp_MAT = np.reshape(np.array(mængde_vp_mat),[len(mængde_vp_mat),24])
pris_vp_MAT = np.reshape(np.array(pris_vp_mat),[len(mængde_vp_mat),24])


plt.figure()
plt.bar(np.arange(0,24,1),varme[1]*0.8,color='blue')
plt.bar(np.arange(0,24,1),mængde_vp_mat[1][:],color='red',alpha=0.5)

    
##############################################
##############     FCR-D      ################
##############################################

df_fcr = pd.read_csv('fcrreservesdk2.csv').iloc[23:8783] # måske lav noget ignore index
fcr_D = df_fcr.FCR_D_UpPriceDKK.tolist()
FCR_D_MAT = np.reshape(np.array(fcr_D),[365,24])



indtjening_list = []
k = 1
bud_pris_list = np.arange(100,300,5)

for i in bud_pris_list:
    BUD_PRIS = i
    bud_vp_mat = []
    for j in range(len(mængde_vp_mat)):
        bud_vp=[]
        for i in range(24):
            if pris_vp_mat[j][i] <=BUD_PRIS:
                bud_vp.append(BUD_PRIS)
            else:
                bud_vp.append(pris_vp_mat[j][i])
        bud_vp_mat.append(bud_vp)
    
    besparelse_vp_FCRD = []
    bud_vp_mængde = []
    
    for j in range(len(mængde_vp_mat)):
        besparelse_vp=[]
        bud_mængde = []
        for i in range(24):
            if mængde_vp_mat[j][i]*(700/1000) > 0.3 and bud_vp_mat[j][i]<= FCR_D_MAT[j,i]:
                besparelse_vp.append(bud_vp_mat[j][i]*mængde_vp_mat[j][i]*(700/1000)
                -k*pris_vp_mat[j][i]*mængde_vp_mat[j][i]*(700/1000)*1) #evt gang den fratrukkede mængde med 0.2
                bud_mængde.append(mængde_vp_mat[j][i])
            else:
                besparelse_vp.append(0)
                bud_mængde.append(0)
        besparelse_vp_FCRD.append(besparelse_vp)
        bud_vp_mængde.append(bud_mængde)
    
    
    indtjening_list.append(np.sum(besparelse_vp_FCRD))


print('Optimal budpris: ',bud_pris_list[indtjening_list.index(max(indtjening_list))])
print('Tilhørende indtjening: ',max(indtjening_list))


plt.figure()
plt.plot(bud_pris_list, indtjening_list, 'o-',color='blue')
plt.ylabel('Indtjening [DKK]')
plt.xlabel('Budpris [DKK/MW]')
plt.title('Indtjening af FCR-D som funktion af budpris (varmepumper)')




plt.figure()
plt.bar(np.arange(0,24,1),varme[1][:]*0.8,color='blue',label='Forbrug')
plt.bar(np.arange(0,24,1),mængde_vp_mat[1][:],color='red',alpha=0.55,label='Tilgængelig budmængde')
plt.xlabel("Time på døgnet")
plt.ylabel("kWh")
plt.title("Spotprisoptimeret forbrug 2. januar")
plt.ylim([0,2.1])
plt.legend()

plt.figure()
plt.bar(np.arange(0,24,1),varme[139][:]*0.8,color='blue',label='Forbrug')
plt.bar(np.arange(0,24,1),mængde_vp_mat[139][:],color='red',alpha=0.55,label='Tilgængelig budmængde')
plt.xlabel("Time på døgnet")
plt.ylabel("kWh")
plt.title("Spotprisoptimeret forbrug 20. maj")
plt.ylim([0,2.1])
plt.legend()

#plt.bar(np.arange(0,24,1),mængde_vp_mat[14][:],color='red',alpha=0.5)
plt.bar(np.arange(0,24,1),mængde_vp_mat[1][:],color='red',alpha=0.5)
plt.title('Varmepumpe spotoptimeret måned: '+str(Mat_time_21[17,0].month))


