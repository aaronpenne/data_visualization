#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 23 07:33:30 2018

@author: aaronpenne
"""

import os
import pandas as pd
import numpy as np

code_dir = os.path.dirname(__file__)  # Returns full path of this script
data_dir = os.path.join(code_dir, 'data')
output_dir = os.path.join(code_dir, 'output')
if not os.path.isdir(output_dir):
    os.mkdir(output_dir)
    
df = pd.read_excel(os.path.join(data_dir, '2010.xlsx'))

# Thanks to colorbrewer2.org
colors = ['#ffffcc','#d9f0a3','#addd8e','#78c679','#41ab5d','#238443','#005a32']
total_max = 1000
bins = np.linspace(0, total_max, len(colors))

year = 2010
cols = [('TOTRATE', 'Concentration of 236 Religious Groups'),
       ('CATHRATE', 'Catholic'),
       ('MSLMRATE', 'Muslim')]
for col, name in cols:
    with open(os.path.join(data_dir, 'county_map.svg'), 'r') as f:
        svg = f.readlines()
    
    idx = [i for i, s in enumerate(svg) if '<style' in s or '</style' in s]
    svg_top = svg[:idx[0]+1]
    svg_bot = svg[idx[1]:]
    
    default = [s for s in svg[idx[0]:idx[1]] if '.counties' in s or '.State_' in s or '.separator' in s]

    style = []
    for val, fips in zip(df[col], df['FIPS']):
        color = colors[0]
        if val > bins[0]:
            color = colors[1]
        if val > bins[1]:
            color = colors[2]
        if val > bins[2]:
            color = colors[3]
        if val > bins[3]:
            color = colors[4]
        if val > bins[4]:
            color = colors[5]
        if val > bins[5]:
            color = colors[6]            
        style.append('.c{:05} {{fill:{}}}\n'.format(fips, color))
    
    # Annotation styles
    style.append('.title { font: 20px monospace; }')
    style.append('.subtitle { font: 15px monospace; }')
    style.append('.annotation { font: 10px monospace; }')
    
    # Annotations
    svg_bot.insert(1, '<text text-anchor="middle" x="660" y="20" class="title">{} in {}</text>'.format(name, year))
    svg_bot.insert(1, '<text text-anchor="middle" x="660" y="40" class="subtitle">Adherents per 1000 people</text>'.format(name))
    svg_bot.insert(1, '<text text-anchor="middle" x="660" y="605" class="annotation">Association of Religion Data Archives</text>')
    svg_bot.insert(1, '<text text-anchor="middle" x="660" y="615" class="annotation">Aaron Penne © 2018</text>')
    
    # Legend
    x = 600
    y = 550
    w = 15
    h = 15
    for i, color in enumerate(colors):
        svg_bot.insert(1, '<rect x="{}" y="{}" width="{}" height="{}" fill="{}"/>'.format(x+i*w, y, w, h, color))
    svg_bot.insert(1, '<text text-anchor="middle" x="660" y="540" class="annotation">Adherents/1000 people</text>')
    svg_bot.insert(1, '<text x="{}" y="{}" class="annotation">{}</text>'.format(x-10, y+10, 0))
    svg_bot.insert(1, '<text x="{}" y="{}" class="annotation">{}</text>'.format(x+i*w+20, y+10, total_max))
    
    out = svg_top + default + style + svg_bot
    with open(os.path.join(output_dir, name + '.svg'), 'w+') as f:
        f.writelines(out)