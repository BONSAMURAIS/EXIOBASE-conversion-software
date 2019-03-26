# About this repository
The code in this repository is for conversion of these tables into into the Bonsai RDF ontology.

This readme explains the reasoning behind the choice to use the hybrid (rather than monetary) tables of EXIOBASE for the hackathon prototype. 


# Versions of Exiobase currently available
On [exiobase.eu](https://www.exiobase.eu/index.php/component/users/?view=login&return=aHR0cHM6Ly93d3cuZXhpb2Jhc2UuZXUvaW5kZXgucGhwL2RhdGEtZG93bmxvYWQvZXhpb2Jhc2UzaHliLzEyNS1leGlvYmFzZS0zLTMtMTctaHN1dC0yMDExL2ZpbGU=&Itemid=251) there are monetary and hybid tables. 

### Monetary tables v3.4

Currently only Monetary Input-Otput tables (MIOTs) are uploaded on the website. There are two types of tables:

- Product by product (200x200) x 49 countries/ROW regions
- Industry by industry (163*163 ) x 49 countries//ROW regions

The tables are calculated for the years 1995-2011. The assumption used for the construction of the MIOTs is the industry technology assumption.

### Hybrid tables v3.3.17

The hybrid dataset includes HybriSupply and Use tables (HSUTs) and Hybrid Input-Output tables (HIOTs). The latter is determined using the by-product technology assumption. The tables are just for the year 2011.

## Differences between the two tables

The differencies between the types of tables are listed in the table below.

![Table](https://github.com/BONSAMURAIS/EXIOBASE-conversion-software/blob/master/differences_exiobase_monetary_physical.jpg)

## Selected framework for Bonsai

The hybrid supply and use tables are the natural choice for Bonsai for the following reasons:

- currently there are no monetary supply and use tables avalaible. The available MIOTs are the result of the adoption of specific constructs. The aim of Bonsai is to leave to the user the choice of the construct to transform supply and use tables into input-output tables.
- hybrid tables can be easily linked to other existing LCA-datasets becuase the tangible flows are accounted either in tonne or TJ. Therefore there is no need to use prices that may be a further source of uncertainty.

