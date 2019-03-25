# EXIOBASE-conversion-software
This repo explains the reasons behind the choice of the EXIOBASE version adopted in the initial version of Bonsai and how to convert the dataset into RDF.

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

