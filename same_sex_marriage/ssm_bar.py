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

## Define globals
dpi = 100
resolution = 2
input_file = 'C:\\tmp\\ssm_3.csv'
output_dir = 'C:\\tmp\\output_bar\\'
if not os.path.isdir(output_dir):
    os.mkdir(output_dir)
    
## Read in CSV
df = pd.read_csv(input_file)

# Delete the state columns because this viz is from the country level
states = df.loc[:,'abbrev']
# Delete the state columns because this viz is from the country level
df = df.drop(['State', 'abbrev'], axis=1)

## Add NaN columns to increase viz resolution
for res in range(3):
    df_columns = list(df)
    for i in range(1, 2*len(df_columns)-1, 2):
        df.insert(i, ' ',
                  float('nan'),
                  allow_duplicates=True)
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
    mask_le = df.iloc[:,i]>1
    mask_no = (df.iloc[:,i]>0) & (df.iloc[:,i]<=1)
    mask_st = (df.iloc[:,i]<0) & (df.iloc[:,i]>=-1)
    mask_co = df.iloc[:,i]<-1
    
    
    plt.figure()
    plt.bar(df[mask_le].index,
            df[mask_le].iloc[:,i],
            width=1,
            color='blue')
    plt.bar(df[mask_no].index,
            df[mask_no].iloc[:,i],
            width=1,
            color='grey')
    plt.bar(df[mask_st].index,
            df[mask_st].iloc[:,i],
            width=1,
            color='orange')
    plt.bar(df[mask_co].index,
            df[mask_co].iloc[:,i],
            width=1,
            color='red')
    plt.title(column, fontdict=font_title)
    plt.xlabel('')
    plt.ylabel('')
    plt.ylim(-3, 3)
    plt.yticks([-2, -1, 1, 2], 
               ['Constitutional Ban',
                'Statutory Ban',
                'No Law',
                'Legal'],
                fontname='monospace')
    plt.tight_layout()
    plt.savefig('{0}{1:03.0f}.png'.format(output_dir, i), dpi=dpi)
    plt.close()
#    
### Create title page/chart to break up the loop, saving image
#sns.set_style('white', {'xtick.color': 'white', 'axes.labelcolor': 'white'})
#plt.figure()
#violin = sns.violinplot(x=df['1995'], inner=None, palette='Set2', bw=0.4)
#plt.text(2, -1.5,
#         'Same Sex Marriage Laws in the USA\n1995 - 2015',
#         fontdict=font_h1)
#plt.text(-1, -2.35,
#         '© Aaron Penne\nSource: Pew Research Center, Religion & Public Life',
#         fontdict=font_h2)
#plt.title(' ')
#plt.ylim(-2, -1)
#plt.xlim(-1, 5)
#plt.xticks([0, 1, 2, 3], 
#           ['Constitutional Ban',
#            'Statutory Ban',
#            'No Law',
#            'Legal'],
#            rotation=90)
#plt.yticks([-2, -0.5, -1])
#violin.xaxis.label.set_color('white')
#violin.yaxis.label.set_color('white')
#plt.xlabel('')
#plt.ylabel('% of States')
#plt.tight_layout()
#plt.savefig('{0}999.png'.format(output_dir), dpi=200)

## Append images to create GIF 
# Read in all png files in folder - https://stackoverflow.com/a/27593246
png_files = [f for f in os.listdir(output_dir) if f.endswith('.png')]

charts = []
## Append the title chart - https://stackoverflow.com/a/35943809
#for i in range(30):
#    charts.append(imageio.imread('{0}999.png'.format(output_dir)))

# Append all the charts (except the title slide)
for i,f in enumerate(png_files):
    charts.append(imageio.imread('{0}{1}'.format(output_dir, f)))
    if i % 8 == 0:
        for k in range(10):
            charts.append(imageio.imread('{0}{1}'.format(output_dir, f)))
            
# Append the last chart a few extra times
for i in range(10):
    charts.append(imageio.imread('{0}{1}'.format(output_dir, f)))

# Save gif
imageio.mimsave('{0}ssm_bar.gif'.format(output_dir), charts, format='GIF', duration=0.07)
