# -*- coding: utf-8 -*-
"""
Dot pairs plot of subset of National Statistics by Parent Income Percentile, Gender, and Race 
http://www.equality-of-opportunity.org/data/

Author: Aaron Penne
Created: 2018-03-20

Developed with:
    Python 3.6
    Windows 10
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Set output directory, make it if needed
output_dir = os.path.relpath('output')
if not os.path.isdir(output_dir):
    os.mkdir(output_dir)

# Get input data
input_file = os.path.join('data', 'race_and_wealth.txt')
df = pd.read_csv(input_file)

total = df['white'] + df['black']
pct_white = df['white']/total*100
pct_black = df['black']/total*100


fig, ax = plt.subplots(figsize=(5, 5), dpi=150)

for i in df.index:
    x = [pct_white[i], pct_black[i]]
    y = [i, i]
    print(x, y)
    plt.plot(x, y,
             color='gray',
             linestyle='-',
             linewidth=1)
    if x[0] > x[1]:
        plt.text(x[0]+4, y[0], '{:.0f}%'.format(pct_white[i]), horizontalalignment='left', verticalalignment='center')
        plt.text(x[1]-4, y[1], '{:.0f}%'.format(pct_black[i]), horizontalalignment='right', verticalalignment='center')
    else:
        plt.text(x[0]-4, y[0], '{:.0f}%'.format(pct_white[i]), horizontalalignment='right', verticalalignment='center')
        plt.text(x[1]+4, y[1], '{:.0f}%'.format(pct_black[i]), horizontalalignment='left', verticalalignment='center')
    
# Plot white
x = pct_white
y = df.index
plt.plot(x, y,
         color='#65C2A5',
         linestyle='None',
         marker='o',
         markersize=7,
         fillstyle='full')

# Plot black
x = pct_black
y = df.index
plt.plot(x, y,
         color='#FC8D62',
         linestyle='None',
         marker='o',
         markersize=7,
         fillstyle='full')

# Despine
for side in ['right', 'left', 'top', 'bottom']:
    ax.spines[side].set_visible(False)

plt.ylim([-1, 6])
plt.xlim([0, 100])
plt.yticks(np.linspace(0,4,5))
plt.xticks(range(0,101,25), color='gray')
ax.set_yticklabels(df['class'])

#plt.text(-50, 12, 'What economic class do wealthy kids end up in as adults?',
#         horizontalalignment='left',
#         size=16,
#         weight='bold')
#plt.text(-50, 11, 'Black adults that were raised wealthy vs.',
#         horizontalalignment='left',
#         color='#FC8D62',
#         size=14)
#plt.text(42, 11, 'White adults that were raised wealthy',
#         horizontalalignment='left',
#         color='#65C2A5',
#         size=14)
#plt.text(-50, -3, '© 2018 Aaron Penne\nSource: u/k0m0d0z0',
#         horizontalalignment='left',
#         color='gray',
#         size=8)

# Reveal
plt.show()

# Save
fig.savefig(os.path.join(output_dir, 'dot_pairs_race_wealth.png'),
            dpi=fig.dpi,
            bbox_inches='tight',
            pad_inches=0.3)