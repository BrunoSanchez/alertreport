# Alertreport

Automatic reports for astronomical alerts

* Ingests a healpy map in fits format and a galaxy catalog -right now using the White catalog from [http://arxiv.org/abs/1103.0695](White et al. 2011)- and performs a series of plots crossmatching the galaxies and producing a latex table of objects to observe.
* After that a makefile is preset to produce a pdf displaying the
report of the observable objects.

## Workflow

The workflow of tools is changing right now.
But is kind of:

* Take a observatoy object (astroplan object) from conf.py and set it as location in earth
* Ingest the HealPy map, and take the relevant part (given our location on earth)
* Cross this map with a catalog of astronomical objects
* Perform likelihhood interpolation for every object
* Sort the results and generate a targets list
* Extract and plot information related to every target relevant for observers (heigth, airmass, char for field recognization)
* Publish this information in pdf in a friendly format.


*This is work for PhD @ UNC Cordoba Argentina*
   ...   
