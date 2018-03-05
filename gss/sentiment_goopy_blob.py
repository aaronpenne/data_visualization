#
# Author: Aaron Penne
#
# Created: 02-22-2018
#
# Source: General Social Survey
#         https://gssdataexplorer.norc.org/variables/272/vshow
#
# Variable: gunlaw
# Question: Would you favor or oppose a law which would require a person to 
#           obtain a police permit before he or she could buy a gun? 
#

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import imageio
import os

## Define globals
input_file = 'C:\\tmp\\gun_permit_1976-2016.csv'
output_dir = 'C:\\tmp\\output_gun\\'
if not os.path.isdir(output_dir):
    os.mkdir(output_dir)
    
## Read in CSV
df = pd.read_csv(input_file)

#df_dict = {'year': [],
#           'opinion': []}
#for row in list(df.index):
#    a = []
#    a = [-2] * int(round(df.iloc[row,1]))  # Oppose
#    a += [0] * int(round(df.iloc[row,2]))  # Dont_know
#    a += [2] * int(round(df.iloc[row,3]))  # Favor
#    df_dict['year'] += [df.iloc[row,0]] * len(a)
#    df_dict['opinion'] += a
#    
#df_melt = pd.DataFrame(df_dict)


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
    violin = sns.violinplot(x=df.iloc[:,i], 
                            inner=None, 
                            palette='Set2', 
                            bw=0.4,
                            scale='count',
                            scale_hue=False)
    plt.title(column, fontdict=font_title)
    plt.xlabel('')
    plt.ylabel('% of Respondents',
               fontname='monospace')
    plt.ylim(-0.5, 0.5)
    plt.xlim(-3, 3)
    plt.xticks([-2, 0, 2], 
               ['Oppose',
                'No Opinion',
                'Support'],
                rotation=90)
    plt.yticks([-0.5, 0, 0.5])
    plt.tight_layout()
    plt.savefig('{0}{1:03.0f}_{2}.png'.format(output_dir, i, column), dpi=200)
    plt.close()
    
## Create title page/chart to break up the loop, saving image
sns.set_style('white', {'xtick.color': 'white', 'axes.labelcolor': 'white'})
plt.figure()
violin = sns.violinplot(x=df['1996'], inner=None, palette='Set2', bw=0.4)
plt.text(0, -1.5,
         'Support/oppose law to get a\npolice permit before buying a gun?\n1972-2016',
         fontdict=font_h1)
plt.text(-3, -2.35,
         '© Aaron Penne\nSource: General Social Survey',
         fontdict=font_h2)
plt.title(' ')
plt.ylim(-2, -1)
plt.xlim(-3, 3)
plt.xticks([-2, 0, 2], 
           ['Oppose',
            'No Opinion',
            'Support'],
            rotation=90)
plt.yticks([-2, -0.5, -1])
violin.xaxis.label.set_color('white')
violin.yaxis.label.set_color('white')
plt.xlabel('')
plt.ylabel('% of States')
plt.tight_layout()
plt.savefig('{0}999.png'.format(output_dir), dpi=200)

## Append images to create GIF 
# Read in all png files in folder - https://stackoverflow.com/a/27593246
png_files = [f for f in os.listdir(output_dir) if f.endswith('.png')]

charts = []
# Append the title chart - https://stackoverflow.com/a/35943809
for i in range(30):
    charts.append(imageio.imread('{0}999.png'.format(output_dir)))

# Append all the charts (except the title slide)
for f in png_files[:-1]:
    charts.append(imageio.imread('{0}{1}'.format(output_dir, f)))

# Append the last chart a few extra times
for i in range(10):
    charts.append(imageio.imread('{0}{1}'.format(output_dir, f)))

# Save gif
imageio.mimsave('{0}gun_violin.gif'.format(output_dir), charts, format='GIF', duration=0.07)
