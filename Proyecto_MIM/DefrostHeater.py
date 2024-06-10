from __future__ import print_function
from CoolProp import AbstractState
from CoolProp.CoolProp import PhaseSI, PropsSI, get_global_param_string
import CoolProp.CoolProp as CoolProp
from CoolProp.HumidAirProp import HAPropsSI
from math import sin
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib as mpl
import matplotlib.pyplot as plt
import os
import math

step_sec = 2
#ts = np.arange(0, 3600, step_sec)
#T = np.arange(0, 3600, step_sec)
hconv = 0.08                           #kW/m2-K 
mo = 0.1509                               # control volume mass in (kg)
To = 273.15 - 2
l_tb = 2.24
n_tb = 40 
D_tb = 9.525 * 10 ** (-3)               # number of tubes (und)
As = math.pi * D_tb * l_tb * n_tb                  #Surface Area of tube (m2)  
Qh = 1.8                               #Heat flux in heater (kW) 
Cp_air = 1.005                           #Cp in air (kJ/(kg-K))
Cp_water = 4.186       #kJ/kg-K
rho_ice = 1000          #density in (kg/m3) 
h_sf = 333.43                            #Enthalpy from fusion (kJ/kg)
T_water = 273.15 + 8
T_ice = 273.15 -5  
T_prom = (T_water + T_ice) / 2
ts0 = 2 * 10 ** (-3)    # Ice thickness in m at 0s
#T[0] = 273.15 - 2   # Air temperature at 0s





def odeEuler(f,t,y0):
    y = np.zeros(len(t))
    y[0] = y0
    for n in range(0,len(t)-1):
        y[n+1] = y[n] + f(t[n],y[n])*(t[n+1] - t[n])
    return y

def odeEulerMod(f,t,T,y0):
    y = np.zeros(len(t))
    y[0] = y0
    for n in range(0,len(t)-1):
        y[n+1] = y[n] + f(t[n],y[n],T[n])*(t[n+1] - t[n])
    return y

f = lambda t,T: (Qh - (hconv * As * (T - T_prom))) * ( T / (mo * To * Cp_air) )
t0 = 0; tf = 2000; h = 0.1; N = int((tf - t0)/h);
t = np.linspace(t0,tf,N+1); T0 = To;
Tvec = odeEuler(f,t,T0)

g = lambda t,ts, T: - (hconv * (T - T_prom)) / (rho_ice * (h_sf + Cp_water * (T_water - T_ice)) )
z = odeEulerMod(g,t,Tvec,ts0)

fig = plt.figure()
plt.plot(t,Tvec,'b.-'), plt.grid(True)

fig2 = plt.figure()
plt.plot(t,z,'r.-'), plt.grid(True)
plt.show()

print(T_prom + Qh / (hconv * As ) )