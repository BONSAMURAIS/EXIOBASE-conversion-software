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

import re
import csv
import sys
import argparse

import ntpath
import pandas as pd
import numpy as np

from pyxlsb import open_workbook as open_xlsb

def file_name(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


def xlsb2csv(xlsb, outdir, sheetnum = 2, csvOut=None):
    '''
    convert a XLSB to a long table and write that table to a CSV file as well.
    The table is ready to be used for conversion to RDF.
    TODO: maybe add some caching to avoid reading the Excel file again.
    '''
    csvArr = []

    if csvOut is None:
        filename = re.sub(r'.xls.{0,1}$', '', file_name(xlsb))
        csvOut = outdir + filename + '.csv'
    else :
        csvOut = outdir + csvOut

    with open_xlsb(xlsb) as wb:
        # Read the sheet to array first and convert to pandas first for quick access
        with wb.get_sheet(sheetnum) as sheet:
            for row in sheet.rows(sparse = True):
                vals = [item.v for item in row]
                csvArr.append(vals)

    csvDF = pd.DataFrame(csvArr)
    # Start or and colum take into account headers
    startRow = 4
    startCol = 5
    print("Parsed sheet has size {}".format(csvDF.shape))

    ## Separates Header information from actual data
    actTrans = csvDF.iloc[:4,].transpose() # Get the subset for activities
    outDF = []
    rows = csvDF.shape[0]
    cols = csvDF.shape[1]
    for i in range(startRow, rows):
        if (i-startRow)%50 ==1:
            print("Parsed {}".format(i-startRow-1))
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
    print("Saving to {}".format(csvOut))
    outDF.to_csv(csvOut, header=False, index=False)
    return outDF

def excel2csv(args):

    exfile = args.exfile
    outdir = args.outdir
    if not outdir.endswith('/'):
        outdir = outdir + '/'
    print("Parsing file: {}".format(exfile))

    # All files in sheet num 1 contain metadata:
    # -> year + timestamp of production + version number
    # This metada is not parsed currently


    # File HSUP & HUSE both parse sheet number 2

    # File HSUT_extension contains both outputs and input flows
    # contains multiple separate sheets
    # Requires to instantiate flow objects 66 - 19 - 7 - 39

    # HFD  sheet FD (2) for Final demand and sheet stock_to_waste (3) for Stock to waste
    # This one is missing the activity types 6+1


    xlsb2csv(exfile, outdir)
