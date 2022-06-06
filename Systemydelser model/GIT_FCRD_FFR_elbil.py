# -*- coding: utf-8 -*-
"""
Created on Sun Jun  5 12:24:15 2022

@author: mie_h
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from GIT_spot_elbil import Mat_21_DK2, natopladning, natopladning_ekstra, dagsopladning

pris = []
mængde = []
for i in range(len(natopladning)):
    if natopladning[i][0] == natopladning[i][1] or natopladning[i][0] == 23:
        pris.append(1000)
        mængde.append(0)
    elif natopladning[i][0] + 1 == natopladning[i][1]:
        pris.append(Mat_21_DK2[i,natopladning[i][0]+1]-Mat_21_DK2[i,natopladning[i][0]])
        mængde.append(natopladning[i][2]*0.8)
    elif natopladning[i][0] > natopladning[i][1]: #hvis den oplader om aftenen før 23.00
        pris.append(min(Mat_21_DK2[i,natopladning[i][0]+1:23].tolist()+Mat_21_DK2[i,0:natopladning[i][1]].tolist())-Mat_21_DK2[i,natopladning[i][0]])
        mængde.append(natopladning[i][2]*0.8)
    else:
        pris.append(min(Mat_21_DK2[i,natopladning[i][0]+1:natopladning[i][1]])-Mat_21_DK2[i,natopladning[i][0]])
        mængde.append(natopladning[i][2]*0.8)
    #lav if statement om hvis den oplader om aftenen før 24


pris_ekstra = []
mængde_ekstra = []
for i in range(len(natopladning_ekstra)):
    if natopladning_ekstra[i][0] == natopladning_ekstra[i][1] or natopladning_ekstra[i][0] == 23:
        pris_ekstra.append(1000)
        mængde_ekstra.append(0)
    elif natopladning_ekstra[i][0] + 1 == natopladning_ekstra[i][1]:
        pris_ekstra.append(Mat_21_DK2[i,natopladning_ekstra[i][0]+1]-Mat_21_DK2[i,natopladning_ekstra[i][0]])
        mængde_ekstra.append(natopladning_ekstra[i][2]*0.8)
    elif natopladning_ekstra[i][0] > natopladning_ekstra[i][1]: #hvis den oplader om aftenen før 23.00
        pris_ekstra.append(min(Mat_21_DK2[i,natopladning_ekstra[i][0]+1:23].tolist()+Mat_21_DK2[i,0:natopladning_ekstra[i][1]].tolist())-Mat_21_DK2[i,natopladning_ekstra[i][0]])
        mængde_ekstra.append(natopladning_ekstra[i][2]*0.8)
    else:
        pris_ekstra.append(min(Mat_21_DK2[i,natopladning_ekstra[i][0]+1:natopladning_ekstra[i][1]])-Mat_21_DK2[i,natopladning_ekstra[i][0]])
        mængde_ekstra.append(natopladning_ekstra[i][2]*0.8)
    #lav if statement om hvis den oplader om aftenen før 24

#beregner piser og mængder for dagstilsluttede biler
pris_dag = []
mængde_dag = []
opregu_time = []
for i in range(len(dagsopladning)):
    if dagsopladning[i][0] == dagsopladning[i][1]:
        pris_dag.append(1000)
        mængde_dag.append(0)
    elif dagsopladning[i][0] + 1 == dagsopladning[i][1]:
        pris_dag.append(Mat_21_DK2[i,dagsopladning[i][0]+1]-Mat_21_DK2[i,dagsopladning[i][0]])
        mængde_dag.append(dagsopladning[i][2]*0.8)
    else:
        pris_dag.append(min(Mat_21_DK2[i,dagsopladning[i][0]+1:dagsopladning[i][1]])-Mat_21_DK2[i,dagsopladning[i][0]])
        mængde_dag.append(dagsopladning[i][2]*0.8)

#laver 2-dim liste til matrix
nat = np.reshape(natopladning,[len(natopladning),3])
nat_i = nat[:,0] #tidspunkt hvor elbilerne oplader

dag = np.reshape(dagsopladning,[len(dagsopladning),3])
dag_i = dag[:,0] #tidspunkt hvor elbilerne oplader

nat_ekstra = np.reshape(natopladning_ekstra,[len(natopladning_ekstra),3])
nat_i_ekstra = nat_ekstra[:,0] #tidspunkt hvor elbilerne oplader

##############################################
##############     FCR-D      ################
##############################################
df_fcr = pd.read_csv('fcrreservesdk2.csv').iloc[23:8783] # måske lav noget ignore index
fcr_D = df_fcr.FCR_D_UpPriceDKK.tolist()
FCR_D_MAT = np.reshape(np.array(fcr_D),[365,24])


bud_fcrd = np.arange(100,260,5)
k = 1
earnings = []

for j in bud_fcrd:
    BUD_FCRD = j
    
    bud_nat = []
    for i in range(len(pris)):
        if pris[i]<=BUD_FCRD:
            bud_nat.append(BUD_FCRD)
        else:
            bud_nat.append(pris[i])
    
    bud_dag = []
    for i in range(len(pris_dag)):
        if pris_dag[i]<=BUD_FCRD:
            bud_dag.append(BUD_FCRD)
        else:
            bud_dag.append(pris_dag[i])
    
    bud_nat_ekstra = []
    for i in range(len(pris_ekstra)):
        if pris_ekstra[i]<=BUD_FCRD:
            bud_nat_ekstra.append(BUD_FCRD)
        else:
            bud_nat_ekstra.append(pris_ekstra[i])
    
    besparelse_nat = []
    ### Evt. 0.8*mængde[i] > 0.3
    ### Konstant behov på 44 MW eller 624 MW - langt højere end max mængde,
    ### så vi regner med hele mængden altid vil accepteres,
    ### såfremt prisen er lavere den højest accepterede
    for i in range(len(pris)):
        if mængde[i] > 0.3 and bud_nat[i]<= FCR_D_MAT[i,int(nat_i[i])]:
            besparelse_nat.append(bud_nat[i]*mængde[i]-pris[i]*k*mængde[i]) #evt gang den fratrukkede mængde med 0.2, da det ikke er det hele der flyttes
        else:
            besparelse_nat.append(0)
    
    besparelse_nat_ekstra = []
    for i in range(len(pris_ekstra)):
        if mængde_ekstra[i] > 0.3 and bud_nat_ekstra[i]<= FCR_D_MAT[i,int(nat_i_ekstra[i])]:
            besparelse_nat_ekstra.append(bud_nat_ekstra[i]*mængde_ekstra[i]-pris_ekstra[i]*k*mængde_ekstra[i]) #evt gang den fratrukkede mængde med 0.2, da det ikke er det hele der flyttes
        else:
            besparelse_nat_ekstra.append(0)
    
    
    besparelse_dag = []
    
    for i in range(len(pris_dag)):
        if mængde_dag[i] > 0.3 and bud_dag[i]<= FCR_D_MAT[i,int(dag_i[i])]:
            besparelse_dag.append(bud_dag[i]*mængde_dag[i]-pris_dag[i]*k*mængde_dag[i]) #evt gang den fratrukkede mængde med 0.2, da det ikke er det hele der flyttes
        else:
            besparelse_dag.append(0)
    
    earnings.append(sum(besparelse_dag)+sum(besparelse_nat)+sum(besparelse_nat_ekstra))  
    
    if j == 220:
        ind = np.sum([besparelse_dag,besparelse_nat,besparelse_nat_ekstra],axis=0)
        tid =pd.date_range(start='01-01-2021 00:00', periods=365,freq='24 h')
        plt.figure(figsize=(10,5))
        plt.plot(tid,ind,'o',color='blue',markersize=3)
        plt.ylabel('Daglig indtjening [DKK]')
        plt.xlabel('Dag på året')

#print('Indtjening FCR-D: ',sum(besparelse_dag)+sum(besparelse_nat)+sum(besparelse_nat_ekstra))

print('Optimal budpris: ',bud_fcrd[earnings.index(max(earnings))])
print('Tilhørende indtjening: ',max(earnings))

plt.figure()
plt.plot(bud_fcrd, earnings, 'o-',color='blue')
plt.ylabel('Indtjening [DKK]')
plt.xlabel('Budpris [DKK/MW]')
plt.title('Indtjening af FCR-D som funktion af budpris (elbiler spotprisoptimeret)')

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

### FFR er marginalprisafregnet, men hvis vi kan byde ind med hele mængden
### så bliver marginalprisen lig med vores budpris. Derfor modificeres budprisen
### til at være med lig 75 EURO, da marginalprisen kun én gang på et år 
### er lavere end dette

bud_ffr_list = np.arange(100,1300,5)
indtjening_ffr_list = []
k=1
for j in bud_ffr_list:
    
    BUD_FFR = j
    
    bud_nat = []
    for i in range(len(pris)):
        if pris[i]<=BUD_FFR:
            bud_nat.append(BUD_FFR)
        else:
            bud_nat.append(pris[i])
    
    bud_nat_ekstra = []
    for i in range(len(pris_ekstra)):
        if pris_ekstra[i]<=BUD_FFR:
            bud_nat_ekstra.append(BUD_FFR)
        else:
            bud_nat_ekstra.append(pris[i])
    
    bud_dag = []
    for i in range(len(pris_dag)):
        if pris_dag[i]<=BUD_FFR:
            bud_dag.append(BUD_FFR)
        else:
            bud_dag.append(pris_dag[i]) 
    
    besparelse_nat = []
    ### Evt. 0.8*mængde[i] > 0.3
    for i in range(len(pris)):
        if mængde[i] > 0.3 and bud_nat[i]<= FFR_mat[i,int(nat_i[i])]*7.44 and mængde[i]<=FFR_amount[i,int(nat_i[i])]:
            besparelse_nat.append(mængde[i]*(FFR_mat[i,int(nat_i[i])]*7.44-k*pris[i])) 
        elif mængde[i] > 0.3 and bud_nat[i]<= FFR_mat[i,int(nat_i[i])]*7.44 and mængde[i]>FFR_amount[i,int(nat_i[i])]:
            besparelse_nat.append(FFR_amount[i,int(nat_i[i])]*(bud_nat[i]-k*pris[i])) 
        else:
            besparelse_nat.append(0)
    
    besparelse_nat_ekstra = []
    ### Evt. 0.8*mængde[i] > 0.3
    for i in range(len(pris_ekstra)):
        if mængde_ekstra[i] > 0.3 and bud_nat_ekstra[i]<= FFR_mat[i,int(nat_i_ekstra[i])]*7.44 and mængde_ekstra[i]<=FFR_amount[i,int(nat_i_ekstra[i])]:
            besparelse_nat_ekstra.append(mængde_ekstra[i]*(FFR_mat[i,int(nat_i_ekstra[i])]*7.44-k*pris_ekstra[i])) 
        elif mængde_ekstra[i] > 0.3 and bud_nat_ekstra[i]<= FFR_mat[i,int(nat_i_ekstra[i])]*7.44 and mængde_ekstra[i]>FFR_amount[i,int(nat_i_ekstra[i])]:
            besparelse_nat_ekstra.append(FFR_amount[i,int(nat_i_ekstra[i])]*(bud_nat_ekstra[i]-k*pris_ekstra[i])) 
        else:
            besparelse_nat_ekstra.append(0)
    
    besparelse_dag = []
    ### Evt. 0.8*mængde[i] > 0.3
    for i in range(len(pris_dag)):
        if mængde_dag[i] > 0.3 and bud_dag[i]<= FFR_mat[i,int(dag_i[i])]*7.44 and mængde_dag[i]<=FFR_amount[i,int(dag_i[i])]:
            besparelse_dag.append(mængde_dag[i]*(FFR_mat[i,int(dag_i[i])]*7.44-k*pris_dag[i])) #evt gang den fratrukkede mængde med 0.2, da det ikke er det hele der flyttes
        elif mængde_dag[i] > 0.3 and bud_dag[i]<= FFR_mat[i,int(dag_i[i])]*7.44 and mængde_dag[i]>FFR_amount[i,int(dag_i[i])]:
            besparelse_dag.append(FFR_amount[i,int(dag_i[i])]*(bud_dag[i]-k*pris_dag[i])) #evt gang den fratrukkede mængde med 0.2, da det ikke er det hele der flyttes
        else:
            besparelse_dag.append(0)
    
    indtjening_ffr_list.append(sum(besparelse_dag)+sum(besparelse_nat)+sum(besparelse_nat_ekstra))
    
    if j == 625:
        ind = np.sum([besparelse_dag,besparelse_nat,besparelse_nat_ekstra],axis=0)
        tid =pd.date_range(start='01-01-2021 00:00', periods=365,freq='24 h')
        plt.figure(figsize=(10,5))
        plt.plot(tid,ind,'o',color='blue',markersize=3)
        plt.ylabel('Daglig indtjening [DKK]')
        plt.xlabel('Dag på året')


print('Optimal budpris FFR : ',bud_ffr_list[indtjening_ffr_list.index(max(indtjening_ffr_list))])
print('Tilhørende indtjening FFR: ',max(indtjening_ffr_list))

plt.figure()
plt.plot(bud_ffr_list, indtjening_ffr_list, 'o-',color='blue')
plt.ylabel('Indtjening [DKK]')
plt.xlabel('Budpris [DKK/MW]')
plt.title('Indtjening af FFR som funktion af budpris (elbiler spotprisoptimeret)')

