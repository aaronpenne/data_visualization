# -*- coding: utf-8 -*-
"""
Heatmap for US birth rate per month (births per capita)

Author: Aaron Penne
Created: 2017

Developed with:
    Python 3.6
    Windows 10
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os

# Set output directory, make it if needed
output_dir = os.path.realpath(r'C:\tmp\births')  # Windows machine
if not os.path.isdir(output_dir):
    os.mkdir(output_dir)

# Get input data
input_file = os.path.realpath(r'C:\tmp\USAbirthbymonth.txt')
df = pd.read_csv(input_file)

input_file = os.path.realpath(r'C:\tmp\days_of_month.txt')
df_days = pd.read_csv(input_file)

df = df[~df.Month.isin(['TOT'])]

df_pivot = pd.pivot_table(df, index='Month', columns='Year', values='Births', aggfunc=np.sum)
months = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
df_pivot = df_pivot.reindex(months, axis=0)

c = df_pivot.values / df_days.values
df_norm = pd.DataFrame(data=c, columns=df_pivot.columns, index=months)

# 
# ## Visualization
# 
# * Now the whole friggin point is to make a chart. 

# In[26]:

sns.set()

fig, ax = plt.subplots(figsize=(12, 4))
cbar_ax = fig.add_axes([0.93, .33, .01, .33])
sns.heatmap(df_norm,
            ax = ax,
            cbar_ax = cbar_ax,
            yticklabels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
            xticklabels=2,
            vmin = 5500,
            vmax = 12500,
            cmap="gist_heat",
            square=True,
            cbar=True)
ax.set_xlabel('Year', 
            fontsize=16,
            fontname = 'Consolas')
ax.set_ylabel('')
ax.tick_params(axis='both', which='major', labelsize=9)
fig.set_facecolor('#f3f3f3') 


# Chart titles
ax.text(-3, 16,
        'USA Births Per Day binned by Month (1933-2015)',
        fontsize = 20,
        weight = 'bold',
        fontname = 'Consolas')
ax.text(-3, 14,
        'Calculated by dividing the count of births in a given month by the number of days in that month.',
        fontsize = 14,
        alpha = .85,
        fontname = 'Consolas')

# Chart footer
ax.text(-3, -7,
        '_____________________________________________________________________________________________________',
        fontsize = 14,
        color = 'grey',
        alpha = .77,
        fontname = 'Consolas')
ax.text(-3, -9,
        '© Aaron Penne',
        fontsize = 14,
        color = 'grey',
        alpha = .77,
        fontname = 'Consolas')
ax.text(63, -9,
        'Source: Human Mortality Database',
        fontsize = 14,
        color = 'grey',
        alpha = .77,
        fontname = 'Consolas')
fig.savefig('Rate_Births_Month_USA.jpg', dpi=200, bbox_inches='tight', pad_inches=.11)


# * Awwww yeahhhh
# 
# ## Conclusion
# 
# * Purely a quick-and-dirty visual analysis, statistics aren't good for me when I'm sleepy so I'll come back to that. FIXME
# * That baby boomer spike is so nicely timed with WWII that it's amazing. The war ended on September 2, 1945 and nine months later is June 1946, precisely when the births start **heating** up.
# * As pointed out by some Redditors, it is possible that 'echos' from the baby boomers show up every 20ish years.
# * Big drop off from 1971-ish through 1978-ish. Curious to see what war/economy/politics were going on then.
# * July through October has higher birth months, likely due to more banging during the winter.
# * February has a streak of low numbers, wonder if the shorter number of days is a contributing factor?
# * November also has a low number sreak, which surprises me because I figured 9 months after February (Valentine's Day) would have a spike.
# * Interesting trend up during 1942/1943... Starts increasing in August/September 1942 which is 9 months after the attack on Pearl Harbor (Dec 7, 1941). Possibly putting a bun in the oven before heading off to war?
# * Hey this is fun making guesses based on a chart!
# 
# 
# * Let's take a look at the describe() output for each month of the pivot table (transposed):

# In[25]:

df_describe = df_norm.T.describe(percentiles=[0.5])

pd.set_option('display.float_format', lambda x: '%.0f' % x)
df_describe


# * Seeing this little table makes me want to plot more but it's time for bed. ...violin plots for each month? bar chart of monthly means?
