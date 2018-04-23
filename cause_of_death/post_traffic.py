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
from datetime import datetime
import os

post_color = '#d63031'
gray_color = '#6f6f6f'
colors = ['#1f1f1f', '#0984e3']
mpl.rcParams['font.family'] = 'monospace'
mpl.rcParams['axes.prop_cycle'] = mpl.cycler(color=colors)

def normalize(s):
    return (s - s.min()) / (s.max() - s.min())

# Set output directory, make it if needed
output_dir = os.path.realpath('output')
if not os.path.isdir(output_dir):
    os.mkdir(output_dir)

# Get input data
input_file = os.path.join('data', 'dataisbeautiful_traffic.csv')
df = pd.read_csv(input_file, parse_dates=[1])
df = df[['day', 'subscribers', 'users_here']].set_index('day').set_axis(['subs', 'users'], axis='columns', inplace=False).loc['2018-04-16':'2018-04-18']
df['subs_n'] = normalize(df['subs'])
df['users_n'] = normalize(df['users'])

df['subs_d'] = normalize(np.gradient(df['subs']))
df['users_d'] = normalize(np.gradient(df['users']))


# Plot
fig, (ax1, ax2) = plt.subplots(nrows=2, 
                                 ncols=1, 
                                 sharex=True, 
                                 sharey=True, 
                                 figsize=(5,5), 
                                 dpi=300)
lw = 0.8
ax1.plot(df['users_n'], lw=lw)
ax1.plot(df['subs_n'], lw=lw)

ax2.plot(df['users_d'], lw=lw)
ax2.plot(df['subs_d'], lw=lw)

ax1.axvline(datetime(2018, 4, 17, 6), color=post_color, lw=lw, ls='--')
ax2.axvline(datetime(2018, 4, 17, 6), color=post_color, lw=lw, ls='--')
ax2.text(datetime(2018, 4, 17, 6), -0.11, 'Posted', rotation=90, size='x-small', color=post_color, ha='center', va='top')

ax1.tick_params(axis='both', which='major', labelsize='xx-small', labelcolor=gray_color, color=gray_color)
ax2.tick_params(axis='both', which='major', labelsize='xx-small', labelcolor=gray_color, color=gray_color)

plt.xticks(rotation=90)

ax2.xaxis.set_major_locator(mpl.dates.DayLocator())
ax2.xaxis.set_minor_locator(mpl.dates.HourLocator(byhour=[0,6,12,18]))

ax2.xaxis.set_major_formatter(mpl.dates.DateFormatter('%a'))

for side in ['right', 'left', 'top']:
    ax1.spines[side].set_visible(False)
    ax2.spines[side].set_visible(False)

ax1.text(min(df.index),0.84,'Number of \"Users Here\"', size='xx-small', color=colors[0], va='center')
ax1.text(min(df.index),0.76,'Number of \"Subscribers\"', size='xx-small', color=colors[1], va='center')

ax2.text(min(df.index),0.84,'Gradient of \"Users Here\"', size='xx-small', color=colors[0], va='center')
ax2.text(min(df.index),0.76,'Gradient of \"Subscribers\"', size='xx-small', color=colors[1], va='center')

ax1.text(datetime(2018, 4, 15, 14), 0.5, 'Normalized traffic', color=gray_color, size='xx-small', rotation=90, va='center', ha='center')
ax2.text(datetime(2018, 4, 15, 14), 0.5, 'Normalized traffic', color=gray_color, size='xx-small', rotation=90, va='center', ha='center')

# Annotations
ax1.text(min(df.index), 1.43, 'Popular Posts Bring Subreddit Subscribers')
ax1.text(min(df.index), 1.3, 'r/dataisbeautiful traffic during a popular post (Tue Apr 17)', size='x-small')

ax2.text(min(df.index), -0.6,
        'Traffic stats were scraped by a simple script for another project and\n' \
        'my Cause of Death post threw off the metrics. Data is normalized to the\n' \
        'max and min for each series for the given time range using y=(x-min)/(min-max)\n' \
        'The gradient plot shows the rate of change for each series.\n\n' \
        'Data and code: www.github.com/aaronpenne\n' \
        'Twitter: @aaronpenne\n' \
        'Aaron Penne © 2018\n\n',
        fontsize = 'xx-small',
        color = gray_color,
        va='top',
        multialignment = 'left')

fig.savefig(os.path.join(output_dir, 'traffic.png'),
            dpi=fig.dpi,
            bbox_inches='tight',
            pad_inches=0.3)
plt.close(fig)
