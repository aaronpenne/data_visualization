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
        os.mkdir(output_dir)
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


# Line - raw
dp = df
fig, ax = plt.subplots(figsize=(12, 4), dpi=150)
ax.plot(dp['birth'], color='black')
plt.title('Monthly USA Birth Counts 1933-2015')
ax.set_xlabel("Year")
ax.set_ylabel('Births')
ax.text(728000, 15,
        'Birth data: Human Mortality Database\nPopulation data: US Census Bureau\nCode: www.github.com\\aaronpenne\nAaron Penne © 2018',
        fontsize = 8,
        color = 'gray',
        multialignment = 'right')
fig.savefig('birth_count_usa_line.png', dpi='figure', bbox_inches='tight', pad_inches=.11)



#
# Birth rate
#
    
# Line - raw
dp = df
fig, ax = plt.subplots(figsize=(12, 4), dpi=150)
ax.plot(dp['rate'], color='black')
plt.title('Monthly USA Birth Rate 1933-2015')
ax.set_xlabel("Year")
ax.set_ylabel('Births/day per million ppl')
ax.text(728000, 15,
        'Birth data: Human Mortality Database\nPopulation data: US Census Bureau\nCode: www.github.com\\aaronpenne\nAaron Penne © 2018',
        fontsize = 8,
        color = 'gray',
        multialignment = 'right')
fig.savefig('birth_rate_usa_line.png', dpi='figure', bbox_inches='tight', pad_inches=.11)


# Boxplot - with dots (month to month comparison)
dp = df
fig, ax = plt.subplots(figsize=(12, 4), dpi=150)
sns.boxplot(x='month', y='rate', data=dp, ax=ax, palette='Set2')
sns.stripplot(x='month', y='rate', data=dp, ax=ax, color='black', alpha=0.3, jitter=0.2)
plt.title('USA Birth Rate 1933-2015 - Month to Month comparison')
ax.set_xlabel("Month")
ax.set_ylabel('Births/day per million ppl')
ax.text(8, 10,
        'Birth data: Human Mortality Database\nPopulation data: US Census Bureau\nCode: www.github.com\\aaronpenne\nAaron Penne © 2018',
        fontsize = 8,
        color = 'gray',
        multialignment = 'right')
fig.savefig('birth_rate_usa_box.png', dpi='figure', bbox_inches='tight', pad_inches=.11)

    
# Line - each month over years
dp = df
dp = pd.pivot_table(dp, index='month', columns='year', values='rate', aggfunc=np.sum)
fig, ax = plt.subplots(figsize=(12, 4))
for index, row in dp.iterrows():
    ax.plot(row)
    
# Line - max/min of each year over the years
dp = df
dp = pd.pivot_table(dp, index='month', columns='year', values='rate', aggfunc=np.sum)
fig, ax = plt.subplots(figsize=(12, 4))
for year in df:
    ax.plot(dp.max())
    ax.plot(dp.min())

    
# Heatmap - matplotlib
dp = pd.pivot_table(df, index='month', columns='year', values='rate', aggfunc=np.sum)
fig, ax = plt.subplots(figsize=(12, 4), dpi=150)
plt.imshow(dp, interpolation='nearest', cmap='YlOrRd')
ax.grid(False)
for _, loc in ax.spines.items():
#    loc.set_visible(True)
    loc.set_color('black')
plt.yticks(np.linspace(0,11,12), month_names,
           size='small',
           color='black')
x_values, x_names = get_custom_tick_labels(dp, 2)
plt.xticks(x_values, x_names,
           size='small',
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
        fontsize = 14,
        color = 'black',
        weight = 'bold',)
ax.text(-0.5, -2,
        'Rate = Births / Population / Days in Month',
        fontsize = 12,
        color = 'black',)
ax.text(64, -2,
        'Birth data: Human Mortality Database\nPopulation data: US Census Bureau\nCode: www.github.com\\aaronpenne\nAaron Penne © 2018',
        fontsize = 7,
        color = 'gray',
        multialignment = 'right')
fig.savefig('birth_rate_heat_usa.png', dpi='figure', bbox_inches='tight', pad_inches=.11)


# Heatmap - matplotlib - ranged
dp = df
dp = dp.loc[dp.index.to_series().dt.year >= min_year]
dp = dp.loc[dp.index.to_series().dt.year <= max_year]
dp = pd.pivot_table(dp, index='month', columns='year', values='rate', aggfunc=np.sum)
fig, ax = plt.subplots(figsize=(8, 4), dpi=150)
plt.imshow(dp, interpolation='nearest', cmap='YlOrRd')
ax.grid(False)
for _, loc in ax.spines.items():
#    loc.set_visible(True)
    loc.set_color('black')
plt.yticks(np.linspace(0,11,12), month_names,
           size='small',
           color='black')
x_values, x_names = get_custom_tick_labels(dp, 2)
plt.xticks(x_values, x_names,
           size='small',
           color='black',
           rotation='vertical')
cax = fig.add_axes([0.92, .28, 0.01, .45])
cb = plt.colorbar(label='Births/day per million ppl', cax=cax)
cb.outline.set_edgecolor('black')
cax.yaxis.label.set_font_properties(h3)
cax.set_yticklabels(cax.get_yticklabels(),
                    size='x-small')
# Annotations
ax.text(-0.5, -3.5,
        'Monthly USA Birth Rate Per Capita ' + str(min_year) + '-' + str(max_year),
        fontsize = 12,
        color = 'black',
        weight = 'bold')
ax.text(-0.5, -2,
        'Rate = Births / Population / Days in Month',
        fontsize = 10,
        color = 'black')
ax.text(34, -2,
        'Birth data: Human Mortality Database\nPopulation data: US Census Bureau\nCode: www.github.com\\aaronpenne\nAaron Penne © 2018',
        fontsize = 6,
        color = 'gray',
        multialignment = 'right')
fig.savefig('birth_rate_usa_heat_ranged.png', dpi='figure', bbox_inches='tight', pad_inches=.11)



  
# Heatmap - matplotlib - COUNT
dp = df
days_in_month = df.index.to_series().dt.daysinmonth
df['birth_norm'] = df['birth'] / days_in_month
dp = pd.pivot_table(df, index='month', columns='year', values='birth_norm', aggfunc=np.sum)
fig, ax = plt.subplots(figsize=(12, 4), dpi=150)
plt.imshow(dp, interpolation='nearest', cmap='YlOrRd')
ax.grid(False)
for _, loc in ax.spines.items():
#    loc.set_visible(True)
    loc.set_color('black')
plt.yticks(np.linspace(0,11,12), month_names,
           size='small',
           color='black')
x_values, x_names = get_custom_tick_labels(dp, 2)
plt.xticks(x_values, x_names,
           size='small',
           color='black',
           rotation='vertical')
cax = fig.add_axes([0.92, .3333, 0.01, .3333])
cb = plt.colorbar(label='Births/day', cax=cax)
cb.outline.set_edgecolor('black')
cax.yaxis.label.set_font_properties(h3)
cax.set_yticklabels(cax.get_yticklabels(),
                    size='x-small')
# Annotations
ax.text(-0.5, -4.2,
        'Monthly USA Birth Counts 1933-2015',
        fontsize = 14,
        color = 'black',
        weight = 'bold',)
ax.text(-0.5, -2,
        'Births Normalized = Births / Days in Month',
        fontsize = 12,
        color = 'black',)
ax.text(64, -2,
        'Birth data: Human Mortality Database\nPopulation data: US Census Bureau\nCode: www.github.com\\aaronpenne\nAaron Penne © 2018',
        fontsize = 7,
        color = 'gray',
        multialignment = 'right')
fig.savefig('birth_count_heat_usa.png', dpi='figure', bbox_inches='tight', pad_inches=.11)

