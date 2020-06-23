__all__ = (
    "csv2rdf",
    "excel2csv",
    "makeRDF",
)

VERSION = (0, 5)
__version_dot__ = ".".join(str(v) for v in VERSION)
__version_dash__ = "_".join(str(v) for v in VERSION)

data_dir = "../data"

from .csv2rdf import csv2rdf
from .excel2csv import excel2csv
from .makeRDF import makeRDF


def conversion(args, script):
    if script == 'excel2csv':
        excel2csv(args)
    elif script == 'csv2rdf':
        csv2rdf(args)