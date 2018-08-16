#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 16 08:33:06 2018

@author: aaronpenne
"""

import os
from datetime import datetime

import numpy as np
import pandas as pd

import matplotlib as mpl
import matplotlib.pyplot as plt
mpl.rcParams['font.family'] = 'monospace'

###############################################################################
# Parameters

deg = 1
min_date = datetime(2012, 1, 1)

def filter_date(df, min_date, max_date):
    return df[(df['date']>=min_date) & (df['date']<=max_date)]

def get_fit(df, deg):
    x_fit = np.arange(0,len(df['date']))
    y_fit = df['rate']
    
    z = np.polyfit(x_fit, y_fit, deg)
    return np.poly1d(z)
    

filename = os.path.join('data','unemp_black.xlsx')

df = pd.read_excel(filename,
                   index_col=0,
                   header=0,
                   skiprows=12)
cols = list(df)
df = df.unstack().reset_index()
df.columns = ['month', 'year', 'rate']
df['date'] = df['month'] + '-' + df['year'].apply(str)
df['date'] = pd.to_datetime(df['date'], format='%b-%Y')
df.sort_values(by=['date'], inplace=True)
df.dropna(inplace=True)
df.reset_index(inplace=True)

###############################################################################
# 2012-2015 (Obama)

df_ob = filter_date(df, datetime(2012, 1, 1), datetime(2015, 12, 1))
p_ob = get_fit(df_ob, deg)

###############################################################################
# 2016-2018 (Trump)

df_tr = filter_date(df, datetime(2016, 1, 1), datetime(2018, 12, 1))
p_tr = get_fit(df_tr, deg)

###############################################################################
# Plots

fig, ax1 = plt.subplots(figsize=(4,5), dpi=200)
ax1.set_axisbelow(True)

# All dates
x = df.loc[df['date']>=min_date, 'date']
y = df.loc[df['date']>=min_date, 'rate']
ax1.scatter(list(x.values), list(y.values), color='#3f3f3f', linewidth=0, alpha=0.4)

# 2012-2015
x = df_ob['date']
x_num = np.arange(0, len(x))
y = p_ob(x_num)
ax1.plot(x, y, '-', color='#4183d7')
ax1.text(x.iloc[9+int(np.median(x_num))], 13.2, 'Obama (2nd term)', rotation=-52, ha='center', color='#4183d7')

# 2016-2018
x = df_tr['date']
x_num = np.arange(0, len(x))
y = p_tr(x_num)
ax1.plot(x, y, '-', color='#d24d57')
ax1.text(x.iloc[5+int(np.median(x_num))], 8.5, 'Trump', rotation=-41, ha='center', color='#d24d57')

# Adjust figure
light_grey = '#eeeeee'
med_grey = '#aaaaaa'
#ax1.grid(axis='x', color=light_grey)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)

vals = ax1.get_yticks()
ax1.set_yticklabels(['{:0.0f}%'.format(x) for x in vals])

ax1.set_xlabel('Years', size='x-small')
ax1.tick_params(axis='x', labelsize='x-small')
ax1.tick_params(axis='y',  labelsize='x-small')

ax1.set_title('U.S. Black Unemployment Rate', size='medium')

###############
ax1.text(datetime(2015,1,1), 3,
            'Data: data.bls.gov\n' \
            'Code: www.github.com/aaronpenne\n' \
            'Aaron Penne © 2018',
            fontsize = 'x-small',
            color = med_grey,
            multialignment = 'right')

fig.savefig('black_unemployment.png',
            dpi=fig.dpi,
            bbox_inches='tight',
            pad_inches=0.3)

###############


fig, ax2 = plt.subplots(figsize=(4,5), dpi=200)
ax1.set_axisbelow(True)


x = df_tr['date']
x_num = np.arange(0, len(x))
y = p_tr(x_num)
y_start = y[0]
ax2.plot(x_num, y, '-', color='#d24d57')
ax2.text(16.5, 8.8, 'Trump (-0.08% per month)', rotation=-40, ha='center', color='#d24d57')
slope_tr = (y[-1]-y[0])/(x_num[-1]-x_num[0])

x = df_ob['date']
x_num = np.arange(0, 50)
y = p_ob(x_num)
y = y + (y_start - y[0])
ax2.plot(x_num, y, '-', color='#4183d7')
ax2.text(14, 8.1, 'Obama (-0.12% per month)', rotation=-52, ha='center', color='#4183d7')
slope_ob = (y[-1]-y[0])/(x_num[-1]-x_num[0])


slope_ob - slope_tr
         
         
# Adjust figure
light_grey = '#eeeeee'
med_grey = '#aaaaaa'
#ax2.grid(axis='x', color=light_grey)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

vals = ax2.get_yticks()
ax2.set_yticklabels(['{:0.0f}%'.format(x-9) for x in vals])

ax2.set_xlabel('Months', size='x-small')
ax2.tick_params(axis='x', labelsize='x-small')
ax2.tick_params(axis='y',  labelsize='x-small')

ax2.set_title('Change of U.S. Black Unemployment Rate', size='medium')

ax2.text(20, 4, '0.08/0.12 = 0.66', ha='center', size='x-small')
ax2.text(20, 3.5, 'The black unemployment rate has\ndecreased 33% slower under Trump', ha='center', size='x-small')


###############
ax2.text(20, 1.1,
            'Data: data.bls.gov\n' \
            'Code: www.github.com/aaronpenne\n' \
            'Aaron Penne © 2018',
            fontsize = 'x-small',
            color = med_grey,
            multialignment = 'right')

fig.savefig('black_unemployment_change.png',
            dpi=fig.dpi,
            bbox_inches='tight',
            pad_inches=0.3)