import os
import pandas as pd
import datetime
import matplotlib.pyplot as plt

df = pd.read_csv(os.path.join('data', 'lake_mendota.csv'))


df['year'] = df['close_year']
df['month'] = df['close_month']
df['day'] = df['close_day']
df['close_date'] = pd.to_datetime(df[['year', 'month', 'day']])

df['year'] = df['open_year']
df['month'] = df['open_month']
df['day'] = df['open_day']
df['open_date'] = pd.to_datetime(df[['year', 'month', 'day']])

df['days_delta'] = (df['open_date'] - df['close_date']).dt.days

fig = plt.figure()
plt.plot(df['close_date'], df['days_delta'])
plt.plot(df['open_date'], df['days_delta'])
