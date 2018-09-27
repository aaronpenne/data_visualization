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
import os
import sys
from PIL import Image

color_gray = ['#3f3f3f', '#6f6f6f']
mpl.rcParams['font.family'] = 'monospace'
#mpl.rcParams['axes.prop_cycle'] = mpl.cycler(color=color_gray)
#plt.rcParams["image.cmap"] = 'Pastel1'
plt.rcParams['axes.prop_cycle'] = plt.cycler(color=plt.cm.tab20b.colors)

def normalize(s, n):
    delta = n - sum(s)
    spread = delta / len(s)
    return s + spread

def label_bar(rects, text, weight='normal', color='#3f3f3f'):
    for rect in rects:
        height = rect.get_height()
        width = rect.get_width()
        x = rect.get_x()
        y = rect.get_y()
#        if text in ['Heart Disease', 'Overdose', 'Homicide', 'Terrorism']:
#            ax.text(x + width/2.0, y + height/2.0 - 0.002, text, ha='center', va='center', color='#dcdccc', size='x-small', weight=weight)
#        else:
#            ax.text(x + width/2.0, y + height/2.0 - 0.002, text, ha='center', va='center', color='#3f3f3f', size='x-small', weight=weight)
        ax.text(x + width/2.0, y + height/2.0 - 0.002, text, ha='center', va='center', color='k', size='x-small', weight=weight)

            
# Set output directory, make it if needed
output_dir = os.path.realpath('output')
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

df = df.sort_values('cdc')
df = df.set_index('cod')


for i, col in enumerate(df.columns):
    fig, ax = plt.subplots(figsize=(2.5, 6), dpi=700)
    
    width = 1
    top = 0
    for j, row in enumerate(df.index):
        value = df.iloc[j, i]
        rect = ax.bar(0, value, width, bottom=top, edgecolor='k', linewidth=0.3, alpha=0.7, clip_on=False)
        top += value
        if (i == 0) & ~(row in ['homicide', 'terrorism']):
            label_bar(rect, row.title().replace('_', ' '))
        elif (i == 1) & ~(row in ['kidney_disease']):
            label_bar(rect, row.title().replace('_', ' '))
        elif (i == 2) & ~(row in ['lower_respiratory_disease', 'alzheimers', 'kidney_disease', 'overdose']):
            label_bar(rect, row.title().replace('_', ' '))

    if i == 0:
        ax.text(0, 1.1, 'CDC Cause of Death in USA', ha='center', va='center', fontsize='small')
        ax.text(0, 1.05, '\"What actually causes death?\"', ha='center', va='center', fontsize='x-small')
    elif i == 1:
        ax.text(0, 1.1, 'Google Search Trends', ha='center', va='center', fontsize='small')
        ax.text(0, 1.05, '\"Which causes do we worry about?\"', ha='center', va='center', fontsize='x-small')
    elif i == 2:
        ax.text(0, 1.1, 'NYT & Guardian Headlines', ha='center', va='center', fontsize='small')
        ax.text(0, 1.05, '\"Which causes are in the media?\"', ha='center', va='center', fontsize='x-small')
    else:
        ax.text(0, 1.1, ' ', ha='center', va='center', fontsize='small')
        ax.text(0, 1.05, ' ', ha='center', va='center', fontsize='x-small')
        
    # Deal with axis
    ytick_vals = np.linspace(0,1,21)
    ax.grid(False)
    ax.tick_params(axis='y', colors=color_gray[1])
    plt.yticks(ytick_vals, ['{:.0f}%'.format(x*100) for x in ytick_vals], 
                            fontsize='xx-small', 
                            weight='light',
                            color=color_gray[1])
    plt.xticks([])
    for side in ['right', 'left', 'top', 'bottom']:
        ax.spines[side].set_visible(False)
        
    fig.savefig(os.path.join(output_dir, 'bar_{:02}.png'.format(i)),
                dpi=fig.dpi,
                bbox_inches='tight',
                pad_inches=0.3)
    plt.close(fig)





def append_images(images, direction='horizontal',
                  bg_color=(255,255,255), aligment='center'):
    """
    Appends images in horizontal/vertical direction.

    Args:
        images: List of PIL images
        direction: direction of concatenation, 'horizontal' or 'vertical'
        bg_color: Background color (default: white)
        aligment: alignment mode if images need padding;
           'left', 'right', 'top', 'bottom', or 'center'

    Returns:
        Concatenated image as a new PIL image object.
    """
    widths, heights = zip(*(i.size for i in images))

    if direction=='horizontal':
        new_width = sum(widths)
        new_height = max(heights)
    else:
        new_width = max(widths)
        new_height = sum(heights)

    new_im = Image.new('RGB', (new_width, new_height), color=bg_color)


    offset = 0
    for im in images:
        if direction=='horizontal':
            y = 0
            if aligment == 'center':
                y = int((new_height - im.size[1])/2)
            elif aligment == 'bottom':
                y = new_height - im.size[1]
            new_im.paste(im, (offset, y))
            offset += im.size[0]
        else:
            x = 0
            if aligment == 'center':
                x = int((new_width - im.size[0])/2)
            elif aligment == 'right':
                x = new_width - im.size[0]
            new_im.paste(im, (x, offset))
            offset += im.size[1]

    return new_im


images = map(Image.open, [os.path.join('output','bar_00.png'), os.path.join('output','bar_01.png'), os.path.join('output','bar_02.png')])
all_images = append_images(images)
all_images.save('test.png')