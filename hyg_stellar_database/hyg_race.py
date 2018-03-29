# -*- coding: utf-8 -*-
"""
Exploring star speed

Author: Aaron Penne
Created: 03/29/2018
Developed with Python 3.6 on macOS 10.13
"""
    
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import imageio
import os

#np.random.seed(1138)

min_mag = -20
max_mag = 20
vis_mag = 8
steps = 40
twinkles = 10

# Set output directory, make it if needed
output_dir = os.path.relpath('output')  # Windows machine
if not os.path.isdir(output_dir):
    os.mkdir(output_dir)

# Get input file
input_file = os.path.join('data', 'hygdata_v3.csv')
df = pd.read_csv(input_file)    

# Calculate speed given 3D vector
df['vec_mag'] = df['vx']*df['vx'] + df['vy']*df['vy'] + df['vz']*df['vz']
df['speed'] = np.sqrt(df['vec_mag'])
speed = df.loc[df['speed']!=0, 'speed']

plt.plot(range(len(speed)), speed.sort_values())
