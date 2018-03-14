# -*- coding: utf-8 -*-
"""


"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

min_mag = -20
max_mag = 8
steps = 40

# Set output directory, make it if needed
output_dir = os.path.relpath(r'output')  # Windows machine
if not os.path.isdir(output_dir):
    os.mkdir(output_dir)

# Get input file
input_file = os.path.relpath(r'data\hygdata_v3.csv')
df = pd.read_csv(input_file)

# Only use stars visible to the human eyeish and ignore the sun
df = df[df.mag > min_mag]
df = df[df.mag < max_mag]

#df = df[df.ra > 10]
#df = df[df.ra < 0.1]
##
#df = df[df.dec > -78]
#df = df[df.dec < -76]

# Filter the size/alpha of each magnitude bin (log scale)
mag = {}
for i,value in enumerate(np.geomspace(abs(min_mag)+max_mag, abs(min_mag), num=steps)):
    mag[i] = df['mag'] >= (value + min_mag)
marker = {}
for i,value in enumerate(np.geomspace(4, 0.0001, num=steps)):
    marker[i] = value
alpha = {}
for i,value in enumerate(np.geomspace(80, 10, num=steps)):
    alpha[i] = value








# FIXME left off here
mag_xor = {}
for i in range(len(mag)):
    if i == len(mag)-1:
        mag_xor[i] = mag[i]
        break
    mag_xor[i] = mag[i] & (mag[i] ^ mag[i+1])

mag = mag_xor





    
# Set up plot size
fig, ax = plt.subplots(figsize=(10, 5), dpi=500)

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

# Despine plot
for side in ['right', 'left', 'top', 'bottom']:
    ax.spines[side].set_visible(False)
    
# Clear axis ticks/labels
ax.xaxis.set_ticks([])
ax.yaxis.set_ticks([])

# Set max/min axis limits
plt.ylim([-90, 90])
plt.xlim([0, 24])

# Show plot
plt.show()

# Save plot
fig.savefig(os.path.join(output_dir, 'hyg_scatter.png'),
            dpi=fig.dpi,
            facecolor=fig.get_facecolor(),
            edgecolor='none',
            bbox_inches='tight',
            pad_inches=0.3)