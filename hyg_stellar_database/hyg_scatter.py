# -*- coding: utf-8 -*-
"""


"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

min_mag = -20
max_mag = 20
vis_mag = 8
steps = 40

# Set output directory, make it if needed
output_dir = os.path.relpath(r'output')  # Windows machine
if not os.path.isdir(output_dir):
    os.mkdir(output_dir)

# Get input file
input_file = os.path.relpath(r'data\hygdata_v3.csv')
df = pd.read_csv(input_file)

# Filter to certain magnitudes, ignore the sun
df = df[df.mag > min_mag]
df = df[df.mag < max_mag]

# Filter the size/alpha of each marker by magnitude bin (log scale)
mag = {}
for i,value in enumerate(np.geomspace(abs(min_mag), abs(min_mag)+max_mag, num=steps)):
    mag[i] = (df['mag'] >= (value + min_mag)) & (df['mag'] < vis_mag)
marker = {}
for i,value in enumerate(np.geomspace(4, 0.1, num=steps)):
    marker[i] = value
alpha = {}
for i,value in enumerate(np.geomspace(1, 0.4, num=steps)):
    alpha[i] = value
    


# Workaround to get each magnitude bin only plotted once
mag_xor = {}
for i in range(len(mag)):
    if i == len(mag)-1:
        mag_xor[i] = mag[i]
        break
    mag_xor[i] = mag[i] & (mag[i] ^ mag[i+1])
mag = mag_xor


# Set up plot
fig, ax = plt.subplots(figsize=(10, 5), dpi=300)

# Black out the entire background
fig.set_facecolor('black')
ax.set_facecolor('black')

# Plot each star, differing parameters depending on magnitude
for i in range(steps):
    x = df.loc[mag[i], 'ra']
    y = df.loc[mag[i], 'dec']
    plt.plot(x, y, 
             color='white', 
             linestyle='none',
             linewidth=0,
             marker='.', 
             markersize=marker[i],
             alpha=alpha[i],
             markeredgewidth=0)

## Why not make constellations pop? Doesn't look as good
#x = df.loc[df['bf'].notnull(), 'ra']
#y = df.loc[df['bf'].notnull(), 'dec']
#plt.plot(x, y, 
#         color='white', 
#         linestyle='none',
#         linewidth=0,
#         marker='.', 
#         markersize=5,
#         alpha=1,
#         markeredgewidth=0)

# Despine plot
for side in ['right', 'left', 'top', 'bottom']:
    ax.spines[side].set_visible(False)
    
# Set axis ticks/labels
plt.xticks(np.linspace(0, 24, 5), 
           family='monospace',
           size=5,
           color='white', 
           alpha=0.15)
plt.yticks(np.linspace(-90, 90, 5),
           family='monospace',
           size=5,
           color='white', 
           alpha=0.15)
plt.text(0, -105,
         'Right Ascension (hours)',
         family='monospace',
         size=5,
         color='white', 
         alpha=0.15,
         horizontalalignment='left')
plt.text(-1.2, -51,
         'Declination (degrees)',
         family='monospace',
         size=5,
         color='white', 
         alpha=0.15,
         horizontalalignment='left',
         rotation='vertical')

# Set max/min axis limits
plt.ylim([-90, 90])
plt.xlim([0, 24])

# Add text
plt.text(0, 115, 'The Night Sky',
         family='monospace',
         size=14,
         horizontalalignment='left',
         weight='bold',
         color='white',
         alpha=0.7)
plt.text(0, 110, 'Equirectangular projection of stars (mag<8)'.format(vis_mag),
         family='monospace',
         size=9,
         horizontalalignment='left',
         verticalalignment='top',
         weight='bold',
         color='white',
         alpha=0.7)
plt.text(24, -120, '© 2018 Aaron Penne\nData: HYG Stellar Database\n\nApparent magnitude scale is logarithmic\nBrighter stars have a smaller apparent magnitude',
         family='monospace',
         size=7,
         horizontalalignment='right',
         verticalalignment='top',
         weight='bold',
         color='white',
         alpha=0.7)


# Show plot
plt.show()

# Save plot
fig.savefig(os.path.join(output_dir, 'hyg_scatter.png'),
            dpi=fig.dpi,
            facecolor=fig.get_facecolor(),
            edgecolor='none',
            bbox_inches='tight',
            pad_inches=0.5)


# FIXME twinkle time