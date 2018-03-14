# -*- coding: utf-8 -*-
"""


"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

steps = 20

# Set output directory, make it if needed
output_dir = os.path.relpath(r'output')  # Windows machine
if not os.path.isdir(output_dir):
    os.mkdir(output_dir)

# Get input data
input_file = os.path.relpath(r'data\hygdata_v3.csv')
df = pd.read_csv(input_file)

# Excluding Sol, magnitude range is -2:22
# Try even split
data = {}
for i,mag in enumerate(np.linspace(-2, 22, num=steps)):
    data[i] = df['mag'] >= mag

marker = {}
for i,value in enumerate(np.linspace(0.01, 1, num=steps)):
    marker[steps-i-1] = value
    
alpha = {}
for i,value in enumerate(np.linspace(5, 100, num=steps)):
    alpha[steps-i-1] = value
    


fig, ax = plt.subplots(figsize=(10, 5), dpi=500)

ax.set_facecolor('black')

for i in range(steps):
    x = df.loc[data[i], 'ra']
    y = df.loc[data[i], 'dec']
    plt.plot(x, y, 
             color='white', 
             linestyle='none',
             linewidth=0,
             marker='.', 
             markersize=marker[i],
             alpha=alpha[i])

# Despine
for side in ['right', 'left', 'top', 'bottom']:
    ax.spines[side].set_visible(False)
#    
#plt.xticks('')
#plt.yticks('')

plt.show()

fig.savefig(os.path.join(output_dir, 'hyg_scatter.png'),
            dpi=fig.dpi,
            bbox_inches='tight',
            pad_inches=0.3)