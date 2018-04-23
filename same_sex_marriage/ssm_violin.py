#
# DataViz Battle Feb 2018
# https://www.reddit.com/r/dataisbeautiful/comments/7vegvf/battle_dataviz_battle_for_the_month_of_february/
#
# Author: Aaron Penne
#
# Created: 02-22-2018
#
# Source: Pew Research Center, Religion & Public Life
#         http://www.pewforum.org/2015/06/26/same-sex-marriage-state-by-state/
# 

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import imageio
import os

code_dir = os.path.dirname(__file__)
data_dir = os.path.join(code_dir, 'data')
output_dir = os.path.join(code_dir, 'output')
if not os.path.isdir(output_dir):
    os.mkdir(output_dir)
    
## Read in CSV
df = pd.read_csv(os.path.join(data_dir, 'ssm_2.csv'))

## Create categorical encoding
category_dict = {'Constitutional Ban': 0,
                 'Statutory Ban': 1,
                 'No Law': 2,
                 'Legal': 3}
df = df.replace(category_dict)
# Delete the state columns because this viz is from the country level
df = df.drop(['State', 'abbrev'], axis=1)

## Add NaN columns to increase viz resolution
for res in range(3):
    df_columns = list(df)
    for i in range(1, 2*len(df_columns)-1, 2):
        df.insert(i, df.columns[i-1],
                  float('nan'),
                  allow_duplicates=True)
    # Interpolate between columns and replace NaNs, [2, NaN, 3] becomes [2, 2.5, 3]
    df = df.interpolate(axis=1)

## Set up plotting and formatting of viz
sns.set_style("white")
font_h1 = {'family': 'monospace',
           'color': 'black',
           'weight': 'regular',
           'size': 'small',
           'horizontalalignment': 'center'}
font_h2 = {'family': 'monospace',
            'color': '#6f6f6f',
            'weight': 'regular',
            'size': 'xx-small',
            'horizontalalignment': 'left'}
font_title = {'family': 'monospace',
              'color': '#6f6f6f',
              'weight': 'regular',
              'size': 'xx-small',
              'va': 'center',
              'ha': 'center'}

dpi = 200
figsize = (700/dpi,400/dpi)
pad = 0
    
## Create all interpolated data charts, saving images
for i, column in enumerate(df):
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    violin = sns.violinplot(x=df.iloc[:,i], 
                            inner=None, 
                            color='#3f3f3f', 
                            linewidth=0,
                            bw=0.4,
                            scale='count',
                            scale_hue=False)
    plt.title(' ')
    plt.xlabel('')
    plt.ylabel('% of States',
               fontname='monospace')
    plt.ylim(-0.5, 0.5)
    plt.xlim(-2, 5)
    plt.xticks([0, 1, 2, 3], 
               ['Constitutional Ban',
                'Statutory Ban',
                'No Law',       
                'Legal'],
                rotation=90,
                fontname='monospace',
                fontsize='x-small')
    plt.yticks([-0.5, 0, 0.5])
    violin.xaxis.label.set_fontsize('x-small')
    violin.yaxis.label.set_fontsize('x-small')
    if i % 8 == 0 and i != 0:
        pad += 0.35 
    plt.text(-2+pad, 0.57, column, fontdict=font_title)
    plt.text(1.5, 0.7,
         'Same Sex Marriage Laws in the USA\n1995 - 2015',
         fontdict=font_h1)
    plt.text(-2, -1.7,
            'Source: Pew Research Center\n' \
            'Data and code: www.github.com/aaronpenne\n' \
            'Aaron Penne © 2018\n\n',
            fontdict=font_h2)
    fig.savefig(os.path.join(output_dir, '{:03.0f}_{}.png'.format(i, column)),
            dpi=fig.dpi,
            bbox_inches='tight',
            pad_inches=0.3)
    plt.close()

## Append images to create GIF 
# Read in all png files in folder - https://stackoverflow.com/a/27593246
png_files = [f for f in os.listdir(output_dir) if f.endswith('.png')]
png_files.sort()

charts = []
# Append all the charts (except the title slide)
for f in png_files:
    if f == png_files[-1]:
        for i in range(20):
            charts.append(imageio.imread(os.path.join(output_dir, f)))
    charts.append(imageio.imread(os.path.join(output_dir, f)))

# Save gif
imageio.mimsave(os.path.join(output_dir, 'ssm_violin.gif'), charts, format='GIF', duration=0.08)
