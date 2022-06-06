# -*- coding: utf-8 -*-
"""
Created on Sun Jun  5 12:38:39 2022

@author: mie_h
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from GIT_spot_elbil import Mat_time_21, Mat_21_DK2, Mat_21_DK1



nat_y = []
nat_y1 = []
dag_y = []
dag_fra = []
nat_fra = []
nat_y_ekstra = []
nat_yx1 = []
amount_dag = []
amount_nat = []
amount_ekstra = []
amount_nat1 = []
amount_ekstra1 = []
for i in range(365):
    if Mat_time_21[i,0].dayofweek == 4:
        dag = [0,0,0,0,0,0,0,0,0,0,0,5,5,0,0,0,0,0,0,0,0,0,0,0]
        fra_d = [0,0,0,0,0,0,0,0,0,12,12,12,12,0,0,0,0,0,0,0,0,0,0,0]
        fra_n = [5,5,5,5,5,5,0,0,0,0,0,0,0,0,0,23,23,23,23,23,23,23,23,23]
        ekstra = [2.5,2.5,2.5,2.5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        dag_m = [0,0,0,0,0,0,0,0,0,60,60,60,60,0,0,0,0,0,0,0,0,0,0,0]
        ekstra_m = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        nat_m = [240,240,240,240,240,240,0,0,0,0,0,0,0,0,0,190,190,190,190,190,190,190,190,190]
        ekstra_m1 = [50,50,50,50,50,50,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        nat_m1 = [190,190,190,190,190,190,0,0,0,0,0,0,0,0,0,190,190,190,190,190,190,190,190,190]
        
    elif Mat_time_21[i,0].dayofweek == 5:
        dag = [0,0,0,0,0,0,0,0,0,0,0,10/3,10/3,10/3,0,0,0,0,0,0,0,0,0,0]
        fra_d = [0,0,0,0,0,0,0,0,14,14,14,14,14,14,14,0,0,0,0,0,0,0,0,0]
        fra_n = [5,5,5,5,5,5,0,0,0,0,0,0,0,0,0,0,0,0,0,23,23,23,23,23]
        ekstra = [2.5,2.5,2.5,2.5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        ekstra_m = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        dag_m = [0,0,0,0,0,0,0,0,90,90,90,90,90,90,90,0,0,0,0,0,0,0,0,0]
        nat_m = [210,210,210,210,210,210,0,0,0,0,0,0,0,0,0,0,0,0,0,195,195,195,195,195]
        ekstra_m1 = [15,15,15,15,15,15,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        nat_m1 = [195,195,195,195,195,195,0,0,0,0,0,0,0,0,0,0,0,0,0,195,195,195,195,195]

    elif Mat_time_21[i,0].dayofweek == 6:
        dag = [0,0,0,0,0,0,0,0,0,0,0,5,5,0,0,0,0,0,0,0,0,0,0,0]
        fra_d = [0,0,0,0,0,0,0,12,12,12,12,12,12,0,0,0,0,0,0,0,0,0,0,0]
        fra_n = [5,5,5,5,5,5,0,0,0,0,0,0,0,0,0,23,23,23,23,23,23,23,23,23]
        ekstra = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,10/3,10/3,10/3]
        ekstra_m = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,30,30,30]
        dag_m = [0,0,0,0,0,0,0,90,90,90,90,90,90,0,0,0,0,0,0,0,0,0,0,0]
        nat_m = [180,180,180,180,180,180,0,0,0,0,0,0,0,0,0,180,180,180,180,180,180,180,180,180]
        ekstra_m1 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,30,30,30]
        nat_m1 = [180,180,180,180,180,180,0,0,0,0,0,0,0,0,0,180,180,180,180,180,180,180,180,180]

        
    else:  
        dag = [0,0,0,0,0,0,0,0,0,0,0,10/3,10/3,10/3,0,0,0,0,0,0,0,0,0,0] 
        fra_d = [0,0,0,0,0,0,0,0,0,14,14,14,14,14,14,0,0,0,0,0,0,0,0,0]
        fra_n = [5,5,5,5,5,5,0,0,0,0,0,0,0,0,0,0,0,0,0,23,23,23,23,23]
        ekstra = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        ekstra_m = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        dag_m = [0,0,0,0,0,0,0,0,0,60,60,60,60,60,60,0,0,0,0,0,0,0,0,0]
        nat_m = [240,240,240,240,240,240,0,0,0,0,0,0,0,0,0,0,0,0,0,240,240,240,240,240]
        ekstra_m1 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]        
        nat_m1 = [240,240,240,240,240,240,0,0,0,0,0,0,0,0,0,0,0,0,0,240,240,240,240,240]
    
    dag_y.append((np.array(dag)/1000)*np.array(dag_m)*0.8)
    nat_y.append(np.array([2.5,2.5,2.5,2.5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])/1000*np.array(nat_m)*0.8)
    nat_y_ekstra.append((np.array(ekstra)/1000)*np.array(ekstra_m)*0.8)
    nat_y1.append(np.array([2.5,2.5,2.5,2.5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])/1000*np.array(nat_m1)*0.8)
    nat_yx1.append((np.array(ekstra)/1000)*np.array(ekstra_m1)*0.8)
    dag_fra.append(fra_d)
    nat_fra.append(fra_n)

uge_nat = nat_y1[3].tolist()+nat_y1[4].tolist()+nat_y1[5].tolist()+nat_y1[6].tolist()+nat_y1[7].tolist()+nat_y1[8].tolist()+nat_y1[9].tolist()
uge_dag = dag_y[3].tolist()+dag_y[4].tolist()+dag_y[5].tolist()+dag_y[6].tolist()+dag_y[7].tolist()+dag_y[8].tolist()+dag_y[9].tolist()
uge_ekstra = nat_yx1[3].tolist()+nat_yx1[4].tolist()+nat_yx1[5].tolist()+nat_yx1[6].tolist()+nat_yx1[7].tolist()+nat_yx1[8].tolist()+nat_yx1[9].tolist()
time = pd.date_range(start='2021-01-03 00:00', periods=168, freq="1 h")
time2 = pd.date_range(start='2021-01-04', periods=21, freq="8 h")

time1 = []
for i in range(21):
    #time1.append(str('0'+str(time2[i].day)+'-0'+str(time2[i].month)+' kl. '+str(time2[i].hour)))
    #time1.append(str(str(time2[i].day_name(locale='Danish'))+' - '+str(time2[i].hour)+':00'))
    time1.append(str(str(time2[i].day_name(locale='Danish'))+' kl. '+str(time2[i].hour)))
print(time1)

x=np.arange(0,168,1)

plt.figure(figsize=(10,5))
plt.plot(x,uge_nat,'o',markersize=3,color='blue',label='natopladning')
plt.plot(x,uge_dag,'o',markersize=3,color='red',label='dagsopladning')
plt.plot(x,uge_ekstra,'o',markersize=3,color='green',label='ekstraopladning')
plt.xlabel('Time på ugen')
plt.ylabel('Tilgængelig kapacitet i puljen [MW]')
plt.title('Fast forbrugsmønster mandag til søndag')
plt.xticks(np.arange(0,168,8),time1,rotation=50)
plt.legend()

import array_to_latex as a2l
latex_code = a2l.to_ltx(nat_y1, frmt = '{:6.2f}', arraytype = 'array')

m_energi = nat_y
frakobling = nat_fra

pris_matrix = []
mængde_matrix = []
for i in range(len(m_energi)):
    pris_not_opt = []
    mængde_not_opt = []
    for j in range(24): 
        if m_energi[i][j]  >= 0.3 and j+1 < frakobling[i][j]:
            pris_not_opt.append(min(Mat_21_DK2[i,j+1:frakobling[i][j]])-Mat_21_DK2[i,j])
            mængde_not_opt.append(m_energi[i][j])
        elif  m_energi[i][j]  >= 0.3 and j+1 == frakobling[i][j]:
            pris_not_opt.append(Mat_21_DK2[i,j+1]-Mat_21_DK2[i,j])
            mængde_not_opt.append(m_energi[i][j])
        else:
            pris_not_opt.append(1000)
            mængde_not_opt.append(0)
    pris_matrix.append(pris_not_opt)
    mængde_matrix.append(mængde_not_opt)

m_energi = dag_y
frakobling = dag_fra

pris_matrix_dag = []
mængde_matrix_dag = []
for i in range(len(m_energi)):
    pris_not_opt = []
    mængde_not_opt = []
    for j in range(24): 
        if m_energi[i][j]  >= 0.3 and j+1 < frakobling[i][j]:
            pris_not_opt.append(min(Mat_21_DK2[i,j+1:frakobling[i][j]])-Mat_21_DK2[i,j])
            mængde_not_opt.append(m_energi[i][j])
        elif  m_energi[i][j]  >= 0.3 and j+1 == frakobling[i][j]:
            pris_not_opt.append(Mat_21_DK2[i,j+1]-Mat_21_DK2[i,j])
            mængde_not_opt.append(m_energi[i][j])
        else:
            pris_not_opt.append(1000)
            mængde_not_opt.append(0)
    pris_matrix_dag.append(pris_not_opt)
    mængde_matrix_dag.append(mængde_not_opt)

###########################################
###               FCR-D                ###
##########################################
df_fcr = pd.read_csv('fcrreservesdk2.csv').iloc[23:8783] # måske lav noget ignore index
fcr_D = df_fcr.FCR_D_UpPriceDKK.tolist()
FCR_D_MAT = np.reshape(np.array(fcr_D),[365,24])


bud_fcrd = np.arange(100,260,5)
earnings_no = []
k=0
for p in bud_fcrd:
    BUD_FCRD = p
    
    bud_FCR_D = []
    
    for i in range(len(nat_y)):
        bud_elbil = []
        for j in range(24): 
            if pris_matrix[i][j] <= BUD_FCRD:
                bud_elbil.append(BUD_FCRD)
            else:
                bud_elbil.append(pris_matrix[i][j])
        bud_FCR_D.append(bud_elbil)
    
    besparelse_FCRD = []
    for i in range(len(nat_y)):
        saving_elbil = []
        for j in range(24): 
            if mængde_matrix[i][j] > 0.3 and bud_FCR_D[i][j] <=FCR_D_MAT[i,j]:
                saving_elbil.append(mængde_matrix[i][j]*(bud_FCR_D[i][j]-k*pris_matrix[i][j]))
            else:
                saving_elbil.append(0)
        besparelse_FCRD.append(saving_elbil)
    
  
    bud_FCR_D_day = []
    
    for i in range(len(dag_y)):
        bud_elbil_day  = []
        for j in range(24): 
            if pris_matrix_dag[i][j] <= BUD_FCRD:
                bud_elbil_day.append(BUD_FCRD)
            else:
                bud_elbil_day.append(pris_matrix_dag[i][j])
        bud_FCR_D_day.append(bud_elbil_day)
    
    besparelse_FCRD_day = []
    for i in range(len(dag_y)):
        saving_elbil_day = []
        for j in range(24): 
            if mængde_matrix_dag[i][j] > 0.3 and bud_FCR_D_day[i][j] <=FCR_D_MAT[i,j]:
                saving_elbil_day.append(mængde_matrix_dag[i][j]*(bud_FCR_D_day[i][j]-k*pris_matrix_dag[i][j]))
            else:
                saving_elbil_day.append(0)
        besparelse_FCRD_day.append(saving_elbil_day)
    
    earnings_no.append(np.sum(besparelse_FCRD)+np.sum(besparelse_FCRD_day))
    
    if p == 200:
        ind = np.sum(np.sum([besparelse_FCRD,besparelse_FCRD_day],axis=0),axis=1)
        tid =pd.date_range(start='01-01-2021 00:00', periods=365,freq='24 h')
        plt.figure(figsize=(10,5))
        plt.plot(tid,ind,'o',color='blue',markersize=3)
        plt.ylabel('Daglig indtjening [DKK]')
        plt.xlabel('Dag på året')


print('Optimal budpris: ',bud_fcrd[earnings_no.index(max(earnings_no))])
print('Tilhørende indtjening: ',max(earnings_no))

plt.figure()
plt.plot(bud_fcrd, earnings_no, 'o-',color='blue')
plt.ylabel('Indtjening [DKK]')
plt.xlabel('Budpris [DKK/MW]')
plt.title('Indtjening af FCR-D som funktion af budpris (elbiler fast forbrugsmønster)')



##################################
######       FFR           #######
##################################
ffr = pd.read_csv('FFR_2021.csv', sep = ';',header=0,decimal=",")
ffr_22 = pd.read_csv('ffrpurchaseddk2.csv')
ffr.columns=ffr_22.columns

df_FFR_22 =ffr_22.iloc[23:2758]
df_FFR_21 =ffr.iloc[:6001]

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
FFR_amount = np.reshape(np.array(dFFR.FFR_Purchased),[365,24])


bud_ffr_list = np.arange(100,1200,5)
earning_ffr = []
k=0
for p in bud_ffr_list:
    
    BUD_FFR = p
    
    bud_nat_ffr = []
    
    for i in range(len(nat_y)):
        bud_elbil = []
        for j in range(24): 
            if pris_matrix[i][j] <= BUD_FFR:
                bud_elbil.append(BUD_FFR)
            else:
                bud_elbil.append(pris_matrix[i][j])
        bud_nat_ffr.append(bud_elbil)
    
    bud_dag_ffr = []
    
    for i in range(len(nat_y)):
        bud_elbil = []
        for j in range(24): 
            if pris_matrix_dag[i][j] <= BUD_FFR:
                bud_elbil.append(BUD_FFR)
            else:
                bud_elbil.append(pris_matrix_dag[i][j])
        bud_dag_ffr.append(bud_elbil)
    
    
    besparelse_nat_ffr = []
    
    for i in range(len(nat_y)):
        saving_elbil = []
        for j in range(24): 
            if mængde_matrix[i][j] > 0.3 and bud_nat_ffr[i][j] <= FFR_mat[i,j]*7.44 and mængde_matrix[i][j]<=FFR_amount[i,j]:
                saving_elbil.append(mængde_matrix[i][j]*(FFR_mat[i,j]*7.44-k*pris_matrix[i][j]))
            elif mængde_matrix[i][j] > 0.3 and bud_nat_ffr[i][j] <= FFR_mat[i,j]*7.44 and mængde_matrix[i][j] > FFR_amount[i,j]:
                 saving_elbil.append(FFR_amount[i,j]*(bud_nat_ffr[i][j]-k*pris_matrix[i][j]))
            else:
                saving_elbil.append(0)
        besparelse_nat_ffr.append(saving_elbil)
    
    besparelse_day_ffr = []
    
    for i in range(len(nat_y)):
        saving_elbil = []
        for j in range(24): 
            if mængde_matrix_dag[i][j] > 0.3 and bud_dag_ffr[i][j] <= FFR_mat[i,j]*7.44 and mængde_matrix_dag[i][j]<=FFR_amount[i,j]:
                saving_elbil.append(mængde_matrix_dag[i][j]*(FFR_mat[i,j]*7.44-k*pris_matrix_dag[i][j]))
            elif mængde_matrix_dag[i][j] > 0.3 and bud_dag_ffr[i][j] <= FFR_mat[i,j]*7.44 and mængde_matrix_dag[i][j] > FFR_amount[i,j]:
                 saving_elbil.append(FFR_amount[i,j]*(bud_dag_ffr[i][j]-k*pris_matrix_dag[i][j]))
            else:
                saving_elbil.append(0)
        besparelse_day_ffr.append(saving_elbil)
    
    earning_ffr.append(np.sum(besparelse_day_ffr)+np.sum(besparelse_nat_ffr))
    
     
    if p == 625:
        ind = np.sum(np.sum([besparelse_day_ffr,besparelse_nat_ffr],axis=0),axis=1)
        tid =pd.date_range(start='01-01-2021 00:00', periods=365,freq='24 h')
        plt.figure(figsize=(10,5))
        plt.plot(tid,ind,'o',color='blue',markersize=3)
        plt.ylabel('Daglig indtjening [DKK]')
        plt.xlabel('Dag på året')


print('Optimal budpris: ',bud_ffr_list[earning_ffr.index(max(earning_ffr))])
print('Tilhørende indtjening: ',max(earning_ffr))

plt.figure()
plt.plot(bud_ffr_list, earning_ffr, 'o-',color='blue')
plt.ylabel('Indtjening [DKK]')
plt.xlabel('Budpris [DKK/MW]')
plt.title('Indtjening af FFR som funktion af budpris (elbiler fast forbrugsmønster)')

#########################################################################
###                                end                                ###
##########################################################################
