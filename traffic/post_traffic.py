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
from datetime import datetime, timedelta
import os

post_color = '#d63031'
gray_color = '#6f6f6f'
colors = ['#1f1f1f', '#0984e3']
mpl.rcParams['font.family'] = 'monospace'
mpl.rcParams['axes.prop_cycle'] = mpl.cycler(color=colors)

def normalize(s):
    return (s - s.min()) / (s.max() - s.min())

# Set output directory, make it if needed
code_dir = os.path.dirname(__file__)
data_dir = os.path.join(code_dir, 'data') 
output_dir = os.path.join(code_dir, 'output')
if not os.path.isdir(output_dir):
    os.mkdir(output_dir)

# Get input data
csv_files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
df = pd.DataFrame()
for f in csv_files:
    input_file = os.path.join('data', f)
    df_in = pd.read_csv(input_file, parse_dates=[0])
    df_in = df_in[['pull_timestamp', 'subscribers', 'users_here', 'subreddit']].set_index('pull_timestamp', drop=False)

    df_in['subs'] = pd.to_numeric(df_in['users_here'], errors='coerce')
    df_in['subs_n'] = normalize(pd.to_numeric(df_in['subscribers'], errors='coerce'))
    df_in['users_n'] = normalize(pd.to_numeric(df_in['users_here'], errors='coerce'))
    df_in['users_clip'] = df_in['users_n'].clip(0, 0.35)

    df = pd.concat([df, df_in])

df['pdt'] = df['pull_timestamp'] - timedelta(hours=7)
df['dow'] = df['pdt'].dt.dayofweek
df['hr'] = df['pdt'].dt.hour



subreddits = df['subreddit'].unique()
for s in subreddits:
    fig = plt.figure()
    plt.plot(df.loc[df['subreddit']==s, 'users_n'])
    plt.title(s)
#    plt.close(fig)


plt.plot(df['users_clip'])

dp = pd.pivot_table(df, index='dow', columns='hr', values='users_clip', aggfunc='sum')

fig, ax = plt.subplots(figsize=(12, 4), dpi=150)
plt.imshow(dp, interpolation='nearest', cmap='YlOrRd')
ax.grid(False)
#for _, loc in ax.spines.items():
##    loc.set_visible(True)
#    loc.set_color('black')
#plt.yticks(np.linspace(0,11,12), month_names,
#           size='small',
#           color='black')
##x_values, x_names = get_custom_tick_labels(dp, 2)
#plt.xticks(x_values, x_names,
#           size='small',
#           color='black',
#           rotation='vertical')
#cax = fig.add_axes([0.92, .3333, 0.01, .3333])
#cb = plt.colorbar(label='Births/day', cax=cax)
#cb.outline.set_edgecolor('black')
#cax.yaxis.label.set_font_properties(h3)
#cax.set_yticklabels(cax.get_yticklabels(),
#                    size='x-small')