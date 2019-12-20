#!/usr/bin/env python3
#
# Program name: csv2rdf.py
# Description: convert CSV files with HSUP/HUSE data created by excel2rdf.py to RDF .
# This is a specific solution. Other uses need to adapt accordingly
#
# Last modified Time-stamp: <2018-12-14 10:43:21 CET (vle)>
# Author: Vang Le<vle@its.aau.dk>
# Created: 2018-12-13T21:34:06+0100

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

import re
import sys
import ntpath
import datetime
import argparse

import numpy as np
import pandas as pd

from rdflib import Graph, Literal, BNode, Namespace, URIRef
from rdflib.namespace import DCTERMS, FOAF, XSD, OWL, RDFS, RDF, SKOS

def file_name(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


def makeRDF(data, code="HSUP", isInput=True):
    '''
    create an RDF graph from a Pandas dataframe of 11 columns.
    the dataframe is output of the `xslb2csv` function.
    the code specifies which file is this taken from HSUP/HUSE/Other?
    isInput=true -> the data is about input/use flows
    isInput=false -> the data is about output/supply flows

    # Data row:
    0   1                           2       3        4    5            6       7        8        9             10
    AU  Cultivation of paddy rice   i01.a   A_PARI   AU   Paddy rice   p01.a   C_PARI   tonnes   6.147905e+05  True

    # cols 2/3 are redundant, 6/7 are also redundant -> we use only 3 and 7
    '''

    # Initialize graph and namespaces
    g = Graph()

    BONT = Namespace('http://ontology.bonsai.uno/core#')
    BRDFFO = Namespace("http://rdf.bonsai.uno/flowobject/exiobase3_3_17#")
    BRDFLO = Namespace("http://rdf.bonsai.uno/location/exiobase3_3_17#")
    BRDFTIME = Namespace("http://rdf.bonsai.uno/time#")
    BRDFFAT = Namespace("http://rdf.bonsai.uno/activitytype/exiobase3_3_17#")
    BRDFFOAF = Namespace("http://rdf.bonsai.uno/foaf#")
    BRDFDAT = Namespace("http://rdf.bonsai.uno/data/exiobase3_3_17/{}#".format(code.lower()))
    BRDFPROV = Namespace("http://rdf.bonsai.uno/prov#")
    CC = Namespace('http://creativecommons.org/ns#')
    DC = Namespace('http://purl.org/dc/elements/1.1/')
    DTYPE = Namespace("http://purl.org/dc/dcmitype/")
    NS0 = Namespace('http://purl.org/vocab/vann/')
    NS1 = Namespace("http://creativecommons.org/ns#")
    OM2 = Namespace('http://www.ontology-of-units-of-measure.org/resource/om-2/')
    OT = Namespace("https://www.w3.org/TR/owl-time/")
    SCHEMA = Namespace('http://schema.org/')
    TIME = Namespace('http://www.w3.org/2006/time#')
    XML = Namespace("http://www.w3.org/XML/1998/namespace")
    PROV = Namespace("http://www.w3.org/ns/prov#")


    g.bind("bont", BONT)
    g.bind("brdffo", BRDFFO)
    g.bind("brdflo", BRDFLO)
    g.bind("brdftime", BRDFTIME)
    g.bind("brdffat", BRDFFAT)
    g.bind("brdfdat", BRDFDAT)
    g.bind("brdfprov", BRDFPROV)
    g.bind("brdffoaf", BRDFFOAF)
    g.bind("cc", CC)
    g.bind("dc", DC)
    g.bind("dtype", DTYPE)
    g.bind("ns0", NS0)
    g.bind("ns1", NS1)
    g.bind("om2", OM2)
    g.bind("ot", OT)
    g.bind("schema", SCHEMA)
    g.bind("time", TIME)
    g.bind("xml", XML)
    g.bind("prov", PROV)

    ## Set metadata about this file
    # Author, CC licence, version

    DATASET = URIRef("http://rdf.bonsai.uno/data/exiobase3_3_17/{}".format(code.lower()))
    g.add( ( DATASET, RDF.type, DTYPE.Dataset ) )
    g.add( ( DATASET, RDF.type, PROV.Collection ) )
    g.add( ( DATASET, NS1.license, URIRef("http://creativecommons.org/licenses/by/3.0/") ) )
    g.add( ( DATASET, DC.creator, URIRef(BRDFFOAF.bonsai) ) )
    g.add( ( DATASET, DC.description, Literal("Flow and Activity instances extracted from EXIOBASE {} version 3.3.17".format(code)) ) )
    g.add( ( DATASET, DC.modified, Literal(datetime.date.today().strftime("%Y-%m-%d"),datatype=XSD.date) ) )
    g.add( ( DATASET, PROV.generatedAtTIme, Literal(datetime.date.today().strftime("%Y-%m-%d"),datatype=XSD.date) ) )
    g.add( ( DATASET, PROV.wasAttributedTo, BRDFFOAF.bonsai) )
    # Script version information needs to come from file
    g.add( ( DATASET, PROV.wasGeneratedBy, BRDFPROV["dataExtractionActivity_{}".format("0_4")]))
    g.add( ( DATASET, DC.title, Literal("EXIOBASE {} data v. 3.3.17".format(code)) ) )
    g.add( ( DATASET, NS0.preferredNamespaceUri, URIRef(BRDFDAT) ) )
    g.add( ( DATASET, OWL.versionInfo, Literal("0.4") ) )
    g.add( ( DATASET, FOAF.homepage, URIRef("http://rdf.bonsai.uno/data/exiobase3_3_17/{}/documentation.html".format(code.lower())) ) )

    # TODO: instantiate 2011 EXTENT URI as Temporal Extent to be assigned to the dataset

    # Defined in http://rdf.bonsai.uno/time/
    #2011_EXTENT_URI time:hasBeginning time:inXSDDate for 01 Jan 2011
    #2011_EXTENT_URI time:hasEnd time:inXSDDate for 31 Dec 2011
    extent2011node = URIRef("{}{}".format(BRDFTIME,'2011'))



    # TODO: Load Flow Objects, activity types, etc .. ?
    # This extracts the instances, they should have a mapping in the taxonomy above
    act_countries = data.iloc[:,0].unique()  # E.g., AU
    fobj_countries = data.iloc[:,4].unique()
    all_countries = np.unique(np.concatenate((act_countries, fobj_countries),0))

    #fobjs_numcodes = data.iloc[:,6].unique() # E.g., p01.a
    fobj_alphacodes = data.iloc[:,7].unique() # E.g., C_PARI

    #act_numcodes = data.iloc[:,2].unique() # E.g., i01.a
    act_alphacodes = data.iloc[:,3].unique() # E.g., A_PARI

    print("Working on:{} countries, {} activities, {} products".format(len(all_countries),
                                                                    len(fobj_alphacodes),
                                                                    len(act_alphacodes)
                                                                    ))
    code = code.lower()
    country_map = {}
    for c in all_countries:
        c_node = URIRef("{}{}".format(BRDFLO,c))
        country_map[c] = c_node

    fobj_map = {}
    for fo in fobj_alphacodes:
        fo_node = URIRef("{}{}".format(BRDFFO,fo))
        fobj_map[fo] = fo_node

    # For input flows we need the supply activities
    if isInput:
        sat_map = {}
        for fo in fobj_alphacodes:
            fo_node = URIRef("{}S_{}".format(BRDFFO,fo))
            sat_map[fo] = fo_node


    fat_map = {}
    for fa in act_alphacodes:
        fa_node = URIRef("{}{}".format(BRDFFAT,fa))
        fat_map[fa] = fa_node


    activity_instances_map = {}
    sup_activity_instances_map = {}

    ## Here is the instantiation of the actual data, the FLOWs
    for index, row in data.iterrows():
        if index%1000 == 1:
            print("Parsed {} flows / {} activities".format(index, len(activity_instances_map)))
        # TODO: Here for each row we need to instantiate:

        # FLOW_URI = generate Flow URI For this row
        flowNode = URIRef("http://rdf.bonsai.uno/data/exiobase3_3_17/{}#f_{}".format(code,index))
        # insert flow_uri is A Flow
        g.add((flowNode, RDF.type, BONT.Flow ))
        # Add provenance namedGraph member relation
        g.add((DATASET, PROV.hadMember, flowNode))


        # Load from database activity_instances ?
        # For now Just take as input then assume it exists
        ac_key = (row[0], row[3])
        if ac_key in activity_instances_map:
            acNode = activity_instances_map[ac_key]
        else :
            acNode = URIRef("http://rdf.bonsai.uno/data/exiobase3_3_17/{}#a_{}".format(code, len(activity_instances_map)))
            activity_instances_map[ac_key] = acNode

            # insert ACTIVITY_URI is a activty
            g.add((acNode, RDF.type, BONT.Activity ))

            # Add provenance namedGraph member relation
            g.add((DATASET, PROV.hadMember, acNode))

            # TODO: check that activity type exists in the vocabulary
            # ACTIVITY_TYPE_URI = get Act Type URI from row[2]/row[3]
            # ACTIVITY_URI b:activityType ACTIVITY_TYPE_URI
            g.add((acNode, BONT.activityType, fat_map[row[3]] ))


            # LOCATION_URI = get Location URI from row[0]
            # --> we do not have AGENT_URI = get Agent URI from LOCATION_URI
            # ACTIVITY_URI b:location LOCATION_URI
            g.add((acNode, BONT.location, country_map[row[0]] ))


            #ACTIVITY_URI b:hasTemporalExtent 2011_EXTENT_URI
            g.add((acNode, BONT.hasTemporalExtent, extent2011node ))


        # Insert in RDF data
        # When parsing the SUPPLY matrix we are instantiating OUTPUTS of activities

        if isInput:
            # Data from HUSE / HFD
            # FLOW_URI  b:inputOf ACTIVITY_URI
            g.add((flowNode, BONT.inputOf, acNode))

            # If this is an Input flow, then we have info on the provenance
            # we model an anonymous activity for which we register the location

            sup_ac_key = (row[4], row[7])
            if sup_ac_key in sup_activity_instances_map:
                sacNode = sup_activity_instances_map[sup_ac_key]
            else :
                # Supply activity node
                sacNode = URIRef("http://rdf.bonsai.uno/data/exiobase3_3_17/{}#sa_{}".format(code, len(sup_activity_instances_map)))
                sup_activity_instances_map[sup_ac_key] = sacNode

                # insert ACTIVITY_URI is a activty
                g.add((sacNode, RDF.type, BONT.Activity ))

                # TODO: check that activity type exists in the vocabulary
                # ACTIVITY_TYPE_URI = the act type is a SUPPLY of specific product row[7]
                # ACTIVITY_URI b:activityType ACTIVITY_TYPE_URI
                g.add((sacNode, BONT.activityType, sat_map[row[7]] ))


                # LOCATION_URI = get Location URI from row[4] country of provenance
                # --> we do not have AGENT_URI = get Agent URI from LOCATION_URI
                # ACTIVITY_URI b:hasLocation LOCATION_URI
                g.add((sacNode, BONT.hasLocation, country_map[row[4]] ))


                #ACTIVITY_URI b:hasTemporalExtent 2011_EXTENT_URI
                g.add((sacNode, BONT.hasTemporalExtent, extent2011node ))

            # This flow object is output of a generic supply activty
            g.add((flowNode, BONT.outputOf, sacNode))



        else:
            # Data from HSUP
            # FLOW_URI  b:outputOf ACTIVITY_URI
            g.add((flowNode, BONT.outputOf, acNode))

        if row[10] == True:
            # ACTIVITY_URI  b:determiningFlow FLOW_URI
            g.add((acNode,  BONT.determiningFlow, flowNode))
        elif row[10] != False:
            print("ERRRRRRR ",row[10])
            exit(3)

        g.add((flowNode, OM2.hasNumericValue, Literal(row[9], datatype=XSD.float) ))


        # om2:hasUnit om2:kilogram  row[8]
        if 'kilogram' in row[8]:
            g.add((flowNode,  OM2.hasUnit, OM2.kilogram))
        elif 'tonne' in row[8]:
            g.add((flowNode,  OM2.hasUnit, OM2.tonne))
        else :
            # Uknown, let's hope for the best
            g.add((flowNode,  OM2.hasUnit, OM2[row[8]]))

        # FLOW_URI bont:objectType _:uri41 .
        # FLOW_URI b:objectType get URI OF FLow Object (row[6]/row[7])
        g.add((flowNode,  BONT.objectType, fobj_map[row[7]]))

    return g


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Convert EXIOBASE .csv file to RDF/TTL')
    parser.add_argument('-i','--input',
                        dest='csvfile',
                        required=True,
                        help='<Required> path to csv file to convert')

    parser.add_argument('-o', '--outdir',
                        dest='outdir',
                        default='./',
                        help='Output directory')

    parser.add_argument('-c', '--code',
                        dest='code',
                        required=True,
                        help='The code of the specific file: HSUP/HUSE/HFD/Other?')

    parser.add_argument('--flowtype',
                      choices=['input','output'],
                      required=True,
                      help='If the flow are input or output of activites')

    parser.add_argument('--format',
                      choices=['nt','ttl', 'xml'],
                      default='nt',
                      help='The output format')


    args = parser.parse_args()

    csvfile = args.csvfile
    print("Parsing file: {}".format(csvfile))
    pandasDF=pd.read_csv(csvfile, header=None)

    # This will create the graph in memory!
    rdfGraph = makeRDF(pandasDF, args.code, isInput=(args.flowtype == 'input'))
    filename = re.sub(r'.csv$', '', file_name(csvfile))

    outdir = args.outdir
    if not outdir.endswith('/'):
        outdir = outdir + '/'

    rdfOut = outdir + filename + '.' + args.format

    print("Done making RDF graph. Final Size {} triples".format(len(rdfGraph)))
    # Output format default is NT so that i can be splitted
    rdfGraph.serialize(destination=rdfOut, format=args.format)
    print("Saved to {}".format(rdfOut))
