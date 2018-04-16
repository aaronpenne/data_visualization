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

color_gray = ['#3f3f3f', '#6f6f6f']
mpl.rcParams['font.family'] = 'monospace'
mpl.rcParams['axes.prop_cycle'] = mpl.cycler(color=color_gray)

def normalize(s, n):
    delta = n - sum(s)
    spread = delta / len(s)
    return s + spread

def label_bar(rects, text, weight='normal'):
    for rect in rects:
        height = rect.get_height()
        width = rect.get_width()
        x = rect.get_x()
        y = rect.get_y()
        if height > 0.023:
            ax.text(x + width/2.0, y + height/2.0, text, ha='center', va='center', color='w', size='small', weight=weight)
        
# Set output directory, make it if needed
output_dir = os.path.realpath('output')  # Windows machine
if not os.path.isdir(output_dir):
    os.mkdir(output_dir)

# Get input data
input_file = os.path.join('data', 'cod_rates.csv')
df = pd.read_csv(input_file)

# Get media average
df['media'] = (df['guardian'] + df['nyt'])/2
df = df.drop(columns=['guardian', 'nyt'])

# Normalize to 1 as sum
df['cdc'] = normalize(df['cdc'], 1)
df['google'] = normalize(df['google'], 1)
df['media'] = normalize(df['media'], 1)

# Add repeat column to loop smoothly
df['cdc2'] = df['cdc']

df = df.sort_values('cdc')
df = df.set_index('cod')

## Add NaN columns to increase viz resolution
for res in range(3):
    df_columns = list(df)
    for i in range(1, 2*len(df_columns)-1, 2):
        df.insert(i, df.columns[i-1],
                  float('nan'),
                  allow_duplicates=True)
    # Interpolate between columns and replace NaNs, [2, NaN, 3] becomes [2, 2.5, 3]
    df = df.interpolate(axis=1)
df = df.drop(columns='cdc2')

for i, col in enumerate(df.columns):
    fig, ax = plt.subplots(figsize=(4, 6), dpi=150)
    width = 1
    top = 0
    for j, row in enumerate(df.index):
        value = df.iloc[j, i]
        rect = ax.bar(0, value, width, bottom=top, edgecolor='white', linewidth=0.3)
        top += value
        label_bar(rect, row.title().replace('_', ' '))

    if i in range(0,8):
        ax.text(0, 1.1, 'CDC Cause of Death in USA', ha='center', va='center', fontsize='large')
        ax.text(0, 1.05, '\"What actually causes death?\"', ha='center', va='center', fontsize='medium')
    elif i in range(8,16):
        ax.text(0, 1.1, 'Google Search Trends', ha='center', va='center', fontsize='large')
        ax.text(0, 1.05, '\"Which causes do we worry about?\"', ha='center', va='center', fontsize='medium')
    elif i in range(16,24):
        ax.text(0, 1.1, 'NYT & Guardian Headlines', ha='center', va='center', fontsize='large')
        ax.text(0, 1.05, '\"Which causes are in the media?\"', ha='center', va='center', fontsize='medium')
    else:
        ax.text(0, 1.1, ' ', ha='center', va='center', fontsize='large')
        ax.text(0, 1.05, ' ', ha='center', va='center', fontsize='medium')
        
    # Deal with axis
    ytick_vals = np.linspace(0,1,21)
    ax.tick_params(axis='y', colors=color_gray[1])
    plt.yticks(ytick_vals, ['{:.0f}%'.format(x*100) for x in ytick_vals], 
                            fontsize='xx-small', 
                            weight='light',
                            color=color_gray[1])
    plt.xticks([])
    for side in ['right', 'left', 'top', 'bottom']:
        ax.spines[side].set_visible(False)
        
    # Annotations
    ax.text(-0.5, -0.18,
            'Data: CDC, Google, New York Times, The Guardian\n' \
            'Code: www.github.com\\aaronpenne\n' \
            'Twitter: @aaronpenne\n' \
            'Aaron Penne © 2018\n\n' \
            'Based on in-depth analysis by H. Al-Jamaly, M. Siemers,\n' \
            'O. Shen, and N. Stone at owenshen24.github.io/charting-death',
            fontsize = 'xx-small',
            color = color_gray[1],
            multialignment = 'left')

    fig.savefig(os.path.join(output_dir, 'bar_{:02}.png'.format(i)),
                dpi=fig.dpi,
                bbox_inches='tight',
                pad_inches=0.3)
    plt.close(fig)


# Make gif
png_files = [f for f in os.listdir(output_dir) if f.endswith('.png')]
png_files.sort()

charts = []
for i, f in enumerate(png_files):
    charts.append(imageio.imread(os.path.join(output_dir, f)))
    # Append the actual charts extra to 'pause' the gif
    if i in [0, 8, 16]:
        for j in range(30):
            charts.append(imageio.imread(os.path.join(output_dir, f)))

# Save gif
imageio.mimsave(os.path.join(output_dir, 'bar.gif'), charts, format='GIF', duration=0.09)
