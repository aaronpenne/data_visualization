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


min_year = 1975
max_year = 2018


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

# Rate plot for grounding
dp = df

fig, ax = plt.subplots(figsize=(12, 4))
ax.plot(dp['rate'])

# Boxplot with dots (month to month comparison)
dp = df

fig, ax = plt.subplots(figsize=(12, 4))
sns.boxplot(x='month', y='rate', data=dp, ax=ax, palette='plasma')
sns.stripplot(x='month', y='rate', data=dp, ax=ax, color='0', jitter=0.1)

# Heatmap - full data
dp = pd.pivot_table(df, index='month', columns='year', values='rate', aggfunc=np.sum)

fig, ax = plt.subplots(figsize=(12, 4))
cbar_ax = fig.add_axes([0.93, .33, .01, .33])
sns.heatmap(dp,
            ax = ax,
            cbar_ax = cbar_ax,
            yticklabels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
            xticklabels=2,
            cmap="plasma",
            square=True,
            cbar=True)
ax.set_xlabel('Year', 
            fontsize=16,
            fontname = 'monospace')
ax.set_ylabel('')
ax.tick_params(axis='both', which='major', labelsize=9)

# Heatmap - ranged data
dp = df
dp = dp.loc[dp.index.to_series().dt.year >= min_year]
dp = dp.loc[dp.index.to_series().dt.year <= max_year]
dp = pd.pivot_table(dp, index='month', columns='year', values='rate', aggfunc=np.sum)

fig, ax = plt.subplots(figsize=(12, 4))
cbar_ax = fig.add_axes([0.93, .33, .01, .33])
sns.heatmap(dp,
            ax = ax,
            cbar_ax = cbar_ax,
            yticklabels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
            xticklabels=2,
            cmap="plasma",
            square=True,
            cbar=True)
ax.set_xlabel('Year', 
            fontsize=16,
            fontname = 'monospace')
ax.set_ylabel('')
ax.tick_params(axis='both', which='major', labelsize=9)

# Plot each month over the years
dp = df
dp = pd.pivot_table(dp, index='month', columns='year', values='rate', aggfunc=np.sum)

fig, ax = plt.subplots(figsize=(12, 4))
for index, row in dp.iterrows():
    ax.plot(row)
    
# Plot max/min of each year over the years
dp = df
dp = pd.pivot_table(dp, index='month', columns='year', values='rate', aggfunc=np.sum)

fig, ax = plt.subplots(figsize=(12, 4))
for year in df:
    ax.plot(dp.max())
    ax.plot(dp.min())