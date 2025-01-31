from __future__ import print_function
from CoolProp import AbstractState
from CoolProp.CoolProp import PhaseSI, PropsSI, get_global_param_string
import CoolProp.CoolProp as CoolProp
from CoolProp.HumidAirProp import HAPropsSI
from math import sin
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import os
import xlwings as xw
import datetime
from datetime import datetime, timedelta, time
import tkinter as tk
from tkinter import *
from tkinter import filedialog as fd
import csv



###########################################################################################################################
######################  BLOCK HOURS INPUT DATA FUNCTIONS   #############################################################

class FormatError(Exception):
    pass

class nElementsError(Exception):
    pass

def input_validation( prompt, datatype, out_type = None, n_elements = None, date_format = None):
    while True:
        try:

            if out_type == list:
                user_input = input(prompt)
                input_list = [datatype(item.strip()) for item in user_input.split(',')]
                
                for element in input_list:
                    res = bool(datetime.strptime(element, date_format))
                    if res == False:
                        raise FormatError(f"Input must have this format {date_format}.")
                    
                if len(input_list) != n_elements:
                    raise nElementsError(f"Input must contain exactly {n_elements} elements.")
                else:
                    user_input = input_list
            
            else:
                user_input = datatype(input(prompt))

        except ValueError:
            print(f"Sorry, The date type is wrong, enter a {datatype} type.")
        except FormatError as fe:
            print(fe)
        except nElementsError as ne:
            print(ne)
        else:
            break
    return user_input
                   

def block_hours():
    #n = int(input("Ingrese la cantidad de bloques horarios en 24h \n"))
    n = input_validation( "Ingrese la cantidad de bloques horarios en 24h \n", int)
    #time_values = input("Ingrese la hora de inicio de cada bloque en horario militar \n"
    #    "con el siguiente formato: hh:mm,hh:mm \n").split(",")
    time_values = input_validation( "Ingrese la hora de inicio de cada bloque en horario militar \n"
        "con el siguiente formato: hh:mm,hh:mm \n", str , list, n, "%H:%M" )
    values = input("Ingrese el valor de cada bloque \n"
    "con el siguiente formato: v1,v2 \n").split(",")
    
    time_datetimes = [datetime.strptime(time_str.strip(), "%H:%M") for time_str in time_values]
    values = [float(x) for x in values]

    output = get_hourly_data(time_datetimes, values)
    return output


def nearest(items, pivot):
    return min(items, key=lambda x: abs(x - pivot))

def detect_delimiter_and_decimal(file_path, sample_size=1024):
    with open(file_path, 'r') as file:
        sample = file.read(sample_size)
        
    sniffer = csv.Sniffer()
    delimiter = sniffer.sniff(sample).delimiter
    
    decimal = '.' if sample.count('.') > sample.count(',') else ','
    
    return delimiter, decimal


def open_filetype(filetype, filepath):
    
    try: 
        match filetype:
            case ".xlsx":
                out_df = pd.read_excel(filepath)
            case ".txt" | ".csv" :
                delimiter, decimal = detect_delimiter_and_decimal(filepath)
                out_df = pd.read_csv(filepath, sep = delimiter, decimal = decimal)
            case _:
                raise Exception
            
    except AttributeError:
        print(f"{filetype} is not a valid format type.")
        
    return out_df

def read_file():
    filepath = fd.askopenfilename(parent=window, filetypes=[("Excel Files", "*.xlsx"), ('CSV Files', '*.csv'),
                                                             ('TXT Files', '*.txt')])
    root, file_extension = os.path.splitext(filepath)
    print(root, "+", file_extension)
    df = open_filetype(file_extension, filepath)
    return df

def read_directory():

    df_list = []
    directory_path_str = fd.askdirectory(parent = window)
    directory = os.fsencode(directory_path_str)

    for file in os.listdir(directory):

        filename = os.fsdecode(file)
        filepath = os.path.join(directory_path_str, filename)
        root, file_extension = os.path.splitext(filepath)

        if file_extension in ['.xlsx', '.csv', '.txt']:
            df = open_filetype(file_extension, filepath)
            df = clean_df(df)
            df_list.append(df)

    return df_list

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

def filter_non_numeric_rows(df_p):
    return df_p[df_p.iloc[:,2:].apply(lambda row: all(str(val).replace('.', '').isdigit() 
                                            for val in row), axis=1)]


def clean_df(df):
    df.dropna(axis = 1, thresh = round(len(df.index) / 2), inplace = True)
    df.dropna(axis = 0, inplace = True)

    if df.index[0] > 0:
        new_header = df.iloc[0]
        df = df.iloc[1:]
        df.columns = new_header
        df.reset_index(drop = True, inplace = True)

    #units = df[ df[df.columns[0]].str.contains(r'unit', case=False, regex=True) ]


    df.rename(columns={ df.columns[0]: "Fecha" }, inplace = True)
    df.loc[:, df.columns != "Fecha"] = df.loc[:,df.columns != "Fecha"].apply(lambda x: pd.to_numeric(x, errors = 'coerce'))
    df["Fecha"] = df["Fecha"].apply(lambda x: pd.to_datetime(x, errors = 'coerce'))

    df.dropna(axis = 0, inplace = True)
    df.reset_index(drop = True, inplace = True)
    return df  


print("Hola bb")

window = tk.Tk()
window.wm_attributes('-topmost', 1)
window.withdraw()   # this supress the tk window


print("Ingrese: \n 1: Datos desde CSV \n 2: Datos ingresados como patrón"
       "\n 3: Salir")
input_type = int(input())

if input_type == 1:

    print("\n 1: Si cargará los datos en un único documento u hoja"
           "\n 2: Si cargará los datos de cada variable en un documento u hoja separado"
            "\n 3: Salir")
    read_file_type = int(input())

    if read_file_type == 1:
        df = read_file()
        df = clean_df(df)
    elif read_file_type == 2:
        df_list = read_directory()
        df_a = df_list[0]
        df_b = df_list[1]
        df_c = df_list[2]
    else:
        None

elif input_type == 2:
    Mtx_values, index_list = block_hours()
    print(Mtx_values)
else: 
    None
print("terminaste")
print("we are..")

