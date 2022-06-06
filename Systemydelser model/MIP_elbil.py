# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 11:59:05 2022

@author: mie_h
"""

import pyomo.environ as pyo
import numpy as np

# Optimeringsmodel med sammenhængende (coherent) opladning (trekant)
def OptCoh(spot,morgen,aften,DO,kap):
    M = 10
    
    # Definition af variabel og model
    m = pyo.ConcreteModel()
    m.i = pyo.RangeSet(1,24, doc='indexiofx')
    m.y = pyo.Var(m.i, domain=pyo.NonNegativeReals)
    m.x = pyo.Var(m.i, domain=pyo.Binary)
    m.u = pyo.Var([1,2], domain=pyo.Binary)
    
    #Definition af objektfunktion
    m.obj = pyo.Objective(expr= sum((m.y[i]/1000)*spot[i-1] for i in m.i), sense=pyo.minimize)
    
    #Definition af constraints
    m.Con1 = pyo.Constraint(expr = sum(m.y[i] for i in range(1,m.i[morgen]+1)) + sum(m.y[i] for i in range(m.i[aften],25)) >= DO)
    m.Con2 = pyo.Constraint(m.i, rule=lambda m, i: m.y[i] <= kap*m.x[i])
    m.Con3 = pyo.Constraint(expr = sum(m.x[i] for i in range(1,m.i[morgen]+1)) <= M*m.u[1])
    m.Con4 = pyo.Constraint(expr = sum(m.x[i] for i in range(m.i[aften],25)) <= M*m.u[2])
    m.Con5 = pyo.Constraint(expr = m.u[1]+m.u[2] <=1)
    
    # Rule for coherent (sammenhængende) opladning 
    def cohRule(m, i):
        if i<morgen:
            return m.x[i] <= m.x[i+1]
        elif i>=aften and i < 24:
            return m.x[i] <= m.x[i+1]          
        else:
            return m.x[i] <=1 # måske return tomt eller m.x[i] == 0
    
    # Regel for at opladning skal have nedadgående effekt
    def triRule(m, i):
        if i<morgen:
            return kap*(1-m.x[i])+m.y[i]>=m.y[i+1]
        elif i>=aften and i < 24:
            return kap*(1-m.x[i])+m.y[i]>=m.y[i+1]         
        else:
            return m.y[i] <=kap # måske return tomt eller m.y[i] == 0
    
    # Constraints for sammenhængende opladning
    m.Con6 = pyo.Constraint(m.i, rule=cohRule)
    m.Con7 = pyo.Constraint(m.i, rule=triRule)
    
    # Solver
    opt = pyo.SolverFactory('mindtpy') 
    opt.solve(m, mip_solver='glpk')
    
    #Definerer løsningen som 2 arrays (y er den faktiske opladning)
    x = [pyo.value(m.x[i]) for i in m.i]
    y = [pyo.value(m.y[i]) for i in m.i]
    
    return x, np.round(y,3)

### Weekend-optimering, hvor man som input siger hvor meget der skal 
### oplades midt på dagen og hvor meget der skal oplades om natten

def OptWeekend(spot,morgen,aften,w_tilslut,w_afslut,DO,WO,kap):
    M = 10
    
    # Definition af variabel og model
    m = pyo.ConcreteModel()
    m.i = pyo.RangeSet(1,24, doc='indexiofx')
    m.y = pyo.Var(m.i, domain=pyo.NonNegativeReals)
    m.x = pyo.Var(m.i, domain=pyo.Binary)
    m.u = pyo.Var([1,2], domain=pyo.Binary)
    
    #Definition af objektfunktion
    m.obj = pyo.Objective(expr= sum((m.y[i]/1000)*spot[i-1] for i in m.i), sense=pyo.minimize)
    
    #Definition af constraints
    m.Con1 = pyo.Constraint(expr = sum(m.y[i] for i in range(1,m.i[morgen]+1)) + sum(m.y[i] for i in range(m.i[aften],25)) >= DO)
    m.Con9 = pyo.Constraint(expr = sum(m.y[i] for i in range(1,25)) <= DO+WO+1)
    m.Con8 = pyo.Constraint(expr = sum(m.y[i] for i in range(w_tilslut,w_afslut+1)) >= WO)
    m.Con2 = pyo.Constraint(m.i, rule=lambda m, i: m.y[i] <= kap*m.x[i])
    m.Con3 = pyo.Constraint(expr = sum(m.x[i] for i in range(1,m.i[morgen]+1)) <= M*m.u[1])
    m.Con4 = pyo.Constraint(expr = sum(m.x[i] for i in range(m.i[aften],25)) <= M*m.u[2])
    m.Con5 = pyo.Constraint(expr = m.u[1]+m.u[2] <=1)
    #Con5 skal ændres, hvis det skal være lovligt at oplade både morgen, middag 
    # og aften eller hvis det kun skal være lovligt at oplade på ét tidspunkt
    
    # Rule for coherent (sammenhængende) opladning 
    def cohRule(m, i):
        if i<morgen:
            return m.x[i] <= m.x[i+1]
        elif i>=w_tilslut and i <= w_afslut:
            return m.x[i] <= m.x[i+1]
        elif i>=aften and i < 24:
            return m.x[i] <= m.x[i+1]          
        else:
            return m.x[i] <=1 # måske return tomt eller m.x[i] == 0
    
    # Regel for at opladning skal have nedadgående effekt
    def triRule(m, i):
        if i<morgen:
            return kap*(1-m.x[i])+m.y[i]>=m.y[i+1]
        elif i>=w_tilslut and i <= w_afslut:
            return kap*(1-m.x[i])+m.y[i]>=m.y[i+1]
        elif i>=aften and i < 24:
            return kap*(1-m.x[i])+m.y[i]>=m.y[i+1]         
        else:
            return m.y[i] <=kap # måske return tomt eller m.y[i] == 0
    
    # Constraints for sammenhængende opladning
    m.Con6 = pyo.Constraint(m.i, rule=cohRule)
    m.Con7 = pyo.Constraint(m.i, rule=triRule)
    
    # Solver
    opt = pyo.SolverFactory('mindtpy') 
    opt.solve(m, mip_solver='glpk')
    
    #Definerer løsningen som 2 arrays (y er den faktiske opladning)
    x = [pyo.value(m.x[i]) for i in m.i]
    y = [pyo.value(m.y[i]) for i in m.i]
    
    return x, np.round(y,3), pyo.value(m.obj)

### Weekend-optimering, hvor man som input angiver hvor meget der samlet
### skal oplades i løbet af dagen - modellen må selv fordele om det skal ske
### om morgenen, middag eller aften eller både middag og enten morgen el. aften hvor meget der skal 

def OptWeekendSum(spot,morgen,aften,w_tilslut,w_afslut,DO,kap):
    M = 10
    
    # Definition af variabel og model
    m = pyo.ConcreteModel()
    m.i = pyo.RangeSet(1,24, doc='indexiofx')
    m.y = pyo.Var(m.i, domain=pyo.NonNegativeReals)
    m.x = pyo.Var(m.i, domain=pyo.Binary)
    m.u = pyo.Var([1,2], domain=pyo.Binary)
    
    #Definition af objektfunktion
    m.obj = pyo.Objective(expr= sum((m.y[i]/1000)*spot[i-1] for i in m.i), sense=pyo.minimize)
    
    #Con1 og Con8 kan erstattes af følgende, hvis det er ligemeget,
    #hvor meget der oplades midt på dagen i forhold til om natten
    m.Con0 = pyo.Constraint(expr = sum(m.y[i] for i in range(1,m.i[morgen]+1)) 
    + sum(m.y[i] for i in range(m.i[aften],25))
    + sum(m.y[i] for i in range(w_tilslut,w_afslut)) >= DO)

    
    #Definition af constraints
    #m.Con1 = pyo.Constraint(expr = sum(m.y[i] for i in range(1,m.i[morgen]+1)) + sum(m.y[i] for i in range(m.i[aften],25)) >= DO)
    #m.Con8 = pyo.Constraint(expr = sum(m.y[i] for i in range(w_tilslut,w_afslut)) >= WO)
    m.Con2 = pyo.Constraint(m.i, rule=lambda m, i: m.y[i] <= kap*m.x[i])
    m.Con3 = pyo.Constraint(expr = sum(m.x[i] for i in range(1,m.i[morgen]+1)) <= M*m.u[1])
    m.Con4 = pyo.Constraint(expr = sum(m.x[i] for i in range(m.i[aften],25)) <= M*m.u[2])
    m.Con5 = pyo.Constraint(expr = m.u[1]+m.u[2] <=1)
    #Con5 skal ændres, hvis det skal være lovligt at oplade både morgen, middag 
    # og aften eller hvis det kun skal være lovligt at oplade på ét tidspunkt
    
    # Rule for coherent (sammenhængende) opladning 
    def cohRule(m, i):
        if i<morgen:
            return m.x[i] <= m.x[i+1]
        elif i>=w_tilslut and i <= w_afslut:
            return m.x[i] <= m.x[i+1]
        elif i>=aften and i < 24:
            return m.x[i] <= m.x[i+1]          
        else:
            return m.x[i] <=1 # måske return tomt eller m.x[i] == 0
    
    # Regel for at opladning skal have nedadgående effekt
    def triRule(m, i):
        if i<morgen:
            return kap*(1-m.x[i])+m.y[i]>=m.y[i+1]
        elif i>=w_tilslut and i <= w_afslut:
            return kap*(1-m.x[i])+m.y[i]>=m.y[i+1]
        elif i>=aften and i < 24:
            return kap*(1-m.x[i])+m.y[i]>=m.y[i+1]         
        else:
            return m.y[i] <=kap # måske return tomt eller m.y[i] == 0
    
    # Constraints for sammenhængende opladning
    m.Con6 = pyo.Constraint(m.i, rule=cohRule)
    m.Con7 = pyo.Constraint(m.i, rule=triRule)
    
    # Solver
    opt = pyo.SolverFactory('mindtpy') 
    opt.solve(m, mip_solver='glpk')
    
    #Definerer løsningen som 2 arrays (y er den faktiske opladning)
    x = [pyo.value(m.x[i]) for i in m.i]
    y = [pyo.value(m.y[i]) for i in m.i]
    
    return x, np.round(y,3)


def OptVandEL(spot,elbehov,effekt,COP,morgen_start,morgen_slut,morgen_behov):
    off = min(int(elbehov/1.8)/10,1)
    # Definition af variabel og model
    m = pyo.ConcreteModel()
    m.i = pyo.RangeSet(1,24, doc='indexiofx')
    m.x = pyo.Var(m.i, domain=pyo.NonNegativeReals,bounds=(0,1))
    
    #Definition af objektfunktion
    m.obj = pyo.Objective(expr= sum(((effekt/COP)*(m.x[i])/1000)*spot[i-1] for i in m.i), sense=pyo.minimize)
    
    #Definition af constraints
    m.Con1 = pyo.Constraint(expr = sum((m.x[i])*(effekt/COP) for i in m.i) >= elbehov)
    m.Con5 = pyo.Constraint(expr = sum((m.x[i])*(effekt/COP) for i in m.i) <= elbehov+elbehov/5) #må ikke bruge for meget el fx ved negative spotpriser 
    m.Con2 = pyo.Constraint(m.i, rule=lambda m, i: m.x[i] <= 1)
    m.Con3 = pyo.Constraint(expr = sum((m.x[i])*(effekt/COP) for i in range(m.i[morgen_start],m.i[morgen_slut]+1)) >= morgen_behov)
    m.Con4 = pyo.Constraint(m.i, rule=lambda m, i: m.x[i] >= 0)
   # tilføj binær variabel y, og constraint med m.x[i]>=0.2*m.y[i] +m.x[i]<=M*m.y[i] evt uden M
   
    # Rule for max sluk på 2 timer 
    def offRule(m, i):
        if i>=3:
            return m.x[i-2]+m.x[i-1]+m.x[i] >= off*(COP/effekt)
        else:
            return m.x[i] <=1 # måske return tomt eller m.x[i] == 0
    
    # Constraint for max off på 2 timer
    m.Con6 = pyo.Constraint(m.i, rule=offRule)

    # Solver
    
    opt =  pyo.SolverFactory('glpk')  
    opt.solve(m)
    #opt = pyo.SolverFactory('mindtpy') 
    #opt.solve(m, mip_solver='glpk')
    
    #Definerer løsningen som 2 arrays (y er den faktiske opladning)
    x4 = [(pyo.value(m.x[i]))*(effekt/COP) for i in m.i]
    #x4 = [pyo.value(m.x[i]) for i in m.i]
    return np.abs(np.round(x4,10)), pyo.value(m.obj)


