#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  8 13:12:03 2022

@author: davidpamosortega
"""

import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

file = 'data_astro5.csv'

df = pd.read_csv(file,sep=',')
df[r'B ($\mu$T)'] = np.sqrt(df['B_x']**2 + df['B_y']**2 + df['B_z']**2)

df.head()

fig, ax = plt.subplots(figsize=(15,10))

countries = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
countries.plot(color="lightgrey", ax=ax)

df.plot(x="Longitude (deg)", y="Latitude (deg)", kind="scatter", c=r'B ($\mu$T)', colormap="YlOrRd", ax=ax)
ax.grid(b=True, alpha=0.5)
plt.title('The magnetic field measured by ISS (April 30, 2022)', fontsize = 20)
plt.xlabel('Longitude (deg)',fontsize=20)
plt.ylabel('Latitude (deg)',fontsize=20)
plt.show()

fig.savefig('mag_earth.png')