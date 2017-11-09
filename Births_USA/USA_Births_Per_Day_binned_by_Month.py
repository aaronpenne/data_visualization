
# coding: utf-8

# # USA Births Per Day binned by Month (1933-2015)
# 
# ---
# 
# ## Context
# * Tired but can't sleep in a hotel on work travel to Pt. Mugu. 
# * Wife thinks it sounds like traveling to Mt. Snoob.
# * Looking for secondary data, Google finds tons of goodies to play with, including [Berkeley's link collection](http://guides.lib.berkeley.edu/publichealth/healthstatistics/rawdata).
# * [Human Mortality Database](http://www.mortality.org/cgi-bin/hmd/hmd_download.php) sounds morbid enough for tonight. Turns out they have a metric shit ton of data on 30+ countries. Births is on there. Less morbid than mortality I suppose.
# * Downloaded the USA data cause I live there.
# 
# ## The Data
# * I don't understand what the heck I just downloaded. The file tree looks like it's got a couple database types, a bunch of summary text files, some PDFs, dirs named old-old-old, etc. 
# * Inside the InputDB dir there's a text file called USAbirthbymonth.txt. I bet I can guess what's in here.
# * No need to guess... 

# ## Exploration
# 
# 
# * I opened up the csv in Excel to see what was going on. Nothing too crazy. 
# * I'll open it up here to investigate further.

# In[18]:

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
get_ipython().magic('matplotlib inline')

df = pd.read_csv('USAbirthbymonth.txt')
df.head(15)


# * Well hey it worked. Excellent...
# * Already cool. Immediately only care about 3 columns: Year, Month, Births
# * I'll investigate the other ones later, maybe.
# * Looks like the data has a subtotal every year. That's annoying, let's kill it.
# 
# 
# * [Looks like isin will get us there.](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.isin.html)
# * And we can index using [this nice example.](https://pandas.pydata.org/pandas-docs/stable/indexing.html#indexing-with-isin)
# * [And this answer takes us all the way.](https://stackoverflow.com/a/22485573)
# * Gotta assign that bad boy to a new variable. 
#     * I'll save off the original DataFrame just in case.

# In[19]:

df_BAK = df
df = df[~df.Month.isin(['TOT'])]
df[10:14]


# * Heck yeah!
# 
# 
# * Okay, let's put this into a heatmap 2D format:
#     * One month per row starting with 1
#     * One year per column starting with 1933
# * ~~Use the [length of the index column to count rows](https://stackoverflow.com/questions/15943769/how-do-i-get-the-row-count-of-a-pandas-dataframe)~~
# * ~~Use [itertuples](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.itertuples.html#pandas.DataFrame.itertuples)~~
# * Duh make a [pivot table](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.pivot_table.html)
# * Gotta fix the [leading zero ordering](https://stackoverflow.com/a/36346221) FIXME
# 

# In[20]:

df_pivot = pd.pivot_table(df, index='Month', columns='Year', values='Births', aggfunc=np.sum)
months = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
df_pivot = df_pivot.reindex_axis(months, axis=0)
df_pivot.head(12)


# * It worked. Nice.
# 
# ## Normalization
# 
# * HOWEVER, normalization is the key to make all this look nice.
# * As pointed out on Reddit, the number of days in a month can have a drastic affect, if only one day is missing (30 vs 31) then the count can be affected significantly.
# * To normalize, the # of births in a given month is divided by the number of days in that month.
# * To do this, I'm going to need a table that has the number of days for each month. I'm just going to make it manually in Excel using the info from here: https://landweb.modaps.eosdis.nasa.gov/browse/calendar.html

# In[21]:

df_days = pd.DataFrame.from_csv('days_of_month.txt')
df_days.head(12)


# * Great, notice the leap years
# 
# 
# * Want to rename the columns though after dividing the values...

# In[22]:

df_pivot.columns


# * Could not get my DataFrames to divide, just resulted in NaNs
# * Going to use values to do it, then go back to a DataFrame

# In[23]:

c = df_pivot.values / df_days.values
df_norm = pd.DataFrame(data=c, columns=df_pivot.columns, index=months)
df_norm


# 
# ## Visualization
# 
# * Now the whole friggin point is to make a chart. 

# In[26]:

sns.set()

fig, ax = plt.subplots(figsize=(12, 4))
cbar_ax = fig.add_axes([0.93, .33, .01, .33])
sns.heatmap(df_norm,
            ax = ax,
            cbar_ax = cbar_ax,
            yticklabels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
            xticklabels=2,
            vmin = 5500,
            vmax = 12500,
            cmap="gist_heat",
            square=True,
            cbar=True)
ax.set_xlabel('Year', 
            fontsize=16,
            fontname = 'Consolas')
ax.set_ylabel('')
ax.tick_params(axis='both', which='major', labelsize=9)
fig.set_facecolor('#f3f3f3') 


# Chart titles
ax.text(-3, 16,
        'USA Births Per Day binned by Month (1933-2015)',
        fontsize = 20,
        weight = 'bold',
        fontname = 'Consolas')
ax.text(-3, 14,
        'Calculated by dividing the count of births in a given month by the number of days in that month.',
        fontsize = 14,
        alpha = .85,
        fontname = 'Consolas')

# Chart footer
ax.text(-3, -7,
        '_____________________________________________________________________________________________________',
        fontsize = 14,
        color = 'grey',
        alpha = .77,
        fontname = 'Consolas')
ax.text(-3, -9,
        '© Aaron Penne',
        fontsize = 14,
        color = 'grey',
        alpha = .77,
        fontname = 'Consolas')
ax.text(63, -9,
        'Source: Human Mortality Database',
        fontsize = 14,
        color = 'grey',
        alpha = .77,
        fontname = 'Consolas')
fig.savefig('Rate_Births_Month_USA.jpg', dpi=200, bbox_inches='tight', pad_inches=.11)


# * Awwww yeahhhh
# 
# ## Conclusion
# 
# * Purely a quick-and-dirty visual analysis, statistics aren't good for me when I'm sleepy so I'll come back to that. FIXME
# * That baby boomer spike is so nicely timed with WWII that it's amazing. The war ended on September 2, 1945 and nine months later is June 1946, precisely when the births start **heating** up.
# * As pointed out by some Redditors, it is possible that 'echos' from the baby boomers show up every 20ish years.
# * Big drop off from 1971-ish through 1978-ish. Curious to see what war/economy/politics were going on then.
# * July through October has higher birth months, likely due to more banging during the winter.
# * February has a streak of low numbers, wonder if the shorter number of days is a contributing factor?
# * November also has a low number sreak, which surprises me because I figured 9 months after February (Valentine's Day) would have a spike.
# * Interesting trend up during 1942/1943... Starts increasing in August/September 1942 which is 9 months after the attack on Pearl Harbor (Dec 7, 1941). Possibly putting a bun in the oven before heading off to war?
# * Hey this is fun making guesses based on a chart!
# 
# 
# * Let's take a look at the describe() output for each month of the pivot table (transposed):

# In[25]:

df_describe = df_norm.T.describe(percentiles=[0.5])

pd.set_option('display.float_format', lambda x: '%.0f' % x)
df_describe


# * Seeing this little table makes me want to plot more but it's time for bed. ...violin plots for each month? bar chart of monthly means?
