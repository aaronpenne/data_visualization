#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Redrawing the exploded 3D pie chart from https://www.reddit.com/r/dataisbeautiful/comments/8fyp73/religion_of_nobel_prize_winners_between_1901_and/

Author: Aaron Penne
Created: 2018-04-30

Developed with:
    Python 3.6
    macOS 10.13
"""

import os
import pandas as pd
from PIL import Image

import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['font.family'] = 'monospace'


def resize_image(width, img):
    img = Image.open(img)
    wpct = (width/float(img.size[0]))
    height = int((float(img.size[1])*float(wpct)))
    img = img.resize((width, height), Image.ANTIALIAS)
    img.save(img)

###############################################################################
# Set up directories
code_dir = os.path.dirname(__file__)
data_dir = os.path.join(code_dir, 'data') 
output_dir = os.path.join(code_dir, 'output')
if not os.path.isdir(output_dir):
    os.mkdir(output_dir)
    
###############################################################################
# Wrangle and process data
    
# Get input data
input_file = os.path.join(data_dir, 'nobel_pop_data.csv')
df = pd.read_csv(input_file)    

df.sort_values(by=['pct_pop'], ascending=True, inplace=True)
df.reset_index(inplace=True, drop=True)
    
###############################################################################
# Create visualization
color = '#3f3f3f'

# Make core plot
dpi = 300
fig, ax = plt.subplots(figsize=(800/dpi, 500/dpi), 
                       dpi=1000,
                       ncols=2,
                       sharey=True)
ax[0].barh(df.index, df['pct_pop'], align='center', color=color)
ax[1].barh(df.index, df['pct_nobel'], align='center', color=color)

# Aesthetics
plt.subplots_adjust(wspace=0.6)
ax[0].set_xlim(80,0)
ax[1].set_xlim(0,80)
ax[0].axis('off')
ax[1].axis('off')

# Labels
fontdict = {'va': 'center',
            'size': 4,
            'color': 'gray'}
pad = 5
center = -25
for i,x in enumerate(df['pct_pop']):
    ax[0].text(x + pad, i,
               '{:0.1f}%'.format(x),
               fontdict=fontdict,
               ha='right')
for i,x in enumerate(df['pct_nobel']):
    ax[1].text(x + pad, i,
               '{:0.1f}%'.format(x),
               fontdict=fontdict,
               ha='left')
for i,x in enumerate(df['religion']):
    ax[1].text(center, i,
               x.title(),
               fontdict=fontdict,
               ha='center',
               color=color)

# Title and annotations
ax[0].text(center, 7.5,
        'Religion of Nobel Prize Winners 1901-2000',
        va='bottom',
        ha='center',
        color=color,
        size=7,
        multialignment = 'center')
ax[0].text(0, 6.7,
           'Global Population',
           fontdict=fontdict,
           ha='right')
ax[1].text(0, 6.7,
           'Nobel Prize Winners',
           fontdict=fontdict,
           ha='left')
ax[1].text(center, -1.3,
        'Data: "100 Years of Nobel Prizes" & Wikipedia\n' \
        'Code: www.github.com/aaronpenne\n' \
        '@aaronpenne © 2018',
        fontdict=fontdict,
        va='top',
        ha='center',
        multialignment = 'center')

# Save figure    
fig_name = 'nobel_pop_bar.png'
fig.savefig(os.path.join(output_dir, fig_name),
        dpi=fig.dpi,
        bbox_inches='tight',
        pad_inches=0.3)
plt.close(fig)

