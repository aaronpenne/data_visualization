#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TITLE & DESCRIPTION

Author: Aaron Penne
Created: YYYY-MM-DD

Developed with:
    Python 3.6
    macOS 10.13
"""

import os
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['font.family'] = 'monospace'

###############################################################################
# Set up directories
code_dir = os.path.dirname(__file__)
data_dir = os.path.join(code_dir, 'data') 
output_dir = os.path.join(code_dir, 'output')
if not os.path.isdir(output_dir):
    os.mkdir(output_dir)
    
###############################################################################
# Wrangle and process data
    
# Get input data
input_file = os.path.join(data_dir, 'FILENAME.csv')
df = pd.read_csv(input_file)    
    
###############################################################################
# Create visualization
fig, ax = plt.subplots(figsize=(4, 6), dpi=200)

fig.savefig(os.path.join(output_dir, 'FILE.png'),
        dpi=fig.dpi,
        bbox_inches='tight',
        pad_inches=0.3)
plt.close(fig)