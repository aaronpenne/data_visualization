
# coding: utf-8

# # Births in the USA
# 
# 
# ## Context
# * Tired but can't sleep in a hotel on work travel to Pt. Mugu. 
# * Wife thinks it sounds like traveling to Mt. Snoob.
# * "Reading" an audiobook on the drive that all the cool kids read: [*Thinking Fast and Slow* by Daniel Kahneman](https://www.amazon.com/Thinking-Fast-Slow-Daniel-Kahneman/dp/0374533555)
# * Always been interested in raw data behind psych studies, also frequently think about how great it would be if the results from these amazing studies were readily available and widespread among the normies like me.
# * Hey let's find some data from studies. Turns out it's called **secondary data**. Google finds tons of goodies to play with, including [Berkeley's link collection](http://guides.lib.berkeley.edu/publichealth/healthstatistics/rawdata).
# * [Human Mortality Database](http://www.mortality.org/cgi-bin/hmd/hmd_download.php) sounds morbid enough for tonight. Turns out they have a metric shit ton of data on 30+ countries. Births is on there. Less morbid than mortality I suppose.
# * Downloaded the USA data cause I live there.
# 
# ## The Data
# * I don't understand what the heck I just downloaded. The file tree looks like it's got a couple database types, a bunch of summary text files, some PDFs, dirs named old-old-old, etc. 
# * Inside the InputDB dir there's a text file called USAbirthbymonth.txt. I bet I can guess what's in here.
# * No need to guess... 
    PopName,Area,Year,YearReg,Month,Vital,RefCode,Access,Births,Note1,Note2,Note3,LDB
    USA,02,1933,1933,1,1,17,O,180545,.,.,.,1
    USA,02,1933,1933,2,1,17,O,165986,.,.,.,1
    USA,02,1933,1933,3,1,17,O,183762,.,.,.,1
# * Already cool. Immediately only care about 3 columns: Year, Month, Births
# * I'll investigate the other ones later, maybe.
# 
# ## Exploration

# In[222]:

import pandas as pd
import numpy as np
import seaborn as sns
get_ipython().magic('pylab inline')
pylab.rcParams['figure.figsize'] = (30, 4)

df = pd.read_csv('USAbirthbymonth.txt')
df.head(15)


# * Well hey it worked. Excellent...
# * Looks like the data has a subtotal every year. That's annoying, let's kill it.
# 
# 
# * [Looks like isin will get us there.](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.isin.html)
# * And we can index using [this nice example.](https://pandas.pydata.org/pandas-docs/stable/indexing.html#indexing-with-isin)
# * [And this answer takes us all the way.](https://stackoverflow.com/a/22485573)
# * Gotta assign that bad boy to a new variable. 
#     * I'll save off the original DataFrame just in case.

# In[223]:

df_BAK = df
df = df[~df.Month.isin(['TOT'])]
df[10:14]


# * Heck yeah!
# 
# 
# * Okay, let's put this into a heatmap 2D format:
#     * One year per row starting with 1933 (or the first year in the dataset)
#     * One month per column starting with 1
# * ~~Use the [length of the index column to count rows](https://stackoverflow.com/questions/15943769/how-do-i-get-the-row-count-of-a-pandas-dataframe)~~
# * ~~Use [itertuples](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.itertuples.html#pandas.DataFrame.itertuples)~~
# * Duh make a [pivot table](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.pivot_table.html)
# * Gotta fix the [leading zero ordering](https://stackoverflow.com/a/36346221) FIXME
# 

# In[224]:

df_pivot = pd.pivot_table(df, index='Month', columns='Year', values='Births', aggfunc=np.sum)
months = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
df_pivot_sorted = df_pivot.reindex_axis(months, axis=0)
df_pivot_sorted.loc[:'5',:'1940']


# * It worked.
# 
# 
# ## Visualization
# 
# * Now the whole friggin point is to make a chart. 

# In[225]:

ax = plt.axes()
sns.heatmap(df_pivot_sorted,
            ax = ax,
            yticklabels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
            cmap="magma",
            vmin=150000,
            vmax=400000,
            square=True,
            cbar=True)
ax.set_title('Number of Births in the USA per Month (1933-2015)',
            fontsize=20)
ax.set_xlabel('Year', fontsize=16)
ax.set_ylabel('')


# * Awwww yeahhhh
# 
# ## Conclusion
# 
# * Purely a quick-and-dirty visual analysis, statistics aren't good for me when I'm sleepy so I'll come back to that. FIXME
# * That baby boomer spike is so nicely timed with WWII that it's amazing. The war ended on September 2, 1945 and nine months later is June 1946, precisely when the births start **heating** up.
# * Big drop off from 1971-ish through 1978-ish. Curious to see what war/economy/politics were going on then.
# * July through October has higher birth months, likely due to more banging during the winter.
# * February has a streak of low numbers, wonder if the shorter number of days is a contributing factor?
# * November also has a low number sreak, which surprises me because I figured 9 months after February (Valentine's Day) would have a spike.
# * Interesting trend up during 1942/1943... Starts increasing in August/September 1942 which is 9 months after the attack on Pearl Harbor (Dec 7, 1941). Possibly putting a bun in the oven before heading off to war?
# * Hey this is fun making guesses based on a chart!
# 
# 
# * Let's take a look at the describe() output for each month of the pivot table (transposed):

# In[226]:

df_describe = df_pivot_sorted.T.describe(percentiles=[0.5])

pd.set_option('display.float_format', lambda x: '%.0f' % x)
df_describe


# * Seeing this little table makes me want to plot more but it's time for bed. ...violin plots for each month? bar chart of monthly means?
