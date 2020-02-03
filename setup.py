from setuptools import setup, find_packages
import os

def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths


setup(
    name='EXIOBASE_conversion_software',
    version="0.4",
    packages=find_packages(),
    author="BONSAI team",
    author_email="info@bonsai.uno",
    license=open('LICENSE').read(),
    package_data={'EXIOBASE_conversion_software': package_files(os.path.join('EXIOBASE_conversion_software', 'data'))},
    entry_points = {
        'console_scripts': [
            'csv2rdf-cli = EXIOBASE_conversion_software.bin.csv2rdf_cli:main',
            'excel2csv-cli = EXIOBASE_conversion_software.bin.excel2csv_cli:main',
        ]
    },
    install_requires=[
        'numpy',
        'docopt',
        'pyxlsb',
        'pandas',
        'rdflib',
    ],
    url="https://github.com/BONSAMURAIS/EXIOBASE-conversion-software",
    long_description=open('README.md').read(),
    description="Extract Flows and Activities from the Exiobase HSUP and HUSE tables",
    classifiers=[
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Scientific/Engineering :: Visualization',
    ],
)