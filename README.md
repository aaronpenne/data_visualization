Data_Visualization
==================

This is a collection of my data visualizations, mostly made with Python.



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

<p align="center"><img src="https://github.com/aaronpenne/data_visualization/blob/master/same_sex_marriage/charts/ssm_violin_y_axis.gif" alt="State Same Sex Marriage Laws in the USA - Violin" width="70%"></p>

Code: [ssm_violin.py](https://github.com/aaronpenne/data_visualization/blob/master/same_sex_marriage/ssm_violin.py)

<p align="center"><img src="https://github.com/aaronpenne/data_visualization/blob/master/same_sex_marriage/charts/ssm_joy.png" alt="State Same Sex Marriage Laws in the USA - Joy" width="70%"></p>

Code: [ssm_joy.py](https://github.com/aaronpenne/data_visualization/blob/master/same_sex_marriage/ssm_joy.py)

Data: [Pew Research Center](http://www.pewforum.org/2015/06/26/same-sex-marriage-state-by-state/) via DataViz Battle Feb 2018

Contest: [r/DataIsBeautiful DataViz  Battle 2018-02](https://www.reddit.com/r/dataisbeautiful/comments/7vegvf/battle_dataviz_battle_for_the_month_of_february/)

Contest entry: [Reddit post - Honorable Mention](https://www.reddit.com/r/dataisbeautiful/comments/7zb8i4/same_sex_marriage_laws_in_the_usa_19952015_oc/dumpqzo/)



Annual Company Revenue vs. Annual CEO Compensation
--------------------------------------------------

<p align="center"><img src="https://github.com/aaronpenne/data_visualization/blob/master/ceo_compensation/charts/dot_pairs_ceo.png" alt="Annual Company Revenue vs. Annual CEO Compensation - Dot Pairs" width="90%"></p>

Code: [dot_pairs_ceo_compensation.py](https://github.com/aaronpenne/data_visualization/blob/master/ceo_compensation/dot_pairs_ceo_compensation.py)

Data: [Reddit post by u/k0m0d0z0](https://www.reddit.com/r/dataisbeautiful/comments/842tvn/highestpaid_ceos_in_america_oc/)



USA Population Rankings
-----------------------

<p align="center"><img src="https://raw.githubusercontent.com/aaronpenne/aaronpenne.github.io/master/data_viz/USA_Population_Rankings_1917-2017.jpg" alt="USA Population Rankings - Bump Chart" width="90%"></p>

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
