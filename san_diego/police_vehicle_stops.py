#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 10 14:08:31 2018

@author: aaronpenne
"""

import os
import pandas as pd
from datetime import datetime

code_dir = os.path.dirname(__file__)
output_dir = os.path.join(code_dir, 'output')
if not os.path.isdir(output_dir):
    os.mkdir(output_dir)
data_dir = os.path.join(code_dir, 'data', 'police_vehicle_stops') 
    

df_columns = ['stop_id', 
              'stop_cause', 
              'service_area', 
              'subject_race', 
              'subject_sex',
              'subject_age', 
              'timestamp',
              'stop_date', 
              'stop_time', 
              'sd_resident',
              'arrested', 
              'searched', 
              'obtained_consent', 
              'contraband_found',
              'property_seized']

# Concatenate all available data into single dataframe
df_dict = {}
csv_files = [f for f in os.listdir(data_dir) if f.endswith('.csv') and 'search' not in f]
csv_files.sort()
for i,f in enumerate(csv_files):
    tmp = pd.read_csv(os.path.join(data_dir, f), parse_dates=['timestamp'])
    # Only bring in standard columns (some years had extra unnamed cols)
    df_dict[i] = tmp[df_columns]
df = pd.concat([df_dict[0], df_dict[1], df_dict[2], df_dict[3]], ignore_index=True)
# Remove duplicate stops
df.drop_duplicates(subset='stop_id', inplace=True)

df_pivot = df.pivot_table(index=df['timestamp'].dt.hour,
                          columns=df['timestamp'].dt.dayofweek,
                          values='stop_id',
                          aggfunc='count')
