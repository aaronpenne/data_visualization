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
import os

## Define globals
bandwidth = 0.35
input_file = os.path.join('data', 'ssm.csv')
output_dir = 'output'
if not os.path.isdir(output_dir):
    os.mkdir(output_dir)
    
## Read in CSV
df = pd.read_csv(input_file)

## Create categorical encoding
category_dict = {'Constitutional Ban': 0,
                 'Statutory Ban': 1,
                 'No Law': 2,
                 'Legal': 3}
df = df.replace(category_dict)

# Delete the state column for clarity
df = df.drop(['State', 'abbrev'], axis=1)

# Rearrange data for multiple KDE plots (this is the key!)
df = pd.melt(df, var_name='Year', value_name='Law')

## Set up plotting and formatting of viz
sns.set(style="white", rc={"axes.facecolor": (0, 0, 0, 0)})
font_h1 = {'family': 'monospace',
           'color': 'black',
           'weight': 'bold',
           'size': 16,
           'horizontalalignment': 'center'}
font_h2 = {'family': 'monospace',
           'color': 'black',
           'size': 14,
           'horizontalalignment': 'center'}
font_sub = {'family': 'monospace',
            'color': 'black',
            'weight': 'regular',
            'size': 10,
            'horizontalalignment': 'right'}

## Hey this looks cool
#sns.kdeplot(df, bw=0.4)


# Create axes for each Year, one row per Year
g = sns.FacetGrid(data=df,
                  row='Year',  # Determines which value to group by, in this case the different values in the 'Year' column
                  hue='Year',  # Similar to row. Enables the date labels on each subplot
                  aspect=18,   # Controls aspect ratio of entire figure
                  size=0.5,    # Controls vertical height of each subplot
                  palette=sns.color_palette("Set2", 1))  # Uses a nice green for the area

# Create KDE area plots
g.map(sns.kdeplot, 'Law', bw=bandwidth, clip_on=False, shade=True, alpha=1)

# Create KDE line plots to outline the areas
g.map(sns.kdeplot, 'Law', bw=bandwidth, clip_on=False, color='black')

# Create the psuedo x-axes
g.map(plt.axhline, y=0, lw=2, clip_on=False, color='black')

# Define and use a simple function to label the plot in axes coordinates
# https://seaborn.pydata.org/examples/kde_joyplot.html
def label(x, color, label):
    ax = plt.gca()
    ax.set_xlim([-2,4])
    ax.text(0, 0.07, 
            label,
            family='monospace',
            fontsize=12,
            color='black', 
            ha='left',
            va='center',
            transform=ax.transAxes)
g.map(label, 'Law')

# Overlap the plots to give the ridgeline effect
g.fig.subplots_adjust(hspace=-.7)

# Clean up axes and remove subplot titles
g.set_titles('')
g.set(yticks=[])
plt.xticks([0, 1, 2, 3], 
           ['Constitutional Ban',
            'Statutory Ban',
            'No Law',
            'Legal'],
            rotation=90,
            fontsize=12,
            fontname='monospace')
plt.xlabel('')
g.despine(bottom=True, left=True)

# Add titles and annotations
plt.text(1, 8.5,
         'State Same Sex Marriage Laws in the USA',
         fontdict=font_h1)
plt.text(1, 8.3,
         'Percent of states w/each law type from 1995-2015',
         fontdict=font_h2)
#plt.text(4, -1.8,
#         '© Aaron Penne 2018\nSource: Pew Research Center',
#         fontdict=font_sub)

g.savefig(os.path.join(output_dir, 'ssm_joy.png'), dpi=300, bbox_inches='tight')
