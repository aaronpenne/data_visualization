
# coding: utf-8

# ## Sources/References
# * [NOAA Quality Controlled Datasets](https://www.ncdc.noaa.gov/crn/qcdatasets.html)
#     * Using [5 minute data for 2016 at Yosemite Village, CA](ftp://ftp.ncdc.noaa.gov/pub/data/uscrn/products/subhourly01/2016/)
# 
# 
# 
# ## Temperature Heatmap

# In[1]:


import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


df = pd.read_csv('CRNS0101-05-2016-CA_Yosemite_Village_12_W.txt', 
                 header=None, 
                 sep='\s+',
                 dtype='str')
df.head(5)


# * The README.txt that accompanies this data lists the fields as below.
# * Gotta make sure to offset by 1 due to column indices
Field#  Name                           Units
---------------------------------------------
   1    WBANNO                         XXXXX
   2    UTC_DATE                       YYYYMMDD
   3    UTC_TIME                       HHmm
   4    LST_DATE                       YYYYMMDD
   5    LST_TIME                       HHmm
   6    CRX_VN                         XXXXXX
   7    LONGITUDE                      Decimal_degrees
   8    LATITUDE                       Decimal_degrees
   9    AIR_TEMPERATURE                Celsius
   10   PRECIPITATION                  mm
   11   SOLAR_RADIATION                W/m^2
   12   SR_FLAG                        X
   13   SURFACE_TEMPERATURE            Celsius
   14   ST_TYPE                        X
   15   ST_FLAG                        X
   16   RELATIVE_HUMIDITY              %
   17   RH_FLAG                        X
   18   SOIL_MOISTURE_5                m^3/m^3
   19   SOIL_TEMPERATURE_5             Celsius
   20   WETNESS                        Ohms
   21   WET_FLAG                       X
   22   WIND_1_5                       m/s
   23   WIND_FLAG                      X
# * The data I'm interested in is the local date, local time, and air temperature. 
# * Fields 4, 5, 9. Columns 3, 4, 8.

# In[3]:


data = df[[3,4,8]].copy()
data.columns=['date', 'time', 'temp_c']
data['temp_f'] = data['temp_c'].astype(float)*(9/5) + 32
data.head(5)


# In[4]:


data_pivot = data.pivot_table(values='temp_f',
                              index='time',
                              columns='date')
data_pivot.head(5)


# In[5]:


data_pivot.drop(['20151231','20161231'], axis = 1, inplace = True)


# In[6]:


test = data_pivot.describe()
test


# In[7]:


fig, ax = plt.subplots(figsize=(15, 10))
sns.heatmap(data_pivot, 
            ax=ax,
            vmin=0)


# ## Polar Plot
# * This heatmap doesn't really show the hot week/cold week cycle
# * Polar plot would be best for that

# In[8]:


data_day = data_pivot['20160606']
data_day.values


# In[11]:


theta = np.linspace(0,2*np.pi,len(data_day))
theta


# In[14]:


ax = plt.subplot(111, polar=True)
c = plt.scatter(theta, data_day.values)

