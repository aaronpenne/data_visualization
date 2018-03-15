# -*- coding: utf-8 -*-
"""


"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

min_mag = -20
max_mag = 20
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
for i,value in enumerate(np.geomspace(abs(min_mag)+max_mag, abs(min_mag), num=steps)):
    mag[i] = df['mag'] <= (value + min_mag)
marker = {}
for i,value in enumerate(np.geomspace(3, 0.1, num=steps)):
    marker[i] = value
alpha = {}
for i,value in enumerate(np.geomspace(1, 0.3, num=steps)):
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

## Why not make constellations pop?
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
    
# Clear axis ticks/labels
ax.xaxis.set_ticks([])
ax.yaxis.set_ticks([])

# Set max/min axis limits
plt.ylim([-90, 90])
plt.xlim([0, 24])

# Add text
plt.text(0, 111, 'The Night Sky',
         family='monospace',
         size=10,
         horizontalalignment='left',
         weight='bold',
         color='white',
         alpha=0.6)
plt.text(0, 105, 'Right Ascension vs. Declination',
         family='monospace',
         size=7,
         horizontalalignment='left',
         weight='bold',
         color='white',
         alpha=0.6)
plt.text(24, -111, '© 2018 Aaron Penne\nData: HYG Stellar Database',
         family='monospace',
         size=7,
         horizontalalignment='right',
         weight='bold',
         color='white',
         alpha=0.6)


# Show plot
plt.show()

# Save plot
fig.savefig(os.path.join(output_dir, 'hyg_scatter.png'),
            dpi=fig.dpi,
            facecolor=fig.get_facecolor(),
            edgecolor='none',
            bbox_inches='tight',
            pad_inches=0.7)