#!/usr/bin/env python
# -*- coding: utf-8 -*-


# Copyright (c) 2016, Cordoba Astronomical Observatory.  All rights reserved.
#                    Unauthorized reproduction prohibited.
# NAME:
#        Alertreport
# PURPOSE:
#        Toritos Scheduler White catalog loader
#
# CATEGORY:
#        Program.
#
# INPUTS:
#
#
# MODIFICATION HISTORY:
#   Written by: Mariano Dominguez, July 2015
#    from previuos version using White Catalog January 2014.
#    Any inquirities send an e-mail to mardom@oac.uncor.edu
#
#   Modified by Bruno Sanchez,
#    any inquirities send an email to bruno@oac.unc.edu.ar

# TODO  we should avoid the galactic plane
# TODO  we should avoid moon, and moon phases
# TODO  we should try to use pairs of galaxies

# Load useful packages
import os
import time

import numpy as np
import math as m

import ephem
import seaborn
import matplotlib.pyplot as plt

from astropy import units as u
from astropy.io import ascii
from astropy.coordinates import SkyCoord
from astropy.coordinates import FK5

# Global paths and constants
import conf as cf

data_path = '.'
plots = cf.plots
if not os.path.isdir(plots):
    os.mkdir(plots)


obs_date=time.strftime("%Y/%m/%d %H:%M:%S")

obs = ephem.Observer()
obs.lat = cf.obs_lat
obs.lon = cf.obs_lon
obs.elevation = cf.obs_elevation

# extracting the correct values. WEIRD
print float(ephem.degrees(obs.lon*180./m.pi)), float(ephem.degrees(obs.lat*180./m.pi))

sun = ephem.Sun()
sun.compute(obs)
print sun.a_ra, sun.a_dec
sun_coords = SkyCoord(str(sun.a_ra), str(sun.a_dec), unit=(u.hourangle, u.deg))

print "Sun coordinates are = {}".format(sun_coords.to_string('hmsdms'))

moon = ephem.Moon()
moon.compute(obs)
moon_coords = SkyCoord(str(moon.a_ra), str(moon.a_dec), unit=(u.hourangle, u.deg))

print "Moon coordinates are = {}".format(moon_coords.to_string('hmsdms'))


# This part intends to calculate the rising and setting of the sun at the given date and at Macon.
# Since the big errors and differences for the actual setting and rising times of the sun here,
# we don't trust it at all. Anyway it is not used for any kind of calculation.

# In[9]:

sunrise, sunset = obs.next_rising(sun), obs.next_setting(sun)

print "The time of sunset is {}, \nand the time of sunrise is {}".format(sunset, sunrise)

# at sunset
alpha_zenith_sunset = sun_coords.ra + 105.*u.deg
alpha_observable_min = alpha_zenith_sunset - 40.*u.deg

# at sunrise
alpha_zenith_sunrise = sun_coords.ra - 105.*u.deg
alpha_observable_max = alpha_zenith_sunrise + 40.*u.deg

print alpha_observable_min.hour, alpha_observable_max.hour

white_cat= cf.catalog
white_table = ascii.read(white_cat, delimiter=' ', format='commented_header')#, data_start=2

dist_lim = cf.dist_lim
near = white_table['Dist'] < dist_lim      # Distance cut
visible = white_table['App_Mag']< cf.app_mag     # Apparent Magnitude cut
bright = white_table['Abs_Mag']< cf.abs_mag      # Absolute Magnitude cut
lim_dec = white_table['Dec']< cf.dec_lim          # Declination cut
alfa_min = white_table['RA'] >  float(alpha_observable_min.hour)       # Alpha cut
alfa_max = white_table['RA'] <= float(alpha_observable_max.hour)


if alpha_observable_max.hour > alpha_observable_min.hour:
    sample = white_table[near & visible & bright & lim_dec & (alfa_min & alfa_max)]
else:
    sample = white_table[near & visible & bright & lim_dec & (alfa_min | alfa_max)]

# Plot of magnitudes Histogram
plt.hist(sample['App_Mag'])
plt.xlabel('App B Mag')
plt.ylabel('Number')
plt.title('App B Mag sample histogram')

plt.savefig(os.path.join(plots, 'appmag_sample_histogram.png'), dpi=300)

# Plot of RA histogram
plt.hist(sample['RA'])
plt.xlabel('RA [h]')
plt.ylabel('Number')
plt.title('Right Ascension sample histogram')

plt.savefig(os.path.join(plots, 'RA_sample_histogram.png'), dpi=300)

# Plot of aitoff projection in the sky
plt.figure(figsize=(10,10))
plt.subplot(211, projection="aitoff")
deg2rad=np.pi/180.

x = sample['RA']*15.*deg2rad
xg = []
for ax in x:
    if ax > m.pi:
        ax = ax - 2*m.pi
    xg.append(ax)


yg = sample['Dec']*deg2rad

ramax = alpha_observable_max.hour
if alpha_observable_min.hour > 12. :
    ramin = alpha_observable_min.hour - 24.
else:
    ramin = alpha_observable_min.hour

mean_zenith_ra = ((ramax-ramin)*15./2.)
zenith_dec = float(ephem.degrees(obs.lat*180./m.pi))

#print mean_zenith_ra, zenith_dec

plt.plot(xg,yg, "r.")

plt.plot(mean_zenith_ra*deg2rad, zenith_dec*deg2rad, 'bo' )
plt.grid(True)
plt.title("Aitoff projection of the observable\n objects from Macon")
plt.xlabel("Right Ascention [deg]")
plt.ylabel("Declination [deg]")
plt.savefig(os.path.join(plots, 'radec_aitoff_sample.png'), dpi=300)


# In[20]:

plt.hist(sample['Dist'], range=[1,dist_lim])
plt.title('Distance histogram of the objects\n observable from Macon')

plt.xlabel('Distance [Mpc]')
plt.ylabel('Number')

plt.savefig(os.path.join(plots, 'distance_histogram_sample.png'), dpi=300)

#plt.show()


# In[21]:

import healpy as hp


# In[22]:

aligo_alert_data_file=os.path.join(data_path,"skymap.fits")
NSIDE=512 #2048
aligo_banana = hp.read_map(aligo_alert_data_file)


# In[23]:

from astropy.io import fits
hdr1 = fits.getheader(aligo_alert_data_file)


# plot the banana map
fig = plt.figure(2, figsize=(10, 10))
hp.mollview(aligo_banana, title='aLIGO alert Likelihood level', flip="astro",
            unit='$\Delta$', fig=2)
fig.axes[1].texts[0].set_fontsize(8)

#mean_zenith_ra = 15.*(alpha_observable_max.hour+alpha_observable_min.hour)/2.
#zenith_dec = float(ephem.degrees(macon.lat*180./m.pi))

hp.projscatter(mean_zenith_ra, zenith_dec
               , lonlat=True, color="red")
hp.projtext(mean_zenith_ra, zenith_dec,
            'Macon Zenith\n (mean position\n over the night)', lonlat=True, color="red")
for ra in range(0,360,60):
    for dec in range(-60,90,30):
        if not (ra == 300 and dec == -30):
                hp.projtext(ra,dec,'({}, {})'.format(ra,dec), lonlat=True, color='red')

hp.graticule()

plt.savefig(os.path.join(plots, 'allsky_likelihoodmap.png'), dpi=300)
#plt.show()


# In[28]:

# plot the banana map
fig = plt.figure(2, figsize=(10, 10))
rot=[mean_zenith_ra, zenith_dec]
hp.gnomview(aligo_banana, rot=rot, title='aLIGO alert likelihood level zoom on\n Macon zenith', flip="astro",
            unit='$\Delta$', fig=2, xsize=800, reso=5)
fig.axes[1].texts[0].set_fontsize(8)

hp.projscatter(rot, lonlat=True, color="red")
hp.projtext(mean_zenith_ra, zenith_dec,
            'Macon Zenith\n (mean position\n over the night)', lonlat=True, color="red")

for ra in range(int(mean_zenith_ra)-30, int(mean_zenith_ra)+30, 12):
    for dec in range(int(zenith_dec)-30, int(zenith_dec)+30, 12):
        hp.projscatter(ra, dec, lonlat=True, color="red")
        hp.projtext(ra, dec, '({}, {})'.format(ra,dec), lonlat=True, color='red')

hp.graticule()

plt.savefig(os.path.join(plots, 'gnomom_view_Macon_likelihoodmap.png'), dpi=300)

#plt.show()


# In[29]:

likehood_cut=0.000001 #ut level for mask buildup

aligo_alert_map_high_like = np.logical_not(aligo_banana < likehood_cut)
map_lik_masked = hp.ma(aligo_banana)
map_lik_masked.mask = np.logical_not(aligo_alert_map_high_like)

hp.mollview(map_lik_masked.filled(),
            title='aLIGO aitoff map projection masked\n Likelihood > {}'.format(likehood_cut),
            unit='$\Delta$', fig=2)
hp.graticule()
hp.projscatter(mean_zenith_ra, zenith_dec
               , lonlat=True, color="red")
hp.projtext(mean_zenith_ra, zenith_dec,
            'Macon Zenith\n (mean position\n over the night)', lonlat=True, color="red")

#for ra in range(0,360,60):
#    for dec in range(-60,80,30):
#        if not (ra == 300 and dec == -30):
#            hp.projtext(ra,dec,'({}, {})'.format(ra,dec), lonlat=True, color='red')

plt.savefig(os.path.join(plots, 'allsky_likelihoodmap_masked.png'), dpi=300)
#plt.show()


# In[2]:

deg2rad = m.pi/180.

phis = list(sample['RA']*15.*deg2rad)
thetas = list(m.pi/2. - sample['Dec']*deg2rad)

def interp_filter(theta, phi):
    return hp.pixelfunc.get_interp_val(aligo_alert_map_high_like,
                                       theta, phi, nest=False)

def interp(theta, phi):
    return hp.pixelfunc.get_interp_val(aligo_banana,
                                       theta, phi, nest=False)

interps_filter = np.asarray(map(interp_filter, thetas, phis))

clipped = np.where(interps_filter > 0.2)

interps = np.asarray(map(interp, thetas, phis))

targets = sample[clipped[0]]

target_liks = interps[clipped[0]]

plt.hist(target_liks, log=True)
#plt.show()


# In[ ]:

targets['Likelihoods'] = target_liks


# In[ ]:

print len(targets)

plt.figure(figsize=(10,7))
plt.rcParams.update({"font.size":12})
plt.plot(targets['RA']*15.,targets['Dec'], "ro")
plt.plot(mean_zenith_ra, zenith_dec, 'bo')
plt.xlim(mean_zenith_ra-60, mean_zenith_ra+60)
plt.title("Selected targets near Macon zenith\n with likelihood > {}".format(likehood_cut))
plt.xlabel("RA[deg]")
plt.ylabel("Dec[deg]")
#plt.grid()
plt.savefig(os.path.join(plots, "selected_targets_Ra_dec.png"), dpi=300)
#plt.show()


# In[ ]:

plt.figure(figsize=(10,10))
plt.subplot(211, projection="mollweide")
deg2rad=m.pi/180.
j=0
tick_labels = np.array([150, 120, 90, 60, 30, 0, 330, 300, 270, 240, 210])
tick_labels = np.remainder(tick_labels+360,360)
for row in targets:
        x = np.remainder(row['RA']*15.+360,360) # shift RA values
        if x > 180.:
            x = x-360. # scale conversion to [-180, 180]
        x=-x    # reverse the scale: East to the left
        xg[j]=x*deg2rad
        yg[j]=row['Dec']*deg2rad
        #print gx[j], xg[j], yg[j]
        j=j+1

plt.plot(xg,yg, "r.")
plt.grid(True)
plt.xlabel("Rigth Ascention (degrees)")
plt.ylabel("Declination (degrees)")
plt.title("Aitoff projection of selected targets\n likelihood > {}".format(likehood_cut))
plt.savefig(os.path.join(plots,"aitoff_selected_targets.png"), dpi=300)
#plt.show()


# Uno puede ahora usar las galaxias (visibles) dentro de la mascara y rankearlas como mas le guste.
# Se pueden ordenar simplemente por Likehood por ejemplo, ahora dado que van a estar observando varios
# telescopios (quizas conviene acordar quien mira quien) y las mejoras de posteriores de las alertas
# cambian el negocio substancialmente ademas del input de nuestras mediciones

# In[ ]:

RAJ2015 = []
DecJ2015 = []
RA = []
Dec = []

for row in targets:
    coord=SkyCoord(ra=row['RA']*u.hourangle, dec=row['Dec']*u.degree, frame='icrs')
    precessed=coord.transform_to(FK5(equinox='J2015.11'))

    RAJ2015.append(precessed.to_string('hmsdms').split()[0])
    DecJ2015.append(precessed.to_string('hmsdms').split()[1])

    strcoord = coord.to_string('hmsdms')
    RA.append(strcoord.split()[0])
    Dec.append(strcoord.split()[1])
    #print i, coord.to_string('hmsdms'), targetLik[ind], targetMag[ind], RAJ2015[i], DecJ2015[i], name2[ind]


# In[ ]:

targets['RAJ2015'] = RAJ2015
targets['DecJ2015'] = DecJ2015
targets['RAJ2000'] = RA
targets['DecJ2000'] = Dec

targets.rename_column('App_Mag', 'AppMag')
targets.rename_column('Abs_Mag', 'AbsMag')
targets.rename_column('Maj_Diam_a', 'MajDiamA')
targets.rename_column('Min_Diam_b', 'MinDiamB')
targets.rename_column('err_Maj_Diam','ErrMajDiam')
targets.rename_column('err_Min_Diam','ErrMinDiam')
targets.rename_column('err_Dist', 'ErrDist')
targets.rename_column('err_App_Mag', 'ErrAppMag')
targets.rename_column('err_Abs_Mag', 'ErrAbsMag')
targets.rename_column('err_b/a', 'Errb/a')

targets.sort(['RAJ2000','Likelihoods'])


print "Max RA = {}, Min RA = {}".format(targets['RA'].max(), targets['RA'].min())


# I am going to calculate how many objects we will be able to visit, and assume that we have only capability to cover 2 objects per hour.
#
# After that the next step is to make fringe selections and rankings per fringe by Likelihood.

deltaRA = targets['RA'].max() - targets['RA'].min()

estimated_N_objects = deltaRA/0.5

print "The maximum number of objects visitable are {}".format(round(estimated_N_objects))


# So we choose the above number of objects to work.
#
# The idea will be to optimize the objects using as primary variable the likelihood, and as a second determiner the sky position.

#import link as ll
