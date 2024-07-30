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
import re


class DataReceiverFile:

    filetype = "None"
    num_fields = 0
    num_records = 0
    multiple_files = False
    df = None
    fields = []

    #Detect what symbol is used as the decimal point and detect the delimiter
    #from CSV or txt file
    def __detect_delimiter_and_decimal(self, file_path, sample_size=1024):
        with open(file_path, 'r') as file:
            sample = file.read(sample_size)
            
        sniffer = csv.Sniffer()
        delimiter = sniffer.sniff(sample).delimiter
        
        decimal = '.' if sample.count('.') > sample.count(',') else ','
        
        return delimiter, decimal
    
    #convert data to dataframe.
    def __df_from_filetype(self, filetype, filepath):
    
        try: 
            match filetype.lower():
                case ".xlsx":
                    out_df = pd.read_excel(filepath)
                case ".txt" | ".csv" :
                    delimiter, decimal = self.__detect_delimiter_and_decimal(filepath)
                    out_df = pd.read_csv(filepath, sep = delimiter, decimal = decimal, dtype= str)
                case _:
                    raise Exception
                
        except AttributeError:
            print(f"{filetype} is not a valid format type.")
            
        return out_df


    #Read a single file and return a dataframe
    def read_file(self):

        window = tk.Tk()
        window.wm_attributes('-topmost', 1)
        window.withdraw()   # this supress the tk window

        filepath = fd.askopenfilename(parent=window, filetypes=[("Excel Files", "*.xlsx"), ('CSV Files', '*.csv'),
                                                                ('TXT Files', '*.txt')])
        root, file_extension = os.path.splitext(filepath)
        print(root, "+", file_extension)
        self.filetype = file_extension
        self.df = self.__df_from_filetype(file_extension, filepath)
        self.df = self.__clean_df(self.df)
        self.num_fields = len(self.df.columns)
        self.multiple_files = False

        window.destroy()

        return self.df

    #Read directory which could contain multiple files and concatenate them together
    #to single dataframe
    def read_directory(self):

        window = tk.Tk()
        window.wm_attributes('-topmost', 1)
        window.withdraw()   # this supress the tk window

        self.fields = []
        directory_path_str = fd.askdirectory(parent = window)
        directory = os.fsencode(directory_path_str)

        for file in os.listdir(directory):

            filename = os.fsdecode(file)
            filepath = os.path.join(directory_path_str, filename)
            root, file_extension = os.path.splitext(filepath)

            if file_extension in ['.xlsx', '.csv', '.txt']:
                self.df = self.df_from_filetype(file_extension, filepath)
                self.df = self.__clean_df(self.df)
                self.fields.append(self.df)
            else:
                print("Please specify the right type of file")

        self.df =  pd.concat(self.fields, ignore_index=True) if self.fields else pd.DataFrame()
        self.num_fields = len(self.df.columns)
        self.multiple_files = True
        self.filetypes = "Multiple"
        window.destroy()

        return self.df

    #Clean the dataframe, first clean NAN rows and columns, then detect the "fecha"
    #column and cast to NAN non-numeric or non-datetime values to finally delete them
    def __clean_df(self, df): 
        df.dropna(axis = 1, thresh = round(len(df.index) / 2), inplace = True)
        df.dropna(axis = 0, inplace = True)

        if df.index[0] > 0:
            new_header = df.iloc[0]
            df = df.iloc[1:]
            df.columns = new_header
            df.reset_index(drop = True, inplace = True)

        new_column_names = {col: "Fecha" for col in df.columns if any(keyword in col.lower() for
                                                                       keyword in ["date", "name","time", "fecha"])}
        df.rename(columns=new_column_names, inplace=True)
        df.loc[:, df.columns != "Fecha"] = df.loc[:,df.columns != "Fecha"].apply( lambda x: x.str.replace(',', '.') )
        df.loc[:, df.columns != "Fecha"] = df.loc[:,df.columns != "Fecha"].map( self.__non_decimal )
        df.loc[:, df.columns != "Fecha"] = df.loc[:,df.columns != "Fecha"].apply(lambda x: pd.to_numeric(x, errors = 'coerce'))
        df["Fecha"] = df["Fecha"].apply(lambda x: pd.to_datetime(x, errors = 'coerce'))

        df.dropna(axis = 1, thresh = round(len(df.index) / 2), inplace = True)
        df.dropna(axis = 0, inplace = True)
        df.reset_index(drop = True, inplace = True)
        self.df = df
        return df  

    #If value is str, return string without characters different from
    #digits, dots, commas or negative signs.
    def __non_decimal(self, value):
        if isinstance(value, str):
            non_decimal = re.compile(r'[^\d.,-]+')
            return non_decimal.sub("", value)
        else:
            return value
 
    

test1 = DataReceiverFile()
test1.read_file()

print(test1.df.describe())
print(test1.df.info())
print(test1.df.mean())

