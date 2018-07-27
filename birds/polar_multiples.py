# -*- coding: utf-8 -*-
"""
DataIsBeautiful July 2018

Crazy birds
"""

import numpy as np
import pandas as pd
from statsmodels.graphics.mosaicplot import mosaic
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['font.family'] = 'monospace'

## Feeder info
#df_feed = pd.read_csv('feeder_seeds.csv')
#seeds = df_feed['seeds']
#df_feed.drop(columns='seeds', inplace=True)
#df_feed.apply(pd.to_numeric)
#max_feed = df_feed.max().max()
#min_feed = df_feed.min().min()

# Bird info
df_bird = pd.read_csv('birds_seeds.csv')
birds = df_bird['birds']
df_bird.drop(columns='birds', inplace=True)
seeds = df_bird.columns.tolist()
df_bird.apply(pd.to_numeric)
max_bird = df_bird.max().max()
min_bird = df_bird.min().min()

color_sat = ['#a6cee3','#1f78b4','#b2df8a','#fdbf6f','#33a02c','#fb9a99','#ff1a62','#ff7f00','#cab2d6']
color_pale = ['#8dd3c7','#ffffb3','#bebada','#fb8072','#80b1d3','#fdb462','#b3de69','#fccde5','#d9d9d9']
color_grey = '#5F5F5F'

## Feeder and Seeds
#bottom = 3
#rows = 3
#cols = 3
#fig, axes = plt.subplots(rows, cols, subplot_kw={'projection':'polar'}, figsize=(8,8), dpi=100)
#i = 0
#for row in range(0,rows):
#    for col in range(0,cols):
#        ax = axes[row, col]
#        
#        N = 6
#        step = 2*np.pi/N
#        theta = np.arange(0.0, 2*np.pi, step)
#        radii = df_feed.iloc[i,:].tolist() # Y data here
#
#        bars = ax.bar(theta, radii, width=0.7*step, bottom=bottom, color=color_sat)
#        
#        ax.set_title('Axis [{},{}]'.format(row, col))
#        ax.set_yticks(np.arange(min_feed, max_feed, 5))
#        ax.set_xticklabels([])
#        ax.set_yticklabels([])
#        ax.grid(color='#FFFFFF', linestyle='-', linewidth=1, axis='y', alpha=0.4)
#        ax.grid(linewidth=0, axis='x')
##        for s in ax.spines:
##            print(s)
#        ax.spines['polar'].set_visible(False)
#        
#        # Counter
#        i += 1
#fig.subplots_adjust(hspace=0.3)


# Birds and Seeds POLAR
title_dict = {'fontsize':'small', 'color':'#5F5F5F'}
handles = {}
bottom = 0
rows = 4
cols = 4
fig, axes = plt.subplots(rows, cols, subplot_kw={'projection':'polar'}, figsize=(8,8), dpi=300)
i = 0
for row in range(0,rows):
    for col in range(0,cols):
        ax = axes[row, col]
        
        N = 9
        step = 2*np.pi/N
        theta = np.arange(0.0, 2*np.pi, step)
        if i < 15:
            radii = df_bird.iloc[i,:].tolist() # Y data here
            bars = ax.bar(theta, radii, width=0.7*step, bottom=bottom)
            for index in range(0, N):
                bars[index].set_color(color_sat[index])
            ax.set_title(birds[i].title(), fontdict=title_dict)
            alpha=0.4
        else:
            ax.set_title('Legend', fontdict=title_dict)
            alpha=0
        ax.set_ylim(min_bird, max_bird)
        ax.set_xticklabels([])
        if i == 0:            
            ax.tick_params(axis='y', direction='out', which='both')
            ax.set_yticks([0, 1, 2, 3, 4])
            ax.set_yticklabels(['', 1, 2, 3, 4], fontdict={'fontsize':'xx-small', 'color':color_grey})
            ax.set_rlabel_position(220)
        else:
            ax.set_yticks(np.arange(min_bird, max_bird+1, 1))
            ax.set_yticklabels([])
        ax.grid(color=color_grey, linestyle='-', linewidth=1, axis='y', alpha=alpha)
        ax.grid(linewidth=0, axis='x')
#        for s in ax.spines:
#            print(s)
        ax.spines['polar'].set_visible(False)
        ax.set_axisbelow(True)
        
        # Counter
        i += 1
fig.subplots_adjust(hspace=0.3)

# Legend
for i, color in enumerate(color_sat):
    label_dict = {'color':color, 'fontsize':'xx-small', 'ha':'center'}
                  
    if i < len(color_sat)/2:
        x = np.pi/2
        y = max_bird-(i*(max_bird*2)/len(color_sat))
        plt.text(x, y, seeds[i].title(), fontdict=label_dict)
        
    elif i == len(color_sat)/2:
       plt.text(0, 0, seeds[i].title(), fontdict=label_dict)
       
    else:
        x = 3*np.pi/2
        y = min_bird+((i-len(color_sat)/2)*(max_bird*2)/len(color_sat))
        plt.text(x, y, seeds[i].title(), fontdict=label_dict)
        
# Fig subtitle
label_dict = {'color':color_grey, 'fontsize':'x-small', 'ha':'left'}
plt.text(0.12, 0.95, 'High=4, Med=2, Low=1', 
         fontdict=label_dict,
         transform=plt.gcf().transFigure)        

# Fig title
plt.suptitle('Seed Preferences of Birds\nNear Chagrin Falls, Ohio', x=0.12, y=1.01,
             ha='left',
             va='top')

# Fig annotations
plt.text(0.88, 1.01,
        'Data: DataIsBeautiful Contest July 2018\n' \
        'Code: www.github.com/aaronpenne\n' \
        '@aaronpenne © 2018',
        fontsize = 'xx-small',
        color = color_grey,
        ha='right',
        va='top',
        multialignment = 'right',
        transform=plt.gcf().transFigure)

fig.savefig('birdseed.png', dpi=fig.dpi, bbox_inches='tight')

#
#
## Birds and Seeds BAR
#bottom = 0
#rows = 4
#cols = 4
#fig, axes = plt.subplots(rows, cols, figsize=(8,8), dpi=200)
#i = 0
#for row in range(0,rows):
#    for col in range(0,cols):
#        ax = axes[row, col]
#        
#        theta = np.arange(0.0, 2*np.pi, step)
#        if i < 15:
#            x = np.arange(0, len(df_bird.iloc[0]), 1)
#            y = df_bird.iloc[i,:].tolist() # Y data here
#    
#            bars = ax.bar(x, y, width=0.7, bottom=bottom, color=color_sat)
#        
#            ax.set_title(birds[i])
#        ax.set_yticks(np.arange(min_bird, max_bird, 1))
#        ax.set_xticklabels([])
#        ax.set_yticklabels([])
#        ax.grid(color='#FFFFFF', linestyle='-', linewidth=1, axis='y', alpha=0.4)
#        ax.grid(linewidth=0, axis='x')
#        for s in ax.spines:
#            ax.spines[s].set_visible(False)
#        
#        # Counter
#        i += 1
#        
#
## Mosaic (just aint working)
#df_original = pd.read_csv('original.csv')
#fig, ax = plt.subplots(figsize=(8,8), dpi=200)
#mosaic(df, ['birds', 'seeds'],  ax=ax, statistic=True)
#
#df = df_original[df_original['amount']!=0]
#for i in range(2, 1+df['amount'].max()):
#    df = df.append([df[df['amount']==i]]*i, ignore_index=True)
#len(df_original['amount'])
