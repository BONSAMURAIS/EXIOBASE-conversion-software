# About this repository
The code in this repository supports the conversion of these tables into into the Bonsai RDF ontology.

This readme also explains the reasoning behind the choice to use the hybrid (rather than monetary) tables of EXIOBASE for the prototype.

## Run it

### Setup
Clone repository
```bash
$ git clone git@github.com:BONSAMURAIS/EXIOBASE-conversion-software.git
$ cd EXIOBASE-conversion-software
```

Create pipenv

```bash
$ pipenv install
$ pipenv shell
```

### Install
```bash
$ python setup.py install
```


## Usage
### As a command line tool
### Convert `xslb` to `csv`
```
$ excel2csv-cli -i data/MR_HSUP_2011_v3_3_17.xlsb -o data/
$ excel2csv-cli -i data/MR_HUSE_2011_v3_3_17.xlsb -o data/
```

### Convert `csv` to `nt`
```
csv2rdf-cli -i data/MR_HSUP_2011_v3_3_17.csv -o data/  -c HSUP --flowtype output
csv2rdf-cli -i data/MR_HUSE_2011_v3_3_17.csv -o data/  -c HUSE --flowtype input
```

<!---
## Run with Docker

```bash
docker build  . -t bonsai/converter -f converter.dockerfile
```

create `data` directory
Download exiobase.zip inside  `data`
unzip
remove unused files

Convert supply table to `CSV`

```
docker run --rm  -v "$PWD/data":/data bonsai/converter python3 scripts/excel2csv.py -i data/MR_HSUP_2011_v3_3_17.xlsb -o data/

docker run --rm  -v "$PWD/data":/data bonsai/converter python3 scripts/excel2csv.py -i data/MR_HUSE_2011_v3_3_17.xlsb -o data/


docker run --rm  -v "$PWD/data":/data bonsai/converter python3 scripts/csv2rdf.py -i data/MR_HUSE_2011_v3_3_17.csv -o data/  -c HUSE --flowtype input

docker run --rm  -v "$PWD/data":/data bonsai/converter python3 scripts/csv2rdf.py -i data/MR_HSUP_2011_v3_3_17.csv -o data/  -c HSUP --flowtype output
```
-->

## Contributing
All contributions to the scripts should be via pull request. 
Please do not edit this package directly!

# Choice to use the hybrid tables of EXIOBASE

## Versions of Exiobase currently available
There are monetary and hybrid tables published on [exiobase.eu](https://www.exiobase.eu/index.php/component/users/?view=login&return=aHR0cHM6Ly93d3cuZXhpb2Jhc2UuZXUvaW5kZXgucGhwL2RhdGEtZG93bmxvYWQvZXhpb2Jhc2UzaHliLzEyNS1leGlvYmFzZS0zLTMtMTctaHN1dC0yMDExL2ZpbGU=&Itemid=251) .

### Monetary tables 

The Monetary Input-Otput tables (MIOTs) are calculated for the years 1995-2011. There are two types of tables:

- Product by product (200x200) x 49 countries/ROW regions
- Industry by industry (163*163 ) x 49 countries//ROW regions

The MIOTs were constructed using the industry technology assumption.

### Hybrid tables 

The hybrid dataset includes Hybrid Supply and Use tables (HSUTs) and Hybrid Input-Output tables (HIOTs). The tables are just for the year 2011.
The HIOT was constructed using the by-product technology assumption. 

## Differences between the two tables

The differencies between the types of tables are listed in the table below.

![Table](https://github.com/BONSAMURAIS/EXIOBASE-conversion-software/blob/master/differences_exiobase_monetary_physical.jpg)

The lack of value added in the hybrid table is a temporary issue

## Selected framework for Bonsai

For the purpose of this work we have used the hybrid supply and use tables (**v3.3.17**) were selected for the BONSAI prototype for the following reasons:

- The aim of Bonsai is to leave to the user the choice of algorithms to transform supply and use tables into input-output tables. Currently there are no monetary supply and use tables available. The available MIOTs are the result of the adoption of the specific industry technology assumption. 
- Hybrid tables can be easily linked to other existing LCA-datasets because the tangible flows are accounted either in tonne or TJ. Therefore there is no need to use prices that may be a further source of uncertainty.

