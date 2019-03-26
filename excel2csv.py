#!/usr/bin/env python3
# Copyright (C) 2018  Vang Quy Le

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.


# Author: Vang Le-Quy (vle@its.aau.dk)
# Date: 20181205
# Description: To convert to CSV file for Bo Weidema (bweidema@plan.aau.dk)

# import logging as log
import csv
import sys
import re
import pandas as pd
from pyxlsb import open_workbook as open_xlsb
import numpy as np
# from numba import jit

# @jit
def convertxlsb2csv(exfile):
    out = re.sub(r'.xls.{0,1}$', '.csv', exfile)
    with open(out, mode='w') as outfile:
        csvwriter = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        with open_xslb(exfile) as wb:
            # Using the sheet index (1-based)
            with wb.get_sheet(2) as sheet:
                # You can use .rows(sparse=True) to skip empty rows
                for row in sheet.rows(sparse=True):
                    # values = [r.v for r in row if r.v is not None]  # retrieving content
                    values = [r.v for r in row]  # retrieving content
                    if values is not None:
                        # csv_line = ','.join(values)  # or do your thing
                        csvwriter.writerow(values)


def convertexcel2csv(exfile):

    out = re.sub(r'.xls.{0,1}$', '.csv', exfile)
    # sheetname below is either a string of sheetname or zero-based index number of sheet
    df = pd.read_excel(exfile, sheetname=1)
    df.to_csv(out)


def xlsb2pd(xlsb, sheetnum=2):
    '''Read and convert an XLSB Excel file to Pandas dataframes.
       By default, the data is expected to be on the second sheet
    '''
    products = []
    activities = []
    pros_acts = []

    with open_xlsb(xlsb) as wb:

        with wb.get_sheet(sheetnum) as sheet:
            rowcount = 0
            for row in sheet.rows(sparse=True):
                rowcount += 1
                vals = [item.v for item in row]
                if rowcount <= 4:
                    activities.append(vals[5:])
                if rowcount >= 4:
                    products.append(vals[0:4])
                    pros_acts.append(vals)
                if rowcount % 1000 == 0:
                    print('Converted ' + str(rowcount) + ' rows')

    products = pd.DataFrame(products[1:], columns=products[0])
    pros_acts = pd.DataFrame(pros_acts[1:], columns=pros_acts[0])
    activities = pd.DataFrame(activities)

    return (products, activities, pros_acts)
def xlsb2csv(xlsb, sheetnum = 2):
    '''
    convert a XLSB to a long table and write that table to a CSV file as well.
    The table is ready to be used for conversion to RDF.
    TODO: maybe add some caching to avoid reading the Excel file again.
    '''
    csvArr = []
    filename = re.sub(r'.xls.{0,1}$', '', xlsb)
    csvOut = 'long_' + filename + '.csv'
    with open_xlsb(xlsb) as wb:
        # Read the sheet to array first and convert to pandas first for quick access
        with wb.get_sheet(sheetnum) as sheet:
            for row in sheet.rows(sparse = True):
                vals = [item.v for item in row]
                csvArr.append(vals)

    csvDF = pd.DataFrame(csvArr)
    startRow = 4
    startCol = 5
    actTrans = csvDF.iloc[:4,].transpose() # Get the subset for activities
    outDF = []
    rows = csvDF.shape[0]
    cols = csvDF.shape[1]
    for i in range(startRow, rows):
        for j in range(startCol, cols):
            # read values
            if csvDF.iat[i,j] != 0: # Commented out to filter in the end with pandas
                mainFlow = (j == (i + 1))
                colAnnot = actTrans.iloc[j]
                rowAnnot = csvDF.iloc[i,0:5]
                outRow = np.concatenate((colAnnot, rowAnnot, [csvDF.iloc[i,j]], [mainFlow]),0)
                outDF.append(outRow)    
    outDF = pd.DataFrame(outDF) 
    # outDF = outDF.loc[outDF.iloc[:,5] != 0,:]
    outDF.to_csv(csvOut, header=False, index=False)
    return outDF

if __name__ == "__main__":
    # convertexcel2csv(sys.argv[1])
    # convertxlsb2csv(sys.argv[1])
    exfile = sys.argv[1]
    # (products, activities, pros_acts) = xlsb2pd(exfile)
    # filename = re.sub(r'.xls.{0,1}$', '', exfile)
    # actOut = 'act_' + filename + '.csv'
    # proOut = 'products_' + filename + '.csv'
    # proactOut = 'proact_' + filename + '.csv'

    # products.to_csv(proOut, index=None)
    # pros_acts.to_csv(proactOut, index=None)
    # activities.to_csv(actOut, header=None, index=None)
    xlsb2csv(exfile)
