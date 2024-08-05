#from __future__ import print_function
#from CoolProp import AbstractState
#from CoolProp.CoolProp import PhaseSI, PropsSI, get_global_param_string
#import CoolProp.CoolProp as CoolProp
#from CoolProp.HumidAirProp import HAPropsSI
#from math import sin
import numpy as np
import pandas as pd
#import matplotlib as mpl
#import matplotlib.pyplot as plt
import os
#import xlwings as xw
import datetime
from datetime import datetime, timedelta, time
import tkinter as tk
from tkinter import *
from tkinter import filedialog as fd
import csv


class DataReceiver:

    filetype = "None"
    num_fields = 0
    num_records = 0
    multiple_files = False
    df = None
    dict_input = {}
    dict_output = {}
    fields = []

    #Cast all fields in array to selected output type, format is optional
    #if output_type is a datetime. 
    def __read_cast(self, data, output_type, format = None):

        while True:
            try:
                    if output_type == datetime:
                        value_list = [datetime.strptime(time_str.strip(), format) for time_str in data.split(',')]
                    else:
                        value_list = [output_type(item.strip()) for item in data.split(',')]
                    break
            
            except (AttributeError, ValueError):
                    print(f"Sorry, The date type is wrong, It can't be cast to {output_type} type.")
                    return None
            
        return value_list
    
    def Sort_profile(self, data, index = None):
        if index != None:
            output = sorted(data, key = lambda x: x[index])
        else :
            output = sorted(data, key = lambda x: x[0])
        return output



    #Add a pair of time and variable to define 24h profile, the output is a Dictionary
    #whose key is the name of variable, for example: suc_pressure
    def add_field(self, time, value, name, output_type):

        self.fields.append( self.__read_cast(time, datetime, '%H:%M') )
        self.fields.append( self.__read_cast(value, output_type, format) )
        zipped = list(zip(self.fields[0], self.fields[1]))
        self.fields[0], self.fields[1] = zip(*self.Sort_profile(zipped, index = 0))
        self.dict_input[name] = self.fields
        self.fields = []
        self.num_fields += 1
        return self.dict_input
    
    #Delete a pair of time and variable array, whose key is the name of variable
    def del_field(self, name):

        try:
            del self.dict_input[name]
            self.num_fields -= 1
        except IndexError:
             print(f'Field {name} does not exist')
    
        return self.dict_input


    def df_from_intervals(self, time_step = None):
        
        if not self.dict_input:
            print("Error: dict_input is empty. Cannot proceed.")
            return None  # or raise an exception, depending on your error handling strategy

        epoch_start = datetime(1900, 1, 1)
        time_step = 15 if time_step == None else time_step  #tiempo intervalos de 15 min
        len_data = int(24 * 60 / time_step)
        hours_list = [ epoch_start + timedelta(minutes = int( x * time_step) ) for x in range(len_data) ]
        self.dict_output['time'] = hours_list

        for key, value in self.dict_input.items():

            values_list = [0] * len_data
            index_list = [0] * len_data
            
            for idx, (time, val) in enumerate( zip(value[0], value[1]) ):
                
                nearest_hour = self.__nearest(hours_list,time)
                index = hours_list.index(nearest_hour)
                index_list[idx] = index

                for i in ( range(index,len_data) ):
                    values_list[i] = val
                for i in range(0, index_list[0]):
                    values_list[i] = val
            
            self.dict_output[key] = values_list
            self.dict_input[key].append(index_list)
        
        self.df = pd.DataFrame(self.dict_output)

        return self.df 

    #get the nearest value from array to a pivot value 
    def __nearest(self, items, pivot):
        return min(items, key = lambda x: abs(x - pivot))



class FormatError(Exception):
    pass

class nElementsError(Exception):
    pass


test1 = DataReceiver()

n = int(input("Por favor ingrese el número de intervalos \n"))
print("Ingrese la hora de inicio de cada bloque en horario militar \n"
        "con el siguiente formato: hh:mm,hh:mm")
time_values = input()
print("Ingrese el valor de cada bloque \n"
"con el siguiente formato: v1,v2")
values = input()
print("terminado") 
test1.add_field(time_values, values, "Psuc", float)

"""
n = int(input("Por favor ingrese el número de intervalos \n"))
print("Ingrese la hora de inicio de cada bloque en horario militar \n"
        "con el siguiente formato: hh:mm,hh:mm")
time_values = input()
print("Ingrese el valor de cada bloque \n"
"con el siguiente formato: v1,v2")
values = input()
print("terminado") 
test1.add_field(time_values, values, "Pcond", float)


n = int(input("Por favor ingrese el número de intervalos \n"))
print("Ingrese la hora de inicio de cada bloque en horario militar \n"
        "con el siguiente formato: hh:mm,hh:mm")
time_values = input()
print("Ingrese el valor de cada bloque \n"
"con el siguiente formato: v1,v2")
values = input()
print("terminado") 
test1.add_field(time_values, values, "Temp", int)
"""

test1.df_from_intervals()
print(test1.df.head(40))

