# -*- coding: utf-8 -*-
"""
Created on Mon May  9 15:31:29 2022

@author: matil
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


df_spot = pd.read_csv('Elspot_DK2.csv', sep = ',')
df_spotopt_nat = pd.read_csv('spot_opt_nat.csv', sep = ',',header=None)
df_spotopt_dag = pd.read_csv('spot_opt_dag.csv', sep = ',', header=None)
df_spotopt_ekstra = pd.read_csv('spot_opt_ekstra.csv', sep = ',', header=None)



df_fcr = pd.read_csv('fcrreservesdk2.csv').iloc[23:8783] 
df_fcr = df_fcr.set_index(np.arange(0,len(df_fcr)))
accept1 = df_fcr.FCR_N_PriceDKK.tolist()
accept1 = np.reshape(accept1,[365,24])

spot = df_spot.SpotPriceDKK
timedf = df_spot.HourDK

#laver tidslisten om med datetime
spot_2021 = []
times = pd.to_datetime(timedf)
time = []

for o in range(len(times)):     
    if times[o].year == 2021:
        spot_2021.append(df_spot.SpotPriceDKK[o])
        time.append( pd.to_datetime(times[o]))
        
time = np.array(time[::-1])
spot1 = np.array(spot_2021[::-1])
spot = np.reshape(spot1,[365,24])

#df_elbil = pd.read_csv('el.csv', sep = ',')
#Laver frakoblings tider til spotoptimeret csv.

nat_y = []
dag_y = []
dag_fra = []
nat_fra = []
nat_y_ekstra = []
amount_dag = []
amount_nat = []
amount_ekstra = []
amount_nat1 = []
amount_ekstra1 = []

time_ = np.reshape(time,[365,24])


for kk in range(365):
    if time_[kk,0].dayofweek == 4:
        dag = [0,0,0,0,0,0,0,0,0,0,0,5,5,0,0,0,0,0,0,0,0,0,0,0]
        fra_d = [0,0,0,0,0,0,0,0,0,12,12,12,12,0,0,0,0,0,0,0,0,0,0,0]
        fra_n = [5,5,5,5,5,5,0,0,0,0,0,0,0,0,0,23,23,23,23,23,23,23,23,23]
        ekstra = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        dag_m = [0,0,0,0,0,0,0,0,0,60,60,60,60,0,0,0,0,0,0,0,0,0,0,0]
        ekstra_m = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        nat_m = [240,240,240,240,240,240,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        ekstra_m1 = [50,50,50,50,50,50,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        nat_m1 = [190,190,190,190,190,190,0,0,0,0,0,0,0,0,0,190,190,190,190,190,190,190,190,190]
        
    elif time_[kk,0].dayofweek == 5:
        dag = [0,0,0,0,0,0,0,0,0,0,0,10/3,10/3,10/3,0,0,0,0,0,0,0,0,0,0]
        fra_d = [0,0,0,0,0,0,0,0,14,14,14,14,14,14,14,0,0,0,0,0,0,0,0,0]
        fra_n = [5,5,5,5,5,5,0,0,0,0,0,0,0,0,0,0,0,0,0,23,23,23,23,23]
        ekstra = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        ekstra_m = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        dag_m = [0,0,0,0,0,0,0,0,90,90,90,90,90,90,90,0,0,0,0,0,0,0,0,0]
        nat_m = [210,210,210,210,210,210,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        ekstra_m1 = [15,15,15,15,15,15,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        nat_m1 = [195,195,195,195,195,195,0,0,0,0,0,0,0,0,0,0,0,0,0,195,195,195,195,195]

    elif time_[kk,0].dayofweek == 6:
        dag = [0,0,0,0,0,0,0,0,0,0,0,5,5,0,0,0,0,0,0,0,0,0,0,0]
        fra_d = [0,0,0,0,0,0,0,12,12,12,12,12,12,0,0,0,0,0,0,0,0,0,0,0]
        fra_n = [5,5,5,5,5,5,0,0,0,0,0,0,0,0,0,23,23,23,23,23,23,23,23,23]
        ekstra = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,10/3,10/3,10/3]
        ekstra_m = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,30,30,30]
        dag_m = [0,0,0,0,0,0,0,90,90,90,90,90,90,0,0,0,0,0,0,0,0,0,0,0]
        nat_m = [180,180,180,180,180,180,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        ekstra_m1 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,30,30,30]
        nat_m1 = [180,180,180,180,180,180,0,0,0,0,0,0,0,0,0,180,180,180,180,180,180,180,180,180]

    else:
      
        dag = [0,0,0,0,0,0,0,0,0,0,0,10/3,10/3,10/3,0,0,0,0,0,0,0,0,0,0] 
        fra_d = [0,0,0,0,0,0,0,0,0,14,14,14,14,14,14,0,0,0,0,0,0,0,0,0]
        fra_n = [5,5,5,5,5,5,0,0,0,0,0,0,0,0,0,0,0,0,0,23,23,23,23,23]
        ekstra = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        ekstra_m = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        dag_m = [0,0,0,0,0,0,0,0,0,60,60,60,60,60,60,0,0,0,0,0,0,0,0,0]
        nat_m = [240,240,240,240,240,240,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        ekstra_m1 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]        
        nat_m1 = [240,240,240,240,240,240,0,0,0,0,0,0,0,0,0,0,0,0,0,240,240,240,240,240]
        
    nat_y.append([2.5,2.5,2.5,2.5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
    dag_y.append(dag)
    nat_y_ekstra.append(ekstra)
    dag_fra.append(fra_d)
    nat_fra.append(fra_n)
    amount_dag.append(dag_m)
    amount_nat.append(nat_m)
    amount_ekstra.append(ekstra_m)
    amount_nat1.append(nat_m1)
    amount_ekstra1.append(ekstra_m1)


list_ind = []

for price in np.arange(100,370,10):
    

    #Alle de globale lister defineres
    bud_priser_global = []
    penge_global = []
    ind_global = []
    BUD = []
    y_global = []
    m_global = []
    
    
    #minimumsbud
    min_bud = 0.3
    
    r??dighed = 0.8
    
    
    #aktiveret m??ngde i procent 
    p = 1
    
    ###---------------------------??RS L??KKEN -----------#####
    
    for b in range(365): 
        print('N??et til dag', b+1)
        
        #m??ngden der bydes 
        m = [[],[],[],[]]
            
        #Udgiftslisterne som der minimeres over 
        udgift_op = [[],[],[],[]]
        udgift_ned = [[],[],[],[]]
        udgift = [[],[],[],[]]
        udgiftm = [[],[],[],[]]
        udgift_opm = [[],[],[],[]]
        udgift_nedm = [[],[],[],[]]
        
        #Den andel vi tror der bliver aktiveret af op og ned
        aktiv_ned = 0.6
        aktiv_op = 1-aktiv_ned
        
        
        # evt ogs?? lave op og ned her...  
        bud_priser = [[],[],[],[]]
        penge = [[],[],[],[]]
        ind = [[],[],[],[]]
            
        #lister til at tjekke om de flytter til de samme, og derfor
        # ikke kan bydes samtidig 
        tjek = [[],[],[],[]]
        #tager den g??ldende dag og regner om til MWh, her skal det ganges med  
        x = (np.array(dag_y[b])/1000)*np.array(amount_dag[b])*r??dighed
        fra = (np.array(dag_fra[b]))
        
        MM=100000
        # Her er c den time vi kigger p?? og k er timerne efter indtil frakobling    
        for c in range(0,len(x),1): 
            for k in range(0,4,1):
             
                #Herefter laves alle de andre matricer 
                # En for m??ngde, en for udgift op og en for udgift ned
                # i de f??ste statements tages der h??jde for at man ikke kan 
                # kigge s?? langt frem i de sidste par timer. 
                if c+k+1 >= len(x):
                    m[k].append(0)
                    udgift_op[k].append(MM)
                    udgift_ned[k].append(MM)
                    udgift_opm[k].append(MM)
                    udgift_nedm[k].append(MM)
                     #Laver tjek liste, her er det kun nedregulering
                     # har bare v??rdier p?? alle pladser, da man alligevel ikke 
                     # kommer til at bruge dem hvor m = 0 
                    tjek[k].append(0)
                    
                    
                # her s??rger der for at man kun arbejder med timer med forbrug i,
                #som ikke er timen lige f??r frakobling 
                elif x[c]!=0 and k+c < fra[c] and fra[c] != 0 and x[c+k+1]!=0:
    
                    find_min = []
                    for l in range(1,fra[c]+1-c,1):
                        find_min.append(spot[b][c+l]-spot[b][c])
                    ud = min(find_min)
                
                    if x[k+1+c] <= x[c]:
                        m[k].append(x[k+1+c])
                        udgift_op[k].append(ud*p)
                        udgift_ned[k].append((spot[b][c]-spot[b][c+k+1])*p)
                        udgift_opm[k].append(ud*x[k+1+c]*p)
                        udgift_nedm[k].append(x[k+1+c]*(spot[b][c]-spot[b][c+k+1])*p)
                        tjek[k].append(1+c+k)
                        
                    elif x[c] < x[k+1+c]:
                        m[k].append(x[c])
                        udgift_op[k].append(ud*p)
                        udgift_ned[k].append((spot[b][c]-spot[b][c+k+1])*p)
                        udgift_opm[k].append(ud*x[c]*p)
                        udgift_nedm[k].append(x[c]*(spot[b][c]-spot[b][c+k+1])*p)
                        tjek[k].append(1+c+k)
                else: 
                    m[k].append(0)
                    udgift_op[k].append(MM)
                    udgift_ned[k].append(MM)
                    udgift_opm[k].append(MM)
                    udgift_nedm[k].append(MM)
                    tjek[k].append(0)
                    
            
        #Laver en udgifts matrix som best??r af en v??gtet sum af op og ned, da der oftes 
        # nedregulers mere. 
        udgift = [[],[],[],[]]
        for g in range(0,4,1): 
            for s in range(0,len(x),1): 
                udgiftm[g].append(aktiv_op*udgift_opm[g][s]+aktiv_ned*udgift_nedm[g][s])
                udgift[g].append(aktiv_op*udgift_op[g][s]+aktiv_ned*udgift_ned[g][s])
                if price < udgift[g][s]:
                    penge[g].append(0)
                    bud_priser[g].append(udgift[g][s])
                    ind[g].append(0)
                else: 
                    penge[g].append(price*m[g][s]-udgiftm[g][s])
                    bud_priser[g].append(price)
                    ind[g].append(price*m[g][s]-max([udgift_opm[g][s],udgift_nedm[g][s]]))
                    
        
        # OPTIMERINGSMODELLEN
        
        import pyomo.environ as pyo
            
        model = pyo.ConcreteModel()
        model.i = pyo.RangeSet(1,4, doc='indexiofx')
        model.j = pyo.RangeSet(1,24, doc='indexiofx')
            
        #model.y = pyo.Var(model.i, model.j, domain= pyo.NonNegativeReals, bounds=(0, 1))
        model.y = pyo.Var(model.i, model.j, within=pyo.Binary)
        
    
        #Definition af objektfunktion
        model.obj = pyo.Objective(expr= sum(model.y[i,j]*penge[i-1][j-1] for i in model.i for j in model.j), sense=pyo.maximize)
        model.Con1 = pyo.Constraint(model.j, rule=lambda model, j:(model.y[1,j] + model.y[2,j] + model.y[3,j] + model.y[4,j]) <= 1)
        
        model.cons1 = pyo.ConstraintList()
        
        for ii in range(1,5,1):
            for jj in range(1,25,1): 
                for h in range(1,5,1):
                    for n in range (1,25,1):
                        if m[ii-1][jj-1] !=0:
                            if (tjek[ii-1][jj-1] == tjek[h-1][n-1] and (h!= ii or n!=jj)):
                                expression = x[tjek[h-1][n-1]]-model.y[ii,jj]*m[ii-1][jj-1]-model.y[h,n]*m[h-1][n-1] >= 0
                                model.cons1.add(expr = expression)
                            else: 
                                #print('else inner')
                                hey = 1
                                
        model.cons2 = pyo.ConstraintList()    
        
        for ii in range(1,5,1):
            for jj in range(1,25,1):        
                for h in range(1,5,1):
                    if m[ii-1][jj-1] != 0: 
                        #nedregulering evt byde ind med mindre m??ngde hvis vi har flyttet eller taget noget fra den
                        expression = x[tjek[ii-1][jj-1]] - model.y[h,tjek[ii-1][jj-1]+1]*m[h-1][tjek[ii-1][jj-1]] - model.y[ii,jj]*m[ii-1][jj-1] >= 0
                        model.cons2.add(expr = expression)
                    else: 
                        hey = 2 
          
     
            # s??rger for at minimumsbuddet overholdes... 
        def rule4(model,i,j):
            if m[i-1][j-1] >= 0:
                return model.y[i,j]*min_bud <= m[i-1][j-1]
            else: 
                return pyo.Constraint.Skip
                
        
        
        model.Con2 = pyo.Constraint(model.i, model.j, rule=rule4)    
            
        # Solver
        opt = pyo.SolverFactory('glpk') 
        opt.solve(model)
            
        #model.pprint()
        #model.cons2.pprint()
        xx = [pyo.value(model.y[i,j]) for i in model.i for j in model.j]
        Objekt = pyo.value(model.obj)
        y1 = np.reshape(xx,[4,24])
        
        y_global.append(y1)
        m_global.append(m)
        penge_global.append(penge)
        bud_priser_global.append(bud_priser)
        ind_global.append(ind)
        #print('y1: ', np.sum(y1))
        #print('y global: ', np.sum(y_global))
    
      
        del ii
        del jj
        del h 
        del n  
    
    
    
    #####----------------------STOP ??RS L??KKEN -----------------------------################
    
          
            
    
    BUD = [[],[],[],[]]
    count = 0
    budd = []
    Indkomst = [[],[],[],[]]
    sus = []
    for g in range(len(y_global)):
        for h in range(0,24,1):
            for i in range(0,4,1):
                budd.append(y_global[g][i][h]*m_global[g][i][h])
                Indkomst[i].append(y_global[g][i][h]*ind_global[g][i][h])
                BUD[i].append(y_global[g][i][h]*bud_priser_global[g][i][h])
                if y_global[g][i][h] > 0: 
                    sus.append(y_global[g][i][h]*m_global[g][i][h])
                    count = count+1
    
    min_i = [] 
    # Finder ud af hvilke bud som rent faktisk er accepteret: 
    for hh in range(0,4,1):
        for j in range(0,365,1):
            for i in range(0,24,1):  
                    if accept1[j][i] < BUD[hh][i+j*24]:
                        print('Bud ikke accepteret: ', j,i)
                        min_i.append(BUD[hh][i+j*24])
                        BUD[hh][i+j*24] = 0
                        Indkomst[hh][i+j*24] = 0
                        count = count -1 
              
    print('Ikke accepterede bud: ',min_i)
    print('Der er accepteret: ', count, 'bud')
    print('??rlig indkomst (DKK): ',np.sum(Indkomst))
    
    list_ind.append(np.sum(Indkomst))


#Plotter de forskellige indtjeninger med forskellige valgte faste budpriser
list_prisl = list(np.arange(100,370,10))

plt.figure()
plt.plot(list_prisl,list_ind,'o-',color='blue')
plt.xlabel('Bud pris (DKK)')
plt.ylabel('??rlig indtjening (DKK)')
plt.xlim(100,360)
plt.grid()



