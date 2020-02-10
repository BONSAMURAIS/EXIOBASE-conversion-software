#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""EXIOBASE-conversion-software csv2rdf-cli CLI.
Usage:
  csv2rdf-cli  -i <input/dirpath> -o <output/dirpath>  -c <HSUP/HUSE> --flowtype <input/output>
Options:
  -h --help     Show this screen.
  --version     Show version.
"""

import argparse
from docopt import docopt
from EXIOBASE_conversion_software import conversion
import sys


def main():
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

    parser.add_argument('--multifile',
                      default=100000,
                      dest="multifile",
                      help='Create multiple files each with x triples. Restricted to nt format.')

    parser.add_argument('--merge',
                      dest="merge",
                      help='If multifile is chosen, merge all nt files')

    args = parser.parse_args()

    try:
        conversion(args, 'csv2rdf')
    except KeyboardInterrupt:
        print("Terminating CLI")
        sys.exit(1)


if __name__ == "__main__":
    main()