# hello.py
import numpy as np
import xlwings as xw

def world():
    wb = xw.Book.caller()
    ws_test = wb.sheets('Hoja3')
    ws_test.range('A1').value = "Perritos Ome"
