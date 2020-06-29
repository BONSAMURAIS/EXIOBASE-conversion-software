#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""EXIOBASE-conversion-software excel2csv CLI.
Usage:
  excel2csv-cli -i <input/dirpath> -o <output/dirpath> -c <HSUP/HUSE>
Options:
  -h --help     Show this screen.
  --version     Show version.
"""

import argparse
from docopt import docopt
from EXIOBASE_conversion_software import conversion
import sys


def main():
    parser = argparse.ArgumentParser(description='Convert EXIOBASE .xslb file to csv')
    parser.add_argument('-i','--import',
                        dest='exfile',
                        help='<Required> path to file to convert')

    parser.add_argument('-o', '--outdir',
                        dest='outdir',
                        default='./',
                        help='Output directory')

    parser.add_argument('-c', '--code',
                        dest='code',
                        required=True,
                        help='The code of the specific file: HSUP/HUSE/HFD/Other?')

    args = parser.parse_args()

    try:
        conversion(args, 'excel2csv')
    except KeyboardInterrupt:
        print("Terminating CLI")
        sys.exit(1)


if __name__ == "__main__":
    main()