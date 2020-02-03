#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Arborist CLI.
Usage:
  arborist-cli regenerate <dirpath>
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

    args = parser.parse_args()

    try:
        conversion(args, 'excel2csv')
    except KeyboardInterrupt:
        print("Terminating CLI")
        sys.exit(1)


if __name__ == "__main__":
    main()