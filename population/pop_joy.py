#
# Author: Aaron Penne
#
# Created: 02-22-2018
#
# Source: US Census Bureau
#         https://www.census.gov/data/datasets/2017/demo/popest/state-detail.html
#         https://www2.census.gov/programs-surveys/popest/datasets/2010-2016/state/asrh/sc-est2016-agesex-civ.csv
# 

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

## Define globals
bandwidth = 1.3
input_file = 'C:\\tmp\\sc-est2016-agesex-civ_tidy.csv'
output_dir = 'C:\\tmp\\output_pop_joy\\'
if not os.path.isdir(output_dir):
    os.mkdir(output_dir)
    
## Read in CSV
df = pd.read_csv(input_file)
# Get unique state names
all_states = pd.unique(df.loc[:,"name"])
# Scale population down to make this hacky method manageable
df["pop"] = round(df.loc[:,"pop_2016"]/1000)
df["pop"] = df["pop"].apply(int)

# Frequencies are given in data, need to expand to counts
state_list = []
age_list = []
for state in all_states:
    state_index = df.loc[:,"name"]==state
    state_list = state_list + [state]*sum(df[state_index].loc[:,"pop"])
    for i in list(df[state_index].index):
        age_list = age_list + [df[state_index].loc[i,"age"]]*df[state_index].loc[i,"pop"]

# Create dataframe from count lists    
df_counts = pd.DataFrame({'state': state_list, 
                          'age': age_list})

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

# Create axes for each Year, one row per Year
g = sns.FacetGrid(df_counts,
                  row='state',  # Determines which value to group by, in this case the different values in the 'Year' column
                  hue='state',  # Similar to row. Enables the date labels on each subplot
                  aspect=18,   # Controls aspect ratio of entire figure
                  size=0.5,    # Controls vertical height of each subplot
                  palette=sns.color_palette("Set2", 1))  # Uses a nice green for the area

# Create KDE area plots
g.map(sns.kdeplot, 'age', bw=bandwidth, clip_on=False, shade=True, alpha=1)

# Create KDE line plots to outline the areas
g.map(sns.kdeplot, 'age', bw=bandwidth, clip_on=False, color='black')

# Create the psuedo x-axes
g.map(plt.axhline, y=0, lw=2, clip_on=False, color='black')

## Define and use a simple function to label the plot in axes coordinates
## https://seaborn.pydata.org/examples/kde_joyplot.html
#def label(x, color, label):
#    ax = plt.gca()
#    ax.set_xlim([-2,4])
#    ax.text(0, 0.07, 
#            label,
#            family='monospace',
#            fontsize=12,
#            color='black', 
#            ha='left',
#            va='center',
#            transform=ax.transAxes)
#g.map(label, 'Law')

# Overlap the plots to give the ridgeline effect
g.fig.subplots_adjust(hspace=-.7)

# Clean up axes and remove subplot titles
g.set_titles('')
g.set(yticks=[])
#plt.xticks([0, 1, 2, 3], 
#           ['Constitutional Ban',
#            'Statutory Ban',
#            'No Law',
#            'Legal'],
#            rotation=90,
#            fontsize=12,
#            fontname='monospace')
plt.xlabel('')
g.despine(bottom=True, left=True)

## Add titles and annotations
#plt.text(1, 8.5,
#         'State Same Sex Marriage Laws in the USA',
#         fontdict=font_h1)
#plt.text(1, 8.3,
#         'Percent of states w/each law type from 1995-2015',
#         fontdict=font_h2)
#plt.text(4, -1.8,
#         '© Aaron Penne 2018\nSource: Pew Research Center',
#         fontdict=font_sub)
#
#g.savefig('{0}ssm_joy.png'.format(output_dir), dpi=300, bbox_inches='tight')
