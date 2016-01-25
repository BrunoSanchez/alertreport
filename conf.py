#!/usr/bin/env python
# -*- coding: utf-8 -*-

from reportlab.lib.pagesize import a4

plots = './plots'

obs_lat = '-31.4'
obs_lon = '-64.5'
obs_elevation = 1350
obs_name = 'EABA'

skymap = './skymap.fits'

catalog = './GWGCCatalog.txt'

docsize = a4

# Astronomical cuts
dist_lim = 80.  # Mpc
app_mag = 18.
abs_mag = -18
dec_lim = 30.
