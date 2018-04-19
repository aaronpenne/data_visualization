# -*- coding: utf-8 -*-
"""
Quick chart based on https://owenshen24.github.io/charting-death/

Author: Aaron Penne
Created: 2018-04-15

Developed with:
    Python 3.6
    macOS 10.13
""" 

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import imageio
import os

mpl.rcParams['font.family'] = 'monospace'

# Set output directory, make it if needed
output_dir = os.path.realpath('output')
if not os.path.isdir(output_dir):
    os.mkdir(output_dir)

# Get input data
input_file = os.path.join('data', 'cod_rates.csv')
df = pd.read_csv(input_file)

# Get delta between CDC rate and others
df['delta_google'] = df['google'] - df['cdc']
df['delta_nyt'] = df['nyt'] - df['cdc']
df['ratio_nyt_to_google'] = df['nyt'] / df['cdc']

df = df.set_index('cod')

# Plot
fig, ax = plt.subplots(figsize=(4,6), dpi=150)

# Vert/Horizontal lines
ax.plot([0, 0], [df.loc['heart_disease', 'delta_nyt'], df.loc['terrorism', 'delta_nyt']])

# Scatter
y = df['delta_nyt']
x = [0]*len(y)
ax.scatter(x, y, s=170, marker='s', c='white', edgecolor='white', zorder=3)

# Label the points
for cod in df.index:
    ax.text(0.15, df.loc[cod, 'delta_nyt'], cod.title().replace('_', ' '), va='center')
    ax.text(0.137, df.loc[cod, 'delta_nyt'], '{:.01f}%'.format(df.loc[cod, 'delta_nyt']*100), va='center', ha='right')



plt.xlim([-1,1])
plt.axis('off')


# Annotations
ax.text(-0.5, -0.4,
        'Data: CDC, Google, New York Times, The Guardian\n' \
        'Code: www.github.com\\aaronpenne\n' \
        'Twitter: @aaronpenne\n' \
        'Aaron Penne © 2018\n\n' \
        'Based on in-depth analysis by H. Al-Jamaly, M. Siemers,\n' \
        'O. Shen, and N. Stone at owenshen24.github.io/charting-death',
        fontsize = 'xx-small',
        color = color_gray[1],
        multialignment = 'left')

fig.savefig(os.path.join(output_dir, 'delta_cod.png'),
            dpi=fig.dpi,
            bbox_inches='tight',
            pad_inches=0.3)
plt.close(fig)
