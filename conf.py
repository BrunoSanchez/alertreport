#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

import astropy.units as u
from astropy.coordinates import EarthLocation
from pytz import timezone
from astroplan import Observer

longitude = '-31.4d'
latitude = '-64.5d'
elevation = 1350 * u.m
location = EarthLocation.from_geodetic(longitude, latitude, elevation)

observer = Observer(name='EABA',
               location=location,
               pressure=0.615 * u.bar,
               relative_humidity=0.11,
               temperature=0 * u.deg_C,
               timezone=timezone('America/Argentina/Cordoba'),
               description="Estacion Astrofisica Bosque Alegre")


obs_date=time.strftime("%Y/%m/%d %H:%M")

# Astronomical cuts
dist_lim = 80.  # Mpc
app_mag = 18.
abs_mag = -18
dec_lim = 30.


# Directories where to store stuff
plots = './plots'
skymap = './skymap.fits'
catalog = './cats/GWGCCatalog.txt'


