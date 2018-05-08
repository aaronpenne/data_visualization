# -*- coding: utf-8 -*-
"""
Measuring subreddit traffic data via scraped 'users_here' numbers

Author: Aaron Penne
Created: 2018-04-15

Developed with:
    Python 3.6
    macOS 10.13
""" 

import numpy as np
import pandas as pd
import seaborn as sns
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
    df_in['users'] = pd.to_numeric(df_in['users_here'], errors='coerce')
    threshold = (1 * df_in['users'].std()) + df_in['users'].mean()
    df_in['users_clip'] = df_in['users'].clip(0, threshold)
    df = pd.concat([df, df_in])

# Pull out timestamp pieces for pivot table and heatmap generation
df['time'] = df['pull_timestamp']
df['time'] = df['pull_timestamp'] - timedelta(hours=7)  # Change timezone to PDT
df['dow'] = df['time'].dt.dayofweek
df['hr'] = df['time'].dt.hour
df['elapsed'] = df['time'].dt.floor('15min') - df['time'].dt.floor('d')
df['mins'] = np.floor(df['elapsed'].dt.total_seconds() / 60)

# Plot line plots of raw and filtered data for each subreddit
figsize = (6,4)
dpi = 300
subreddits = df['subreddit'].unique()
for s in subreddits:
    df_s = df[df['subreddit']==s]
    
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    plt.title('r/{} - Raw'.format(s))
    plt.xlabel(' ', size='small')
    plt.xticks(rotation=90)
    plt.ylabel('Users Here', size='small')
    ax.tick_params(axis='both', which='both',length=0, labelsize='small')
    plt.plot(df_s['users'], linewidth=0.7, color='black')
    for _, loc in ax.spines.items():
        loc.set_visible(False)
    ax.text(df_s['time'].max(), 0 - (df_s['users'].max() - df_s['users'].min())/2,
            'Data & Code: www.github.com/aaronpenne\n@aaronpenne © 2018',
            size='x-small',
            color='gray',
            va='top',
            ha='right')
    fig.savefig(os.path.join(output_dir, '{}_raw.png'.format(s.lower())), dpi='figure', bbox_inches='tight', pad_inches=.11)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    flierprops = dict(marker='.', markeredgecolor='none', markerfacecolor='gray', markersize=5)
    sns.boxplot(x='mins', y='users', data=df_s, flierprops=flierprops, color='gray', linewidth=0.7)
    plt.title('r/{} - Time of Day'.format(s))
    plt.xlabel('Hour of Day', size='small')
    plt.ylabel('Users Here', size='small')
    ax.tick_params(axis='both', which='both',length=0, labelsize='small')
    plt.xticks(np.arange(0,24*4,4), np.arange(0,24),
           color='black',
           rotation='vertical')
    for _, loc in ax.spines.items():
        loc.set_visible(False)
    ax.text(24*4, 0 - (df_s['users'].max() - df_s['users'].min())/3,
        'Data & Code: www.github.com/aaronpenne\n@aaronpenne © 2018',
        size='x-small',
        color='gray',
        va='top',
        ha='right')
    fig.savefig(os.path.join(output_dir, '{}_time.png'.format(s.lower())), dpi='figure', bbox_inches='tight', pad_inches=.11)
    plt.close(fig)
    
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    flierprops = dict(marker='.', markeredgecolor='none', markerfacecolor='gray', markersize=3)
    sns.boxplot(x='dow', y='users', data=df_s, flierprops=flierprops, color='gray', width=0.5, linewidth=0.7)
    plt.title('r/{} - Day of Week'.format(s))
    plt.xlabel('Day Name', size='small')
    plt.ylabel('Users Here', size='small')
    ax.tick_params(axis='both', which='both',length=0, labelsize='small')
    plt.xticks(np.arange(0,7), ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
           color='black',
           rotation='vertical')
    for _, loc in ax.spines.items():
        loc.set_visible(False)
    ax.text(df_s['dow'].max(), 0 - (df_s['users'].max() - df_s['users'].min())/3,
            'Data & Code: www.github.com/aaronpenne\n@aaronpenne © 2018',
            size='x-small',
            color='gray',
            va='top',
            ha='right')
    fig.savefig(os.path.join(output_dir, '{}_day.png'.format(s.lower())), dpi='figure', bbox_inches='tight', pad_inches=.11)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    dp = pd.pivot_table(df_s, index='dow', columns='hr', values='users_clip', aggfunc='sum')
    plt.imshow(dp, interpolation='nearest', cmap='YlOrRd')
    plt.title('r/{} - Heatmap'.format(s))
    plt.xlabel('Hour of Day', size='small')
    plt.ylabel('Day of Week', size='small')
    ax.tick_params(axis='both', which='both',length=0, labelsize='small')
    plt.xticks(np.arange(0,24), np.arange(0,24),
           color='black',
           rotation='vertical')
    plt.yticks(np.arange(0,7), ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
           color='black')
    for _, loc in ax.spines.items():
        loc.set_visible(False)
    ax.text(df_s['hr'].max(), 9,
            'Data & Code: www.github.com/aaronpenne\n@aaronpenne © 2018',
            size='x-small',
            color='gray',
            va='top',
            ha='right')
    fig.savefig(os.path.join(output_dir, '{}_heat.png'.format(s.lower())), dpi='figure', bbox_inches='tight', pad_inches=.11)
    plt.close(fig)
    
# Create README because I'm lazy
with open('README.md', 'w+') as f:
    f.write('# Subreddit Traffic\n\n')
    subs = [s.lower() for s in subreddits]
    subs.sort()
    for s in subs:
        f.write('- [r/{0}](#r{0}-)\n'.format(s))
    f.write('\n\n')
    for s in subs:
        f.write('## r/{} [↑](#subreddit-traffic)\n\n'.format(s))
        for name in ['heat', 'raw', 'day', 'time']:
            f.write('![{0} {1}](https://github.com/aaronpenne/data_visualization/blob/master/traffic/charts/{0}_{1}.png)\n'.format(s, name))
        f.write('\n\n')