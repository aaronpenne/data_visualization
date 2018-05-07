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

mpl.rcParams['font.family'] = 'monospace'

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
df_f = pd.DataFrame()
for f in csv_files:
    input_file = os.path.join('data', f)
    df_in = pd.read_csv(input_file, parse_dates=[0])
    df_in = df_in[['pull_timestamp', 'subscribers', 'users_here', 'subreddit']].set_index('pull_timestamp', drop=False)

    df_in['subs'] = pd.to_numeric(df_in['subscribers'], errors='coerce')
    df_in['subs_n'] = normalize(df_in['subs'])
    df_in['users_n'] = normalize(pd.to_numeric(df_in['users_here'], errors='coerce'))
    df_in['users_clip'] = df_in['users_n'].clip(0, 0.35)
    df_in['filter'] = np.abs(df_in['users_n']-df_in['users_n'].mean())<=(4*df_in['users_n'].std())
    df = pd.concat([df, df_in])


#df['users_n'] = normalize(pd.to_numeric(df_in['users_n'], errors='coerce'))

# Pull out timestamp pieces for pivot table and heatmap generation
df['time'] = df['pull_timestamp']
df['time'] = df['pull_timestamp'] - timedelta(hours=7)  # Change timezone to PDT
df['dow'] = df['time'].dt.dayofweek
df['hr'] = df['time'].dt.hour
df['elapsed'] = df['time'].dt.floor('h') - df['time'].dt.floor('d')
df['mins'] = np.floor(df['elapsed'].dt.total_seconds() / 60)

# Make a new df with the filtered data
df_f = df[df['filter']]

# Plot line plots of raw and filtered data for each subreddit
#subreddits = df['subreddit'].unique()
subreddits = ['dataisbeautiful']
for s in subreddits:
    df_s = df_f[df_f['subreddit']==s]
    df_s['users_n_n'] = normalize(pd.to_numeric(df_s['users_n'], errors='coerce'))
    
    fig, ax = plt.subplots(2,1, figsize=(5,3), dpi=150, sharex=True, sharey=True)
    plt.suptitle('r/{}'.format(s))
    ax[0].plot(df_s['users_n'], lw=0.7)
    ax[1].plot(df_s['users_n_n'], lw=0.7)
#    plt.close(fig)

#plt.figure()
#plt.plot(df['users_clip'])
for s in subreddits:
    df_s = df_f[df_f['subreddit']==s]
    df_s['users_n_n'] = normalize(df_s['users_n'])
    
    dp = pd.pivot_table(df_s, index='dow', columns='mins', values='users_n_n', aggfunc='sum')
    fig, ax = plt.subplots(figsize=(5, 5), dpi=150)
    plt.imshow(dp, interpolation='nearest', cmap='YlOrRd')
    plt.title('r/{}'.format(s))
    ax.grid(False)
    for _, loc in ax.spines.items():
    #    loc.set_visible(True)
        loc.set_color('black')
    
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
        
import seaborn as sns
fig = plt.figure()
g = sns.boxplot(x='dow', y='users_n_n', data=df_s, color='gray')     
g.fig.get_axes()[0].set_yscale('log')
sns.stripplot(x='hr', y='users_n', data=df_s, jitter=True, color='gray')
