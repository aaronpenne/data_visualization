#
# DataViz Battle Feb 2018
# https://www.reddit.com/r/dataisbeautiful/comments/7vegvf/battle_dataviz_battle_for_the_month_of_february/
#
# Author: Aaron Penne
#
# Created: 02-21-2018
#
# Source: Pew Research Center, Religion & Public Life
#         http://www.pewforum.org/2015/06/26/same-sex-marriage-state-by-state/
# 

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import imageio
import os

## Define globals
input_file = 'ssm.csv'
output_dir = '.\output'

## Read in CSV
df = pd.read_csv(input_file)

## Create categorical encoding
category_dict = {'Constitutional Ban': 0,
                 'Statutory Ban': 1,
                 'No Law': 2,
                 'Legal': 3}
df = df.replace(category_dict)
# Delete the state columns because this viz is from the country level
df = df.drop(columns=['State', 'abbrev'])

## Add NaN columns to increase viz resolution
for res in range(3):
    df_columns = list(df)
    for i in range(1, 2*len(df_columns)-1, 2):
        df.insert(i, df.columns[i-1], float('nan'), allow_duplicates=True)
    # Interpolate between columns and replace NaNs, [2, NaN, 3] becomes [2, 2.5, 3]
    df = df.interpolate(axis=1)

## Set up plotting and formatting of viz
sns.set_style("white")
font_h1 = {'family': 'monospace',
           'color': 'black',
           'weight': 'semibold',
           'size': 14,
           'horizontalalignment': 'center'}
font_h2 = {'family': 'monospace',
            'color': 'black',
            'weight': 'regular',
            'size': 10,
            'horizontalalignment': 'left'}
font_title = {'family': 'monospace',
              'color': 'black',
              'weight': 'regular',
              'size': 12}

## Create all interpolated data charts, saving images
for i, column in enumerate(df):
    plt.figure()
    violin = sns.violinplot(x=df.iloc[:,i], inner=None, palette='Set2', bw=0.4)
    plt.title(column, fontdict=font_title)
    plt.xlabel('')
    plt.ylabel('')
    plt.xlim(-2, 5)
    plt.xticks([0, 1, 2, 3], 
               ['Constitutional Ban',
                'Statutory Ban',
                'No Law',
                'Legal'],
                rotation=90,
                fontname='monospace')
    plt.tight_layout()
    plt.savefig('{0:03.0f}_{1}.png'.format(i, column), dpi=300)
    plt.close()

## Create title page/chart to break up the loop, saving image
sns.set_style('white', {'xtick.color': 'white', 'axes.labelcolor': 'white'})
plt.figure()
violin = sns.violinplot(x=df['1995'], inner=None, palette='Set2', bw=0.4)
plt.text(2, -1.5,
         'Same Sex Marriage Laws in the USA\n1995 - 2015',
         fontdict=font_h1)
plt.text(-1, -2.35,
         '© Aaron Penne\nSource: Pew Research Center, Religion & Public Life',
         fontdict=font_h2)
plt.title(' ')
plt.ylim(-2, -1)
plt.xlim(-1, 5)
plt.xticks([0, 1, 2, 3], 
           ['Constitutional Ban',
            'Statutory Ban',
            'No Law',
            'Legal'],
            rotation=90)
violin.xaxis.label.set_color('white')
plt.xlabel('')
plt.tight_layout()
plt.savefig('999.png', dpi=300)

## Append images to create GIF 
# Read in all png files in folder - https://stackoverflow.com/a/27593246
png_files = [f for f in os.listdir('.') if f.endswith('.png')]

charts = []
# Append the title chart - https://stackoverflow.com/a/35943809
for i in range(5):
    charts.append(imageio.imread('999.png'))

# Append all the charts (except the title slide)
for f in png_files[:-1]:
    charts.append(imageio.imread(f))

# Append the last chart a few extra times
for i in range(3):
    charts.append(imageio.imread(f))

# Save gif
imageio.mimsave('ssm_violin.gif', charts, format='GIF', duration=0.1)