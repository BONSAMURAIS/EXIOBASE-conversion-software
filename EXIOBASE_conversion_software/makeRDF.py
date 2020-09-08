#!/usr/bin/env python3
#
# Program name: makeRDF.py
# Description: create an RDF file from a Pandas dataframe.
# This is a specific solution. Other uses need to adapt accordingly
#
# Last modified Time-stamp: <2018-12-14 10:43:21 CET (vle)>
# Authors: Emil Riis Hansen <emilrh@cs.aau.dk>, Matteo Lissandrini <matteo@cs.aau.dk>

# Copyright (C) 2020  Emil Riis Hansen, Matteo Lissandrini 

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


import sys
from pathlib import Path
from rdflib import Graph, Literal, Namespace, RDF, URIRef
from rdflib.namespace import XSD, OWL, RDFS
import numpy as np
from .excel2csv import xlsb2csv
import pandas as pd


def getAndSetNode(nID, ojDict, ojType="L"):
    """
    Utility function to get and set a node to a dictionary ojDict
    type: "L" for Literal, "U" for URIRef, and "B" for BNode
    But it is unlikely that we would create BNode this way.
    """
    funcMap = {"L": "Literal", "U": "URIRef", "B": "BNode"}
    if ojType not in funcMap:
        return "Unknown ojbect type: {}".format(ojType)
    if ojType == "B":
        return "Unknow behavior for BNode!"

    node = ojDict.get(nID)
    if node is None:
        node = locals()[funcMap[ojType]](nID)  # some magic here
        ojDict[nID] = node  # ojDict gets update and carried outside!
    return node


def makeRDF(inputDF):
    '''
    create an RDF graph from a Pandas dataframe of 11 columns.
    the dataframe is output of the `xslb2csv` function.
    '''
    # Define namespaces
    BASE = Namespace("http://bo.plan.aau.dk/exiobasev3/")
    LOCAL = BASE
    DCT = Namespace("http://purl.org/dc/terms/")
    DEF = Namespace(BASE + "definitions#")
    DCAT = Namespace("http://www.w3.org/ns/dcat#")
    PROV = Namespace("http://www.w3.org/ns/prov#")
    OM = Namespace("http://www.ontology-of-units-of-measure.org/resource/om-2/")

    # Initialize graph and namespaces
    g = Graph()
    # g = Graph(identifier="TestGraph")

    g.bind("local", LOCAL)
    g.bind("owl", OWL)
    g.bind("xsd", XSD)
    g.bind("dct", DCT)
    g.bind("def", DEF)
    g.bind("dcat", DCAT)
    g.bind("prov", PROV)
    g.bind("om", OM)
    # g.parse('./datasetmeta.ttl', format = 'n3')

    # meta data
    DATASET = URIRef(LOCAL + "EXIOBASE3.3.15HSUT2011")  # dataset name
    DATAFILE = URIRef(LOCAL + "MR_HSUP_2011_v3_3_15.xlsb")
    g.add((
        DATASET,
        RDF.type,
        DCAT.Dataset
    )
    )

    g.add((
        DATASET,
        DCAT.landingPage,
        URIRef("https://www.exiobase.eu/index.php/data-download/exiobase3hyb")
    )
    )
    g.add((
        DATASET,
        DCAT.distribution,
        DATAFILE
    ))

    g.add((
        DATASET,
        DCT.title,
        Literal("EXIOBASE 3.3.15 - HSUT - 2011")
    ))

    g.add((
        DATASET,
        RDFS.comment,
        Literal("A conversion from Binary Exel to RDF for use with other tools and datasets")
    ))
    g.add((
        DATASET,
        PROV.startedAtTime,
        Literal("2018-09-20T00:00:00", datatype=XSD.dateTime)
    ))
    g.add((
        DATASET,
        PROV.endedAtTime,
        Literal("2018-09-20T24:00:00", datatype=XSD.dateTime)
    ))

    # Define file

    g.add((
        DATAFILE,
        RDF.type,
        DCAT.Distribution
    ))
    g.add((
        DATAFILE,
        DCAT.mediaType,
        URIRef("https://www.exiobase.eu/index.php/data-download/exiobase3hyb/124-exiobase-3-3-15-hsut-2011")
    ))
    g.add((
        DATAFILE,
        DCAT.downloadUrl,
        Literal("application/vnd.ms-excel.sheet.binary.macroEnabled.12")
    ))

    # Relationship type
    activity = (DEF.activity, RDF.type, PROV.activity)
    activityCode1 = (DEF.activityCode1, RDF.type,
                     Literal("Some description for Activity Code 1"))
    activityCode2 = (DEF.activityCode2, RDF.type,
                     Literal("Some description for Activity Code 2"))
    activityName = (DEF.activityName, RDF.type, DCT.title)
    countryCode = (DEF.countryCode, RDF.type,
                   Literal("ISO3166 Alpha 2 Country Code"))
    hasActivity = (DEF.hasActivity, RDF.type, PROV.wasAssociatedWith)
    hasAmount = (DEF.hasAmount, RDF.type, PROV.generated)
    isMainProduct = (DEF.isMainProduct, RDF.type,
                     PROV.wasAssociatedWith)
    hasProduct = (DEF.hasProduct, RDF.type, PROV.generated)
    product = (DEF.product, RDF.type, PROV.entity)
    productCode1 = (DEF.productCode1, RDF.type, Literal("Some description for Product Code 1"))
    productCode2 = (DEF.productCode2, RDF.type, Literal("Some description for Product Code 2"))
    productName = (DEF.productName, RDF.type, DCT.title)

    objectList = [
        activity,
        activityCode1,
        activityCode2,
        activityName,
        countryCode,
        hasActivity,
        isMainProduct,
        hasProduct,
        hasAmount,
        product,
        productCode1,
        productCode2,
        productName]

    for triple in objectList:
        g.add(triple)

    # Now ready to loop and add
    # Processing country list

    actCountries = inputDF.iloc[:, 0].unique()
    prodCountries = inputDF.iloc[:, 4].unique()
    COUNTRIES = np.unique(np.concatenate((actCountries, prodCountries), 0))
    productCodes1 = inputDF.iloc[:, 6].unique()
    activityCodes1 = inputDF.iloc[:, 2].unique()

    print("Working on:{} countries, {} activities, {} products".format(len(COUNTRIES),
                                                                       len(activityCodes1),
                                                                       len(productCodes1)
                                                                       ))
    trackCountry = {}
    for c in COUNTRIES:
        country = URIRef(BASE + "country#" + c)
        trackCountry[c] = country
        g.add((country, DEF.countryCode, Literal(c, datatype=XSD.string)))

    for index, row in inputDF.iterrows():

        # Data row:
        # 0 	1                         	2     	3    	4 	5          	6     	7      	8       	9       	10
        # AU 	Cultivation of paddy rice 	i01.a 	A_PARI 	AU 	Paddy rice 	p01.a 	C_PARI 	tonnes 	6.147905e+05 	True

        activityCode1 = Literal(row[2])
        activityCode2 = Literal(row[3])

        productCode1 = Literal(row[6])
        productCode2 = Literal(row[7])
        thisProduct = URIRef(BASE + "product#" + row[6])

        acountry = getAndSetNode(row[0], trackCountry, "L")
        # thisActivity = getAndSetNode(BASE + "activity/" + row[2], trackActivity, "U")
        thisActivity = URIRef(BASE + "activity#" + row[2])

        g.add((thisActivity, RDF.type, DEF.activity))
        g.add((thisActivity, DEF.activityCode1, activityCode1))
        g.add((thisActivity, DEF.activityCode2, activityCode2))
        g.add((thisActivity, DEF.country, acountry))
        g.add((thisActivity, DEF.activityName, Literal(row[1])))
        g.add((thisActivity, DEF.hasProduct, thisProduct))
        if (row[10]):
            g.add((thisProduct, DEF.isMainProduct, thisActivity))
        g.add((DATASET, DEF.hasActivity, thisActivity))
        pcountry = getAndSetNode(row[4], trackCountry, "L")

        g.add((thisProduct, RDF.type, DEF.product))
        g.add((thisProduct, DEF.productCode1, productCode1))
        g.add((thisProduct, DEF.productCode2, productCode2))
        g.add((thisProduct, DEF.country, pcountry))
        g.add((thisProduct, DEF.productName, Literal(row[5])))

        thisAmount = URIRef(BASE + "measure#" + row[4] + "_" + row[3] + row[6])
        g.add((thisAmount, RDF.type, OM.measure))
        # g.add( (thisAmount, DEF.countryCode, pcountry ) )
        # g.add( (thisAmount, DEF.productCode1, productCode1 ) )
        g.add((thisAmount, OM.quantity, Literal(row[9], datatype=XSD.float)))
        g.add((thisAmount, OM.hasUnit, URIRef(OM + row[8])))
        g.add((thisAmount, DCT.title, productCode2))
        # asociate product to measure
        g.add((thisProduct, DEF.hasAmount, thisAmount))
    return g


def makeRdf():
    exfile = sys.argv[1]
    filename = Path(exfile).stem
    outCSV = "long_" + filename + ".csv"
    if Path(outCSV).is_file():
        pandasDF = pd.read_csv(outCSV, header=None)
    else:
        pandasDF = xlsb2csv(exfile, sheetnum=2)  # This will also write a CSV output with name 'long_*.csv'
    rdfGraph = makeRDF(pandasDF)
    print("Done making RDF graph")
    rdfGraph.serialize(destination=(filename + '.rdf'), format='xml')
