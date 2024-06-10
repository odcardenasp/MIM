from __future__ import print_function
from CoolProp import AbstractState
from CoolProp.CoolProp import PhaseSI, PropsSI, get_global_param_string
import CoolProp.CoolProp as CoolProp
from CoolProp.HumidAirProp import HAPropsSI
from math import sin
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import os
import xlwings as xw


#directory_str = ('D:/OneDrive - GreenYellow Colombia/Data/Descargas/Proyecto_MIM'
#                '/MIM_Refrigeration_290923.xlsm')

#excel_app = xw.App(visible = True)
#wb = excel_app.books.open(directory_str)
#wb = xw.Book(directory_str)
#ws = wb.sheets('Layout Actual')





#FUNCTIONS

def psiToPa(P_psi):
    result = P_psi * 6894.76 
    return result 

def PaTopsi(P_Pa):
    result = P_Pa / 6894.76 
    return result 

def barToPa(P_bar):
    result = P_bar * 100000 
    return result 

def TdPoly(Ps, Pc, Ts, n):
    Td = Ts * (Pc / Ps)**( (n - 1) / n )
    return Td

def btuToW(input):
    output = input / 3.412
    return output


Po_LT = barToPa(14.8)
Ts_LT = PropsSI("T", "P", Po_LT, "Q", 0, "R744")
print(Ts_LT-273.15)
Hs_LT_total = PropsSI("H", "P", Po_LT, "T", Ts_LT + 13, "R744")
Hs_LT_util = PropsSI("H", "P", Po_LT, "T", Ts_LT + 6, "R744")
Ss_LT = PropsSI("S", "P", Po_LT, "T", Ts_LT + 13, "R744")
print("hs_LT: ", Hs_LT_total, Hs_LT_util)


Prec = barToPa(39.7)
Trec = PropsSI("T", "P", Prec, "Q", 0, "R744")
print(Trec-273.15)
hrec_Liq = PropsSI("H", "P", Prec, "T", Trec - 0.7, "R744")
print("hrec: ", hrec_Liq)

Pc_LT = barToPa(29.6)
#Tc = PropsSI("T", "P", Pc, "Q", 1, "R744")
Sc_LT = Ss_LT 
n_s = 0.7
hc_s_LT = PropsSI("H", "P",Pc_LT, "S", Sc_LT, "R744")
hc_LT  = Hs_LT_total + ( 1 / n_s ) * ( hc_s_LT - Hs_LT_total )
Td_LT = PropsSI("T", "P", Pc_LT, "H", hc_LT, "R744")
print("hc_LT: ", hc_LT, "Td_LT: ", Td_LT-273.15)

COP = ( Hs_LT_util - hrec_Liq) / ( hc_LT - Hs_LT_total ) 
print("COP: ", COP)

m_evap_LT = 2619 / 3600
Cooling_Cap_LT = (Hs_LT_util - hrec_Liq) * m_evap_LT / 1000
print("LT_Capacity:", Cooling_Cap_LT, "kW")

Power_LT = ( hc_LT - Hs_LT_total ) * m_evap_LT / 1000
print("LT_Power:", Power_LT, "kW")


Po_MT = barToPa(29.6)
Ts_MT = PropsSI("T", "P", Po_MT, "Q", 1, "R744")
print(Ts_MT-273.15)
Hs_MT_total = PropsSI("H", "P", Po_MT, "T", Ts_MT + 15, "R744")
Hs_MT_util = PropsSI("H", "P", Po_MT, "T", Ts_MT + 6, "R744")
Ss_MT = PropsSI("S", "P", Po_MT, "T", Ts_MT + 13, "R744")
print("hs_MT: ", Hs_LT_total, Hs_LT_util)

Pc_MT = barToPa(62.9)
#Tc = PropsSI("T", "P", Pc, "Q", 1, "R744")
Sc_MT = Ss_MT 
n_s = 0.64
hc_s_MT = PropsSI("H", "P",Pc_MT, "S", Sc_MT, "R744")
hc_MT  = Hs_MT_total + ( 1 / n_s ) * ( hc_s_MT - Hs_MT_total )
Td_MT = PropsSI("T", "P", Pc_MT, "H", hc_MT, "R744")
print("hc_MT: ", hc_MT, "Td_MT: ", Td_MT-273.15)

m_evap_MT = (7184 / 3600) - m_evap_LT
m_comp_MT = m_evap_LT + m_evap_MT
Cooling_Cap_MT = (Hs_MT_util - hrec_Liq) * m_evap_MT / 1000
print("MT_Capacity:", Cooling_Cap_MT, "kW")

Power_MT = ( hc_MT - Hs_MT_total ) * m_comp_MT / 1000
print("MT_Power:", Power_MT, "kW")


Pgc = barToPa(62.9)
Tgc = PropsSI("T", "P", Pgc, "Q", 0, "R744")
print(Trec-273.15)
hgc = PropsSI("H", "P", Pgc, "T", Tgc - 5.8, "R744")
print("hgc: ", hgc)

Quality = PropsSI("Q", "P", Prec, "H", hgc, "R744")
hrec_mix = hgc
print("Quality", Quality)
Ts_IT = PropsSI("T", "P", Prec, "Q", 1, "R744")
h_It_util = PropsSI("H", "P", Prec, "T", Ts_IT + 0.1, "R744") 
h_It_total = PropsSI("H", "P", Prec, "T", Ts_IT + 14, "R744") 
h_It = PropsSI("H", "P", Prec, "Q", 1 , "R744")
Ss_IT = PropsSI("S", "P", Prec, "T", Ts_IT + 14,  "R744")
print("h_IT: ", h_It, "Ss_IT", Ss_IT)
print("h_IT_total: ", h_It_total, "h_IT_util: ", h_It_util)

Sc_IT = Ss_IT 
n_s_It = 0.64
hc_s_IT = PropsSI("H", "P", Pgc, "S", Sc_IT, "R744")
hc_IT  = h_It_total + ( 1 / n_s_It ) * ( hc_s_IT - h_It_total )
Td_IT = PropsSI("T", "P", Pgc, "H", hc_IT, "R744")
print("hc_s_IT: ", hc_s_IT, "hc_IT", hc_IT )
print("Td_IT: ", Td_IT - 273.15) 
m_comp_IT = 5686 / 3600
m_evap_AC = m_comp_IT - m_comp_MT * Quality
Cooling_Cap_AC = (h_It_util - hrec_mix) * m_evap_AC / 1000
print("AC_Capacity:", Cooling_Cap_AC, "kW")
print("m_evap_AC:", m_evap_AC)
Power_IT = ( hc_IT - h_It_total ) * m_comp_IT / 1000
print("IT_Power:", Power_IT, "kW")

m_gc = m_comp_MT + m_comp_IT
Tgc_in = ( m_comp_MT * Td_MT + m_comp_IT * Td_IT ) / m_gc
print("m_gc", m_gc*3600, "T_gc_in", Tgc_in - 273.15)
h_gc_in = PropsSI("H", "P", Pgc, "T", Tgc_in, "R744")
h_gc_out = PropsSI("H", "P", Pgc, "T", Tgc - 2, "R744")
GC_capacity = ( h_gc_in - h_gc_out) * m_gc / 1000 
print("gc_Capacity:", GC_capacity, "kW")





#refrigerant = "R22"
#k = 1.35
#Ts = -5 + 273.15
#Tc = 40 + 273.15



   