# -*- coding: utf-8 -*-
"""
Attempting to improve this: https://www.reddit.com/r/dataisbeautiful/comments/842tvn/highestpaid_ceos_in_america_oc/

Author: Aaron Penne
Created: 2018-03-13

Developed with:
    Python 3.6
    Windows 10
"""

import pandas as pd
import matplotlib.pyplot as plt
import os

# Set output directory, make it if needed
output_dir = os.path.realpath(r'C:\tmp\ceo')  # Windows machine
if not os.path.isdir(output_dir):
    os.mkdir(output_dir)

# Get input data
input_file = os.path.realpath(r'C:\tmp\data_ceo_compensation.txt')
df = pd.read_csv(input_file)
df = df.sort_values(['annual_compensation'])
df = df.reset_index(drop=True)

# Normalize to M and B
df['annual_compensation'] = df['annual_compensation']/1000000
df['annual_revenue'] = df['annual_revenue']/1000000000


fig, ax = plt.subplots(figsize=(8, 6), dpi=150)

for i in df.index:
    x = [df.loc[i,'annual_compensation'], df.loc[i, 'annual_revenue']]
    y = [i, i]
    print(x, y)
    plt.plot(x, y,
             color='gray',
             linestyle='-',
             linewidth=1)
    if x[0] > x[1]:
        plt.text(x[0]+4, y[0], df.loc[i, 'ceo'], horizontalalignment='left', verticalalignment='center', weight='bold')
        plt.text(x[1]-4, y[1], df.loc[i, 'company'], horizontalalignment='right', verticalalignment='center')
    else:
        plt.text(x[0]-4, y[0], df.loc[i, 'ceo'], horizontalalignment='right', verticalalignment='center', weight='bold')
        plt.text(x[1]+4, y[1], df.loc[i, 'company'], horizontalalignment='left', verticalalignment='center')
    
# Plot revenue
x = df.loc[:,'annual_compensation']
y = df.index
plt.plot(x, y,
         color='#65C2A5',
         linestyle='None',
         marker='o',
         markersize=7,
         fillstyle='full')

# Plot company
x = df.loc[:,'annual_revenue']
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

plt.ylim([-1, 13])
plt.xlim([-50, 150])
plt.xticks(range(0,101,10), color='gray')
ax.set_yticklabels('')

plt.text(-50, 12, 'Annual Company Revenue and Annual CEO Compensation',
         horizontalalignment='left',
         size=16,
         weight='bold')
plt.text(-50, 11, 'Company revenue is in $Billions.',
         horizontalalignment='left',
         color='#FC8D62',
         size=14)
plt.text(42, 11, 'CEO compensation is in $Millions.',
         horizontalalignment='left',
         color='#65C2A5',
         size=14)
plt.text(-50, -3, '© 2018 Aaron Penne\nSource: u/k0m0d0z0',
         horizontalalignment='left',
         color='gray',
         size=8)

# Reveal
plt.show()

# Save
fig.savefig(os.path.join(output_dir, 'dot_pairs_ceo.png'),
            dpi=fig.dpi,
            bbox_inches='tight',
            pad_inches=0.3)