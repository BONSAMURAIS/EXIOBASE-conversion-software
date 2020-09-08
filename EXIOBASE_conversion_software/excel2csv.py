#!/usr/bin/env python3
# Copyright (C) 2020  Emil Riis Hansen

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


# Author: Emil Riis Hansen (emilrh@cs.aau.dk)
# Date: 20181205
# Description: To convert excel to CSV file 

# import logging as log

import re
import os
import ntpath
import pandas as pd
import numpy as np
import pkg_resources
from collections import namedtuple

ObjectAggregation = namedtuple('ObejectAggretation', ['product_name', 'agg_product_name', 'product_code',
                                                      'agg_product_code', 'activity', 'activity_code'])


def file_name(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


def load_dataset(file_handler, sheetname):
    return pd.read_excel(
        file_handler,
        sheet_name=sheetname,
        header=0,
    )


def xlsb2csv(xlsb, outdir, sheetnum=1, csvOut=None):
    '''
    convert a XLSB to a long table and write that table to a CSV file as well.
    The table is ready to be used for conversion to RDF.
    TODO: maybe add some caching to avoid reading the Excel file again.
    '''

    if csvOut is None:
        filename = re.sub(r'.xls.{0,1}$', '', file_name(xlsb))
        csvOut = outdir + filename + '.csv'
    else:
        csvOut = outdir + csvOut

    # Load Exiobase Classifications
    file_path = os.path.join("data", "exiobase_classifications_v_3_3_17.xlsx")
    file_handler = pkg_resources.resource_stream(__name__, file_path)
    obj_agg = load_dataset(file_handler, "Product_activity_correspondence")
    determining_flows = {product: activity for product, activity in
                         zip(obj_agg['agg_product_code'], obj_agg['activity_code'])}

    # Create dictionary of aggregate product codes,
    # along with the disaggregation
    object_aggregates = dict()
    agg_products = ['C_CLPT', 'C_GASS', 'C_COPR', 'C_REFP', 'C_CHBI', 'C_BGAS']
    for index, row in obj_agg.iterrows():
        if row['agg_product_code'] in agg_products:
            if row['agg_product_code'] in object_aggregates:
                object_aggregates[row['agg_product_code']].append(ObjectAggregation(row['product_name'],
                                                                                    row['agg_product_name'],
                                                                                    row['product_code'],
                                                                                    row['agg_product_code'],
                                                                                    row['activity'],
                                                                                    row['activity_code']))
            else:
                object_aggregates[row['agg_product_code']] = [ObjectAggregation(row['product_name'],
                                                                                row['agg_product_name'],
                                                                                row['product_code'],
                                                                                row['agg_product_code'],
                                                                                row['activity'],
                                                                                row['activity_code'])]

    csvDF = pd.read_excel(xlsb, sheet_name=sheetnum, engine='pyxlsb', header=None)

    # Rename header
    names = {0: 'country', 1: 'product_name', 2: 'product_code_1', 3: 'product_code_2', 4: 'unit'}
    csvDF.rename(columns=names, inplace=True)

    # Copy disaggregate product rows
    csvAggreg = pd.DataFrame(columns=csvDF.columns)
    for key in object_aggregates.keys():
        disag_prods = csvDF.loc[csvDF['product_code_2'].isin([tup.product_code for tup in object_aggregates[key]])].copy(deep=True)

        aggregate = disag_prods.groupby([disag_prods.country, disag_prods.unit], as_index=False).sum()
        aggregate['product_name'] = object_aggregates[key][0].agg_product_name
        aggregate['product_code_2'] = object_aggregates[key][0].agg_product_code
        if aggregate.shape[0] > 0:
            csvAggreg = pd.concat([csvAggreg, aggregate])

    # Add aggregate rows to top of csvDF
    csvDF = pd.concat([csvDF.iloc[:4], csvAggreg, csvDF.iloc[4:]]).reset_index(drop=True)

    # Start row and column take into account headers
    startRow = 4
    startCol = 5
    print("Parsed sheet has size {}".format(csvDF.shape))

    # Separates Header information from actual data
    actTrans = csvDF.iloc[:4, ].transpose()  # Get the subset for activities
    outDF = []
    rows = csvDF.shape[0]
    cols = csvDF.shape[1]
    for i in range(startRow, rows):
        if (i - startRow) % 50 == 1:
            print("Parsed {}".format(i-startRow-1))
        for j in range(startCol, cols):
            # read values
            if csvDF.iat[i, j] != 0:  # Comment out to filter in 0 value flows
                colAnnot = actTrans.iloc[j]
                row_annot = csvDF.iloc[i, 0:5]
                # Based on exiobase classifications, determine whether a flow is determining
                if csvDF.iloc[i, 3] in determining_flows and determining_flows[csvDF.iloc[i, 3]] == colAnnot[3]:
                    determining = True
                else:
                    determining = False
                outRow = np.concatenate((colAnnot, row_annot, [csvDF.iloc[i, j]], [determining]), 0)
                outDF.append(outRow)
    outDF = pd.DataFrame(outDF)

    print("Saving to {}".format(csvOut))
    if not os.path.exists(outdir):
        os.makedirs(outdir)
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
