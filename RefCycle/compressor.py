import CoolProp.CoolProp as CoolProp
from CoolProp import AbstractState
from CoolProp.CoolProp import PhaseSI, PropsSI, get_global_param_string
from CoolProp.HumidAirProp import HAPropsSI
from math import sin
import numpy as np
from myFuncs import *
import math
import statistics


class Compressor:


    def __init__(self, name, brand, reference, refrigerant):
        self.name = name
        self.brand = brand
        self.reference = reference
        self.refrigerant = refrigerant
    
    def massFlow(self, Ts, SH):
        Ts = Ts + 273.15
        Tin = Ts + SH
        Ps = PropsSI("P", "T", Ts, "Q", 1, self.refrigerant)
        rho = PropsSI("D", "P", Ps, "T", Tin, self.refrigerant)
        return self.volFlow() * rho

    def volFlow(self):
        n_vel = 1700
        stroke = 190
        diameter = 100
        height = 200
        Volume = ( math.pi / 4 ) * ( stroke / 1000 ) * ( diameter / 1000 )
        return Volume * n_vel / 60

    def work_per_mass(self, Ps, Pc, SH_Total, Tout):

        Ps = psiToPa(Ps)
        Pc = psiToPa(Pc)
        Tst_in = PropsSI("T", "P", Ps, "Q", 1, self.refrigerant)
        Tin = Tst_in + 20
        Tout = Tout + 273.15



        k = pow( 1 - math.log(Tin/Tout) / math.log(Ps/Pc), -1 )
        
        Cp_in = PropsSI("C", "T", Tin, "P", Ps, self.refrigerant) 
        Cp_out = PropsSI("C", "T", Tout, "P", Pc, self.refrigerant) 
        Cv_in = PropsSI("O", "T", Tin, "P", Ps, self.refrigerant) 
        Cv_out = PropsSI("O", "T", Tout, "P", Pc, self.refrigerant)
        k2 = statistics.mean([Cp_in, Cp_out]) / statistics.mean([Cv_in, Cv_out])
        k2max = Cp_out / Cv_out
        k2min = Cp_in / Cv_in
        
        h3 = PropsSI("H", "P", Ps, "T", Tin, self.refrigerant)
        s3 = PropsSI("S", "P", Ps, "T", Tin, self.refrigerant)
        h4s = PropsSI("H", "P", Pc, "S", s3, self.refrigerant)
        h4_test = PropsSI("H", "P", Pc, "T", Tout, self.refrigerant)
        n_s_test = ( h4s - h3 ) / ( h4_test - h3 )
        
        return k, k2, k2max, k2min, n_s_test, Tin
        


        '''
        Tasks
        1. Plot k for each temperature change.
        2. get value of n and compare with k
        '''
    
    


        
        