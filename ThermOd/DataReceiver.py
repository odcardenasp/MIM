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
    dict = {}
    fields = []


    def __read_cast(self, prompt, output_type, format = None):

        while True:
            try:
                    data = input(prompt)
                    if output_type == datetime:
                        value_list = [datetime.strptime(time_str.strip(), format) for time_str in data.split(',')]
                    else:
                        value_list = [output_type(item.strip()) for item in data.split(',')]
                    break
            
            except (AttributeError, ValueError):
                    print(f"Sorry, The date type is wrong, It can't be cast to {output_type} type.")
            
        return value_list
    

    def add_field(self, name, output_type, format = None):
        self.dict[name] = self.__read_cast(self, output_type, format)
        self.num_fields += 1
        return self.dict
    
    def del_field(self, name):
        try:
            del self.dict[name]
            self.num_fields -= 1
        except IndexError:
             print(f'Field {name} does not exist')
    
        return self.dict


def get_df_byblock(dic, time_step = None):

    epoch_start = datetime(1900, 1, 1)
    time_step = 15 if time_step == None else None  #tiempo intervalos de 15 min
    len_data = int(24 * 60 / time_step)
    hours_list = [ epoch_start + timedelta(minutes = int( x * time_step) ) for x in range(len_data) ]



def nearest(items, pivot):
    return min(items, key = lambda x: abs(x - pivot))

def get_hourly_data(time_arr, values_arr):
    epoch_start = datetime(1900, 1, 1)
    time_step = 15   #tiempo intervalos de 15 min
    len_data = int(24 * 60 / time_step)
    hours_list = [ epoch_start + timedelta(minutes = int( x * time_step) ) for x in range(len_data) ]
    values_list = [0] * len_data
    index_list = [0] * len_data

    for idx,(val,time_val) in enumerate(zip(values_arr, time_arr)):
        
        nearest_hour = nearest(hours_list,time_val)
        index = hours_list.index(nearest_hour)
        index_list[idx] = index

        for i in ( range(index,len_data) ):
            values_list[i] = val
        for i in range(0, index_list[0]):
            values_list[i] = val
        
    output_dict = {'hours': hours_list, 'values': values_list}

    return output_dict, index_list



class FormatError(Exception):
    pass

class nElementsError(Exception):
    pass


""" test1 = DataReceiver()
n = int(input("Por favor ingrese el número de intervalos \n"))
print("Ingrese la hora de inicio de cada bloque en horario militar \n"
        "con el siguiente formato: hh:mm,hh:mm")
time_values = test1.read_cast(datetime, "%H:%M")
print("Ingrese el valor de cada bloque \n"
"con el siguiente formato: v1,v2")
values = test1.read_cast(float)
print("terminado") """

list = [1,2,3]
print(list[2])

