# -*- coding: utf-8 -*-
"""
Quick chart based on https://owenshen24.github.io/charting-death/

Author: Aaron Penne
Created: 2018-04-15

Developed with:
    Python 3.6
    macOS 10.13
""" 

import pandas as pd
import matplotlib.pyplot as plt
import imageio
import os

plt.rcParams['image.cmap'] = 'Set2'

def normalize(s, n):
    return s*(n-sum(s))+s

def label_bar(rects, text):
    for rect in rects:
        height = rect.get_height()
        width = rect.get_width()
        x = rect.get_x()
        y = rect.get_y() 
        ax.text(x + width/2.0, y + height/2.0, text, ha='center', va='center', color='w')

# Set output directory, make it if needed
output_dir = os.path.realpath('output')  # Windows machine
if not os.path.isdir(output_dir):
    os.mkdir(output_dir)

# Get input data
input_file = os.path.join('data', 'cod_rates.csv')
df = pd.read_csv(input_file)

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

# FIXME title slide?

for i, col in enumerate(df.columns):
    fig, ax = plt.subplots(figsize=(4, 6), dpi=150)
    width = 1
    top = 0
    for j, row in enumerate(df.index):
        value = df.iloc[j, i]
        rect = ax.bar(0, value, width, bottom=top)
        top += value
        if row in ['heart_disease', 'kidney_disease', 'cancer', 'suicide', 'terrorism', 'homicide', 'diabetes', 'car_accident']:
            label_bar(rect, row.title().replace('_', ' '))  
    if i == 0:
        plt.title('CDC Causes of Death\nWhat actually kills us')
    elif i == 8:
        plt.title('Google Search Trends\nWhat we are worried about')
    elif i == 16:
        plt.title('NYT & Guardian Headlines\nWhat the media talks about')
    else:
        plt.title(' \n ')
    plt.axis('off')
    fig.savefig(os.path.join(output_dir, 'bar_{:02}.png'.format(i)),
                dpi=fig.dpi,
                bbox_inches='tight',
                pad_inches=0.3)
    plt.close(fig)


# Make gif
png_files = [f for f in os.listdir(output_dir) if f.endswith('.png')]
png_files.sort()

charts = []
# Append the title chart - https://stackoverflow.com/a/35943809
#for i in range(30):
#    charts.append(imageio.imread('{0}999.png'.format(output_dir)))

# Append all the charts (except the title slide)
for i, f in enumerate(png_files):
    charts.append(imageio.imread(os.path.join(output_dir, f)))
    if i in [0, 8, 16]:
        for j in range(25):
            charts.append(imageio.imread(os.path.join(output_dir, f)))

# Save gif
imageio.mimsave(os.path.join(output_dir, 'bar.gif'), charts, format='GIF', duration=0.1)
