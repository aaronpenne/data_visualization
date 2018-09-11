# -*- coding: utf-8 -*-
"""
Heatmap for US birth rate per month (births per capita)

Author: Aaron Penne
Created: 2018-04-03

Developed with:
    Python 3.6
    Windows 10
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib as mp
import matplotlib.pyplot as plt
import os


def get_dir(dirname):
    if not os.path.isdir(dirname):
        os.mkdir(dirname)
    return dirname

def get_data_csv(filename):
    input_file = os.path.join('data', filename)
    df = pd.read_csv(input_file)
    return df

def round_to_n(x, n, direction=''):
    direction = direction.lower()
    if direction == 'up':
        return int(n*np.ceil(float(x)/n))
    elif direction == 'down':
        return int(n*np.floor(float(x)/n))
    else:
        return int(n*round(float(x)/n))
    
def get_custom_tick_labels(dp, base=5):
    x_names = [min(dp)]
    for i in range(int((round_to_n(max(dp),base,'down')-round_to_n(min(dp),base,'up'))/base)+1):
        x_names.append(round_to_n(min(dp),base,'up')+i*base)
    if x_names[-1] != max(dp):
        x_names.append(max(dp))
    
    x_values = []
    for name in x_names:
        x_values.append(dp.columns.get_loc(name))
        
    return x_values, x_names

min_year = 1975
max_year = 2015


#------------------------------------------------------------------------------
# Wrangling
#------------------------------------------------------------------------------


# Set output directory, make it if needed
output_dir = get_dir('output')

# Get input data
df_pop = get_data_csv('usa_pop_1917-2017.csv')
df_birth = get_data_csv('usa_birth_1933-2015.csv')

# Clean up and trim data
df_pop = df_pop[['Year', 'US']]
df_pop.columns = ['year', 'pop']
df_pop['month'] = 1
df_pop['day'] = 1

df_birth = df_birth[['Year', 'Month', 'Births']]
df_birth = df_birth[~df_birth['Month'].isin(['TOT'])]
df_birth.columns = ['year', 'month', 'birth']
df_birth['day'] = 1

# Set indices of dataframes as datetime values to make merging easy
df_pop = df_pop.set_index(pd.to_datetime(df_pop[['year', 'month', 'day']]))
df_birth = df_birth.set_index(pd.to_datetime(df_birth[['year', 'month', 'day']]))

# Create one dataframe with only the datetime index, population, and birth data
df_pop = df_pop['pop']
df_birth = df_birth['birth']
df = pd.concat([df_pop, df_birth], axis=1)

# Do linear interpolation between annual data to get better numbers for monthly population
df = df.interpolate(method='time')

# Calculate birth rate = monthly births per monthly population per days in month
days_in_month = df.index.to_series().dt.daysinmonth
df['rate'] = df['birth'] / df['pop'] / days_in_month * (10**6)
print('Units are births/month/million people')

# Break down date columns
df['month'] = df.index.to_series().dt.month
df['year'] = df.index.to_series().dt.year

# Get rid of rows without birth data
df = df.loc[df.index >= df_birth.index.min()]
df = df.loc[df.index <= df_birth.index.max()]

#------------------------------------------------------------------------------
# Visualization
#------------------------------------------------------------------------------


sns.set_style('whitegrid')
mp.rcParams['font.family'] = 'monospace'

month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

h1 = mp.font_manager.FontProperties(size='large')
h2 = mp.font_manager.FontProperties(size='small')
h3 = mp.font_manager.FontProperties(size='x-small')

#
# Birth rate
#

# Heatmap - matplotlib
dp = pd.pivot_table(df, index='month', columns='year', values='rate', aggfunc=np.sum)
fig, ax = plt.subplots(figsize=(12, 4), dpi=2400)
plt.imshow(dp, interpolation='nearest', cmap='YlOrRd')
ax.grid(False)
for _, loc in ax.spines.items():
#    loc.set_visible(True)
    loc.set_color('black')
plt.yticks(np.linspace(0,11,12), month_names,
           size='x-small',
           color='black')
x_values, x_names = get_custom_tick_labels(dp, 2)
plt.xticks(x_values, x_names,
           size='x-small',
           color='black',
           rotation='vertical')
cax = fig.add_axes([0.92, .3333, 0.01, .3333])
cb = plt.colorbar(label='Births/day per million ppl', cax=cax)
cb.outline.set_edgecolor('black')
cax.yaxis.label.set_font_properties(h3)
cax.set_yticklabels(cax.get_yticklabels(),
                    size='x-small')
# Annotations
ax.text(-0.5, -4.2,
        'Monthly USA Birth Rate Per Capita 1933-2015',
        fontsize = 13,
        color = 'black',
        weight = 'bold',)
ax.text(-0.5, -2,
        'Rate = Births / Population / Days in Month',
        fontsize = 11,
        color = 'black',)
fig.savefig(os.path.join(output_dir, 'birth_rate_heat_usa.png'), dpi=fig.dpi, bbox_inches='tight', pad_inches=.11)


