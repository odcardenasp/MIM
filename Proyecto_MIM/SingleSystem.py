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



#FUNCTIONS

def psiToPa(P_psi):
    result = P_psi * 6894.76 
    return result 

def PaTopsi(P_Pa):
    result = P_Pa / 6894.76 
    return result 

def TdPoly(Ps, Pc, Ts, n):
    Td = Ts * (Pc / Ps)**( (n - 1) / n )
    return Td

def btuToW(input):
    output = input / 3.412
    return output


def carnot_cycle(refrigerant, Ts_C, Tc_C, SH_total, SC, Td):

    #refrigerant = "R22"
    k = 1.35
    #Ts = -5 + 273.15
    #Tc = 40 + 273.15

    Ts = Ts_C + 273.15
    Tc = Tc_C + 273.15
    el_eff = 1

    Ps = PropsSI("P", "T", Ts, "Q", 1, refrigerant)
    Pc = PropsSI("P", "T", Tc, "Q", 1, refrigerant)
    #print('Ps: ', PaTopsi(Ps), 'Pc: ', PaTopsi(Pc) )

    #STATE 1
    #SH_total = 15
    SH_util = 5.6
    SC = SC + 0.01
    n_s = 0.717

    T3g = PropsSI("T", "P", Ps, "Q", 1, refrigerant)
    h3 = PropsSI("H", "P", Ps, "T", T3g + SH_total, refrigerant)
    s3 = PropsSI("S", "P", Ps, "T", T3g + SH_total, refrigerant)
    print('T3g: ',T3g + SH_total, 'h3: ', h3, 'Ps: ', Ps)

    h2 = PropsSI("H", "P", Ps, "T", T3g + SH_util, refrigerant)
    print('T2g: ',T3g + SH_util, 'h2: ', h2, 'Ps: ', Ps, 's3: ', s3)

    h4s = PropsSI("H", "P", Pc, "S", s3, refrigerant)
    h4 = h3 + ( 1 / n_s ) * ( h4s - h3 )
    T4 = PropsSI("T", "P", Pc, "H", h4, refrigerant)
    print('T4: ',T4 , 'h4: ', h4, 'Pc: ', Pc)

    h5 = h4
    T6g = PropsSI("T", "P", Pc, "Q", 0, refrigerant)
    h6 = PropsSI("H", "P", Pc, "T", T6g - SC, refrigerant)
    print('T6: ',T6g - SC, 'h6: ', h6, 'Pc: ', Pc)

    h7 = h6
    h8 = h7
    Q8 = PropsSI("Q", "P", Ps, "H", h8, refrigerant)
    print('Q8: ',Q8, 'h8: ', h8, 'Ps: ', Ps)

    h1 = h8

    COPev_th_num = h2 - h1
    COPcomp_th_num = h3 - h1
    COP_th_den = h4 - h3

    print('evp_h_num : ', COPev_th_num, 'comp_h_num: ', COPcomp_th_num, 'comp_h_den', COP_th_den)
    COPcomp = COPcomp_th_num / COP_th_den
    COPev = COPev_th_num / COP_th_den
    print('COPev: ', COPev, 'COPcomp: ', COPcomp)


    #T4_test = TdPoly(Ps, Pc, T3g + SH_total, 1.25)
    T4_test = Td + 273.15 

    print('T4: ',T4, 'Ttest: ', T4_test )
    S4_test = PropsSI("S", "P", Pc, "T", T4_test, refrigerant)
    h4_test = PropsSI("H", "P", Pc, "T", T4_test, refrigerant)
    h5_test = h4_test
    n_s_test = ( h4s - h3 ) / ( h4_test - h3 )

    COP_test_den = h4_test - h3

    print('comp_test_den', COP_test_den)
    COPcomp_test = (COPcomp_th_num / COP_test_den)*el_eff
    COPev_test = COPev_th_num / COP_test_den
    print('COPev_test: ', COPev_test, 'COPcomp_test: ', COPcomp_test)
    print('ns_test: ', n_s_test)
    
    return COPcomp_test


COPs_MT = carnot_cycle("R507A", -8, 40, 35, 0, 82)

