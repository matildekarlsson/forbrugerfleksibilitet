# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 10:25:15 2022

@author: matil
"""
#Price kan ændres i forhold til hvilken budpris man ønsker 
price = 190


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df_varme = pd.read_csv('Varmepumpe_input_8_3_8_3_7_025.csv', sep = ',')
df_spot = pd.read_csv('Elspot_DK2.csv', sep = ',')
df_fcr = pd.read_csv('fcrreservesdk2.csv').iloc[23:8783]
df_fcr = df_fcr.set_index(np.arange(0,len(df_fcr)))
accept1 = df_fcr.FCR_N_PriceDKK.tolist()
accept1 = np.reshape(accept1,[365,24])


spot = df_spot.SpotPriceDKK
timedf = df_spot.HourDK


#laver tidslisten om med datetime
spot_2021 = []
times = pd.to_datetime(timedf)

for o in range(len(times)):     
    if times[o].year == 2021:
        spot_2021.append(df_spot.SpotPriceDKK[o])

spot1 = np.array(spot_2021[::-1])
spot = np.reshape(spot1,[365,24])

y2 = []
m2 = []

bud_priser_global = []
penge_global = []
ind_global = []

Tjek_op = []
Tjek_ned = []

hour = np.arange(0,24,1)

#minimumsbud
min_bud = 0.3

#antal varmepumper i pulje
nn = 700
# hvor mange procent af det fulde antal satser man på er til rådighed
rådighed = 0.8

#aktiveret mængde i procent 
p = 1


for b in range(365):  
    
    #mængden der bydes 
    m = [[],[],[],[]]
    #matrix med buspriserne
    bud_priser = [[],[],[],[]]
    
    #lister til at tjekke om de flytter til de samme, og derfor
    # ikke kan bydes samtidig 
    tjek_op = [[],[],[],[]]
    tjek_ned = [[],[],[],[]]
    # udgifts lister: 
    udgift_op = [[],[],[],[]]
    udgift_ned = [[],[],[],[]]

    #tager den gældende dag og regner om til MWh, her skal det ganges med 
    #mængden af varmepumper 
    x = (np.array(df_varme.iloc[b])/1000)*nn*rådighed
    max_ = max(np.max(df_varme)/1000*nn)*rådighed
    
    for c in range(0,len(x),1):
        
        # Vi kan ikke byde ind i den sidste time, da der ikke er nogle timer at tage fra eller lægge til
        if x[c] == 0 or x[c] == max_ or c == 23: 
            for h in range (0,4,1): 
                m[h].append(0)
                tjek_op[h].append(0)
                tjek_ned[h].append(0)
                bud_priser[h].append(0)
                udgift_op[h].append(10000)
                udgift_ned[h].append(10000)
                     
                
        # Nu skal der tages højde for at vi ikke flytter forbruget for langt... 
        elif (c == 0 or c == 22 or x[c-1] == 0): 
            #Tjekker hvilken mængde der er mindst og vælger denne, da man både skal 
            # kunne op og nedregulerer med samme...
            m_valg = [min(min(x[c],max_-x[c+1]),min(x[c+1],max_-x[c])),0,0,0]
            
            Spot = [[(spot[b][c+1]-spot[b][c])*p,(spot[b][c]-spot[b][c+1])*p],[0,0],[0,0],[0,0]]
            
            if x[c+1] == max_:
                op = [0,0,0,0]
                ned = [c+1,0,0,0]
            else: 
                op = [c+1,0,0,0]
                ned = [c+1,0,0,0]
            
            for k in range (0,4,1): 
                m[k].append(m_valg[k])
                tjek_op[k].append(op[k])
                tjek_ned[k].append(ned[k])
                udgift_op[k].append(Spot[k][0])
                udgift_ned[k].append(Spot[k][1])
                
                
                # Her laves bud pris listen pr MW og hvor meget indtjening så er pr MW
                if price < np.max(Spot[k]):
                    bud_priser[k].append(np.max(Spot[k]))
                    
                else: 
                    bud_priser[k].append(price)
                    
        

                
        elif x[c] != max_ and x[c] != 0 and (x[c+1] != max_ or x[c+2] != max_) and (x[c+1] != 0 or x[c+2] != 0):
            if x[c+1] ==0 and x[c+2] == max_: 
                #Tjekker hvilken mængde der er mindst og vælger denne, da man både skal 
                # kunne op og nedregulerer med samme...
                m_valg = [0,min(min(x[c],max_-x[c+1]),min(x[c+2],max_-x[c])), 0,0]
                Spot = [[0,0],[(spot[b][c+1]-spot[b][c])*p,(spot[b][c]-spot[b][c+2])*p],[0,0],[0,0]]
                op = [0,c+1,0,0]
                ned = [0,c+2,0,0]
                
                
                
            elif x[c+2] == 0 and x[c+1] == max_:
                #Tjekker hvilken mængde der er mindst og vælger denne, da man både skal 
                # kunne op og nedregulerer med samme...
                m_valg = [0,0,0,min(min(x[c],max_-x[c+2]),min(x[c+1],max_-x[c]))]
                Spot = [[0,0],[0,0],[0,0],[(spot[b][c+2]-spot[b][c])*p,(spot[b][c]-spot[b][c+1])*p]]          
                op = [0,0,0,c+2]
                ned = [0,0,0,c+1]
                
                ####-----------------NÅET HERTIL MED FLOOOOOOW 
                
            elif x[c+1] == 0:
                #Tjekker hvilken mængde der er mindst og vælger denne, da man både skal 
                # kunne op og nedregulerer med samme...
                m_valg = [0,min(min(x[c],max_-x[c+1]),min(x[c+2],max_-x[c])), min(min(x[c],max_-x[c+2]),min(x[c+2],max_-x[c])),0]
                Spot = [[0,0],[(spot[b][c+1]-spot[b][c])*p,(spot[b][c]-spot[b][c+2])*p],[(spot[b][c+2]-spot[b][c])*p,(spot[b][c]-spot[b][c+2])*p],[0,0]]
                op = [0,c+1,c+2,0]
                ned = [0,c+2,c+2,0]
                
                
            elif x[c+2] == 0: 
                #Tjekker hvilken mængde der er mindst og vælger denne, da man både skal 
                # kunne op og nedregulerer med samme...
                m_valg = [min(min(x[c],max_-x[c+1]),min(x[c+1],max_-x[c])),0,0,min(min(x[c],max_-x[c+2]),min(x[c+1],max_-x[c]))]
                Spot = [[(spot[b][c+1]-spot[b][c])*p,(spot[b][c]-spot[b][c+1])*p],[0,0],[0,0],[(spot[b][c+2]-spot[b][c])*p,(spot[b][c]-spot[b][c+1])*p]]
                op = [c+1,0,0,c+2]
                ned = [c+1,0,0,c+1]
                
            
            else: 
                # her er p den procentdel vi regner med der bliver aktiveret 
                #Tjekker hvilken mængde der er mindst og vælger denne, da man både skal 
                # kunne op og nedregulerer med samme...
                m_valg = [min(min(x[c],max_-x[c+1]),min(x[c+1],max_-x[c])),min(min(x[c],max_-x[c+1]),min(x[c+2],max_-x[c])), min(min(x[c],max_-x[c+2]),min(x[c+2],max_-x[c])),min(min(x[c],max_-x[c+2]),min(x[c+1],max_-x[c]))]
                Spot = [[(spot[b][c+1]-spot[b][c])*p,(spot[b][c]-spot[b][c+1])*p],[(spot[b][c+1]-spot[b][c])*p,(spot[b][c]-spot[b][c+2])*p],[(spot[b][c+2]-spot[b][c])*p,(spot[b][c]-spot[b][c+2])*p],[(spot[b][c+2]-spot[b][c])*p,(spot[b][c]-spot[b][c+1])*p]]
                
                
                if x[c+1] == max_:
                    op = [0,0,c+2,c+2]
                    ned = [c+1,c+2,c+2,c+1]
                if x[c+2] == max_:
                    op = [c+1,c+1,0,0]
                    ned = [c+1,c+2,c+2,c+1]
                else:     
                    op = [c+1,c+1,c+2,c+2]
                    ned = [c+1,c+2,c+2,c+1]
                    
                
            # indsætter mængden og til hvilken indtjening 
            for k in range (0,4,1): 
                m[k].append(m_valg[k])
                tjek_op[k].append(op[k])
                tjek_ned[k].append(ned[k])
                udgift_op[k].append(Spot[k][0])
                udgift_ned[k].append(Spot[k][1])
                
                if price < np.max(Spot[k]):
                    bud_priser[k].append(np.max(Spot[k]))
                else: 
                    bud_priser[k].append(price)
                    
                
            #Så nu har vi både mængderne og indtjeningerne gemt for alle mulige kombinationer 
        else: 
            for h in range (0,4,1): 
                m[h].append(0)
                tjek_op[h].append(0)
                tjek_ned[h].append(0)
                bud_priser[h].append(0)
                udgift_op[h].append(10000)
                udgift_ned[h].append(10000)

    udgift = [[],[],[],[]]
    udgiftm = [[],[],[],[]]
    #penge2 er listen hvor vi giver mulighed for at give nedreguleringen en større
    #indflydelse på udgiften, da de aktivers mere 
    penge2 = [[],[],[],[]]  
    ind = [[],[],[],[]]  
    udgift1 = [[],[],[],[]]  
    aktiv_op = 0.4
    aktiv_ned = 1-aktiv_op
    for g in range(0,4,1): 
        for s in range(0,len(x),1): 
            udgiftm[g].append(aktiv_op*udgift_op[g][s]*m[g][s]+aktiv_ned*udgift_ned[g][s]*m[g][s])
            udgift[g].append(max(udgift_op[g][s],udgift_ned[g][s]))
            if price < udgift[g][s]:
                penge2[g].append(0)
                ind[g].append(0)
            else: 
                penge2[g].append(bud_priser[g][s]*m[g][s]-udgiftm[g][s])
                ind[g].append((bud_priser[g][s]-udgift[g][s])*m[g][s])
                        
        
    
    #OPTIMERINGSMODEL 

    
    import pyomo.environ as pyo
    
    model = pyo.ConcreteModel()
    model.i = pyo.RangeSet(1,4, doc='indexiofx')
    model.j = pyo.RangeSet(1,24, doc='indexiofx')
    
    #model.y = pyo.Var(model.i, model.j, domain= pyo.NonNegativeReals, bounds=(0, 1))
    model.y = pyo.Var(model.i, model.j, within=pyo.Binary)
    

    #Definition af objektfunktion
    model.obj = pyo.Objective(expr= sum(model.y[i,j]*penge2[i-1][j-1] for i in model.i for j in model.j), sense=pyo.maximize)
    model.Con1 = pyo.Constraint(model.j, rule=lambda model, j:(model.y[1,j] + model.y[2,j] + model.y[3,j] + model.y[4,j]) <= 1)

    model.cons3 = pyo.ConstraintList()
    model.cons4 = pyo.ConstraintList()
    
    for ii in range(1,5,1):
        for jj in range(1,25,1):
            for h in range(1,5,1):
                for n in range(1,25,1):
                    if m[ii-1][jj-1] !=0:
                        #Tjekker for opregulering
                        if (tjek_op[ii-1][jj-1] == tjek_op[h-1][n-1] and (h!= ii or n!=jj)):
                            expression = x[tjek_op[h-1][n-1]]+model.y[ii,jj]*m[ii-1][jj-1]+model.y[h,n]*m[h-1][n-1] <= max_
                            model.cons3.add(expr = expression)
                        # tjekker for nedregulering     
                        if (tjek_ned[ii-1][jj-1] == tjek_ned[h-1][n-1] and (h!= ii or n!=jj)):
                            expression = x[tjek_ned[h-1][n-1]]-model.y[ii,jj]*m[ii-1][jj-1]-model.y[h,n]*m[h-1][n-1] >= 0
                            model.cons4.add(expr = expression)
                        else: 
                            #print('else inner')
                            hey = 1
     
    model.cons1 = pyo.ConstraintList()  
    
    for ii in range(1,5,1): 
        for jj in range(1,25,1):
            for h in range(1,5,1):
            #opregulering evt byde ind med mindre mængde hvis vi har flyttet eller taget noget fra den
                if m[ii-1][jj-1] != 0: 
                    expression = x[tjek_op[ii-1][jj-1]]+model.y[ii,jj]*m[ii-1][jj-1]+m[h-1][tjek_op[ii-1][jj-1]]*model.y[h,tjek_op[ii-1][jj-1]+1] <= max_
                    model.cons1.add(expr = expression)
                else: 
                    hey = 1 
                
    model.cons2 = pyo.ConstraintList()    
         
    for ii in range(1,5,1):
        for jj in range(1,25,1):
            for h in range(1,5,1):
                if m[ii-1][jj-1] != 0: 
                    #nedregulering evt byde ind med mindre mængde hvis vi har flyttet eller taget noget fra den
                    expression = x[tjek_ned[ii-1][jj-1]]- model.y[ii,jj]*m[ii-1][jj-1] - model.y[h,tjek_ned[ii-1][jj-1]+1]*m[h-1][tjek_ned[ii-1][jj-1]]  >=0
                    model.cons2.add(expr = expression)
                else: 
                    hey = 1 
    
    # sørger for at minimumsbuddet overholdes... 
    def rule4(model,i,j):
        if m[i-1][j-1] >= 0:
            return model.y[i,j]*min_bud <= m[i-1][j-1]
        else: 
            return pyo.Constraint.Skip
    
    
    model.Con3 = pyo.Constraint(model.i, model.j, rule=rule4)    
    
    # Solver
    opt = pyo.SolverFactory('glpk') 
    opt.solve(model)
    
    #model.pprint()
    #model.Con3.pprint()
    xx = [pyo.value(model.y[i,j]) for i in model.i for j in model.j]
    Objekt = pyo.value(model.obj)
    y1 = np.reshape(xx,[4,24])

    y2.append(y1)
    m2.append(m)
    penge_global.append(penge2)
    bud_priser_global.append(bud_priser)
    ind_global.append(ind)
    Tjek_op.append(tjek_op)
    Tjek_ned.append(tjek_ned)
    
    del ii
    del jj
    del h
    del n 

BUD = [[],[],[],[]]
count = 0
budd = []
Indkomst = [[],[],[],[]]
sus = []
for g in range(len(y2)):
    for h in range(0,24,1):
        for i in range(0,4,1):
            budd.append(y2[g][i][h]*m2[g][i][h])
            Indkomst[i].append(y2[g][i][h]*ind_global[g][i][h])
            BUD[i].append(y2[g][i][h]*bud_priser_global[g][i][h])
            if y2[g][i][h] > 0: 
                sus.append(y2[g][i][h]*m2[g][i][h])
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
print('Årlig indkomst (DKK): ',np.sum(Indkomst))
