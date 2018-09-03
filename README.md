This is a collection of my data visualizations, mostly made with Python.

Mapping Religion
----------------
![religion map](https://raw.githubusercontent.com/aaronpenne/data_visualization/master/religion/charts/total_2010.png)

This was created as an example of 'coloring in' a premade SVG file. The SVG map of US counties was obtained from [Wikimedia](https://commons.wikimedia.org/wiki/File:Usa_counties_large.svg)

Code: [religion_county.py](https://github.com/aaronpenne/data_visualization/blob/master/religion/religion_county.py)

Data: [The Association of Religion Data Archives](http://www.thearda.com/Archive/browse.asp)


Bird Seed Preferences
---------------------
<p align="center"><img src="https://raw.githubusercontent.com/aaronpenne/data_visualization/master/birds/charts/birdseed.png" alt="birdseed charts" width="60%"></p>

The July 2018 r/DataIsBeautiful competition was based around improving a grid heatmap [type of chart](https://i.imgur.com/RicYHQ3.jpg). If this was for work, those would be regular bar charts, but this was an exercise in coercing `matplotlib` into plotting bar charts on polar coordinates.

Code: [polar_multiples.py](https://github.com/aaronpenne/data_visualization/blob/master/birds/polar_multiples.py)

Data: Hardcoded from [this image](https://i.imgur.com/RicYHQ3.jpg)

Subreddit Traffic
-----------------
<p align="center"><img src="https://github.com/aaronpenne/data_visualization/blob/master/subreddit_traffic/charts/dataisbeautiful_time.png" alt="dataisbeautiful time" width="60%"></p>
<p align="center"><img src="https://github.com/aaronpenne/data_visualization/blob/master/subreddit_traffic/charts/dataisbeautiful_day.png" alt="dataisbeautiful day" width="60%"></p>

'users_here' counts were scraped every 10 minutes from a few subreddits over the past couple weeks. Each subreddit has 3 charts: raw line chart, box plot by day of week, and box plot by 30 minute bins. Using this data, you could time posts, chat at peak times, etc. The janky but working [scraper is here](https://github.com/aaronpenne/upskill/tree/master/scrape). More charts for 15 or so [subreddits are here](https://github.com/aaronpenne/data_visualization/blob/master/subreddit_traffic/README.md).

Code: [traffic.py](https://github.com/aaronpenne/data_visualization/blob/master/subreddit_traffic/traffic.py)

Data: [Scraped every 10 minutes with simple script](https://github.com/aaronpenne/data_visualization/tree/master/traffic/data).

Religion of Nobel Prize Winners
-------------------------------
<p align="center"><img src="https://raw.githubusercontent.com/aaronpenne/data_visualization/master/nobel/charts/nobel_pop_bar.png" alt="Nobel Prize vs Population" width="60%"></p>

This bar chart was an exercise in replotting the 3D exploded pie chart that appeared [here](https://www.reddit.com/r/dataisbeautiful/comments/8fyp73/religion_of_nobel_prize_winners_between_1901_and/). Data is the same, but augmented with population data to show how certain religions are over/under represented.

Code: [nobel_pop_bar.py](https://github.com/aaronpenne/data_visualization/blob/master/nobel/nobel_pop_bar.py)

Data: [Nobel Prize data](https://commons.wikimedia.org/wiki/File:Religion_of_Nobel_Prize_winners_between_1901-2000.png) and [Global Population data](https://en.wikipedia.org/wiki/List_of_religious_populations) from Wikipedia

Cause of Death - Reality vs. Google vs. Media
---------------------------------------------
<p align="center"><img src="https://github.com/aaronpenne/data_visualization/blob/master/cause_of_death/charts/bar.gif" alt="Animated stacked bar chart - COD" width="60%"></p>

This animation is an expansion on the excellent write up by [Hasan Al-Jamaly](https://github.com/haljamaly), [Maximillian Siemers](https://github.com/phi1eas), [Owen Shen](https://github.com/owenshen24), and [Nicole Stone](https://github.com/stonecoldnicole) for a project in [Brad Voytek](https://twitter.com/bradleyvoytek)'s UCSD course. The writeup can be found here: https://owenshen24.github.io/charting-death/

Code: [bar_cod.py](https://github.com/aaronpenne/data_visualization/blob/master/cause_of_death/bar_cod.py)

Data: [Death: Reality vs. Reported](https://owenshen24.github.io/charting-death/)

Our Living Planet
-----------------

![EVI Animated Map](https://github.com/aaronpenne/data_visualization/blob/master/gis/vegetation/animation_evi_short.gif)

This GIF is shortened from the full dataset of 18 years to only 2 years due to file size restrictions. Full resolution videos from 2000-2018 are on YouTube.
- Normalized Difference Vegetation Index (NDVI) animation: https://youtu.be/OK_HI3sjbtI
- Enhanced Vegetation Index (EVI) animation: https://youtu.be/UytH99Zc2L8

*All credit for the imagery products go to the NASA MODIS Science Team. I only collected the images into animations and annotated them.*

Code: [modis_vegetation.py](https://github.com/aaronpenne/data_visualization/blob/master/gis/vegetation/modis_vegetation.py)

Data: NASA MODIS Sensor on Terra Satellite [LP DAAC](https://lpdaac.usgs.gov/dataset_discovery/modis/modis_products_table/mod13c1_v006)


The Night Sky (HYG Database)
----------------------------

<p align="center"><img src="https://github.com/aaronpenne/data_visualization/blob/master/hyg_stellar_database/charts/hyg_scatter_twinkle.gif" alt="HYG Scatter Plot Twinkling"></p>

Code: [hyg_scatter.py](https://github.com/aaronpenne/data_visualization/blob/master/hyg_stellar_database/hyg_scatter.py)

Data: [HYG Stellar Database v3](https://github.com/astronexus/HYG-Database)

Contest: [r/DataIsBeautiful DataViz  Battle 2018-03](https://www.reddit.com/r/dataisbeautiful/comments/825mg6/battle_dataviz_battle_for_the_month_of_march_2018/)



State Same Sex Marriage Laws in the USA
---------------------------------------

<p align="center"><img src="https://github.com/aaronpenne/data_visualization/blob/master/same_sex_marriage/charts/ssm_violin_y_axis.gif" alt="State Same Sex Marriage Laws in the USA - Violin" width="60%"></p>

Code: [ssm_violin.py](https://github.com/aaronpenne/data_visualization/blob/master/same_sex_marriage/ssm_violin.py)

<p align="center"><img src="https://github.com/aaronpenne/data_visualization/blob/master/same_sex_marriage/charts/ssm_joy.png" alt="State Same Sex Marriage Laws in the USA - Joy" width="50%"></p>

Code: [ssm_joy.py](https://github.com/aaronpenne/data_visualization/blob/master/same_sex_marriage/ssm_joy.py)

Data: [Pew Research Center](http://www.pewforum.org/2015/06/26/same-sex-marriage-state-by-state/) via DataViz Battle Feb 2018

Contest: [r/DataIsBeautiful DataViz  Battle 2018-02](https://www.reddit.com/r/dataisbeautiful/comments/7vegvf/battle_dataviz_battle_for_the_month_of_february/)

Contest entry: [Reddit post - Honorable Mention](https://www.reddit.com/r/dataisbeautiful/comments/7zb8i4/same_sex_marriage_laws_in_the_usa_19952015_oc/dumpqzo/)



Annual Company Revenue vs. Annual CEO Compensation
--------------------------------------------------

<p align="center"><img src="https://github.com/aaronpenne/data_visualization/blob/master/ceo_compensation/charts/dot_pairs_ceo.png" alt="Annual Company Revenue vs. Annual CEO Compensation - Dot Pairs" width="70%"></p>

Code: [dot_pairs_ceo_compensation.py](https://github.com/aaronpenne/data_visualization/blob/master/ceo_compensation/dot_pairs_ceo_compensation.py)

Data: [Reddit post by u/k0m0d0z0](https://www.reddit.com/r/dataisbeautiful/comments/842tvn/highestpaid_ceos_in_america_oc/)



USA Population Rankings
-----------------------

<p align="center"><img src="https://github.com/aaronpenne/data_visualization/blob/master/population/charts/USA_Population_Rankings_1917-2017.jpg" alt="USA Population Rankings - Bump Chart" width="80%"></p>

Code: [pop_joy.py](https://github.com/aaronpenne/data_visualization/blob/master/population/pop_joy.py)

Data (raw): https://census.gov/data/tables/time-series/demo/popest/pre-1980-state.html

Data (manually aggregated/cleaned): [USA_Population_of_States_US_Census_Intercensal_Tables_1917-2017.csv](https://github.com/aaronpenne/aaronpenne.github.io/blob/master/data_viz/USA_Population_of_States_US_Census_Intercensal_Tables_1917-2017.csv)



USA Births Per Month
--------------------

The parts that stand out to me are the two big bumps 9 months after Pearl Harbor and 9 months after the war ended in Sep 1945. Those bumps are so big that the full chart pretty much only shows Baby Boomers.

<p align="center"><img src="https://github.com/aaronpenne/data_visualization/blob/master/birth_rate/charts/birth_rate_heat_usa.png" alt="Births Per Month in the USA - Heat Map" width="90%"></p>

<p align="center"><img src="https://github.com/aaronpenne/data_visualization/blob/master/birth_rate/charts/birth_rate_usa_line.png" alt="Births Per Month in the USA - Line Chart" width="90%"></p>

<p align="center"><img src="https://github.com/aaronpenne/data_visualization/blob/master/birth_rate/charts/birth_rate_usa_box.png" alt="Births Per Month in the USA - Box Plot" width="90%"></p>

<p align="center"><img src="https://github.com/aaronpenne/data_visualization/blob/master/birth_rate/charts/birth_rate_usa_heat_ranged.png" alt="Births Per Month in the USA - Heat Map (Ranged)" width="70%"></p>

Code: [birth_heatmap.py](https://github.com/aaronpenne/data_visualization/blob/master/birth_rate/birth_heatmap.py)


Birth data: [Human Mortality Database](http://www.mortality.org/cgi-bin/hmd/hmd_download.php)

Population data: [US Census Bureau](https://census.gov/data/tables/time-series/demo/popest/pre-1980-state.html)

Population data (aggregated): [USA_Population_of_States_US_Census_Intercensal_Tables_1917-2017.csv](https://github.com/aaronpenne/data_visualization/blob/master/population/data/USA_Population_of_States_US_Census_Intercensal_Tables_1917-2017.csv)
