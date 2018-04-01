Vegetation Index mapping with MODIS
===================================

Animations showing the vegetation indices of the earth from 2000 to the present. These animations are best viewed opened in their own windows.

*All credit for the imagery products go to the NASA MODIS Science Team. I only collected the images into animations and annotated them.*

![EVI Animated Map](https://github.com/aaronpenne/data_visualization/blob/master/gis/vegetation/animation_evi_short.gif)

![NDVI Animated Map](https://github.com/aaronpenne/data_visualization/blob/master/gis/vegetation/animation_ndvi_short.gif)

Background
----------

This data was collected by the Terra satellite with the MODIS sensor every 16 days since February 2000. The Climate Modeling Grid (CMG) resolution used here is 0.05 degrees. Each pixel of the original full resolution image products is equivalent to 5600 meters.

The GIF animations are downsampled to allow for file size restrictions. Full resolution video will be uploaded soon.

Enhanced Vegetation Index (EVI) is an improvement on the standard Normalized Difference Vegetation Index (NDVI). [The NASA Earth Observatry explains it well](https://earthobservatory.nasa.gov/Features/MeasuringVegetation/measuring_vegetation_4.php):

>Derived from state-of-the-art satellite data provided by the MODIS instrument, EVI improves on NDVI's spatial resolution, is more sensitive to differences in heavily vegetated areas, and better corrects for atmospheric haze as well as the land surface beneath the vegetation.

NDVI is calculated as:

```
        NIR - RED
NDVI = -----------
        NIR + RED
```

EVI (using MODIS-EVI constants) is calculated as:

```
                         NIR - RED
EVI = 2.5 * ------------------------------------
             NIR + (6 * RED) - (7.5 * BLUE) + 1
```

References
----------

Terra (EOS AM-1) Satellite
- [Official website](https://terra.nasa.gov/)
- [Wikipedia page](https://en.wikipedia.org/wiki/Terra_%28satellite%29)

The Moderate Resolution Image Spectroradiometer (MODIS)
- [Official website](https://modis.gsfc.nasa.gov/)
- [Wikipedia page](https://en.wikipedia.org/wiki/Moderate-resolution_imaging_spectroradiometer)

Data sourced from [NASA Land Processes Distributed Active Archive Center (LP DAAC)](https://lpdaac.usgs.gov/dataset_discovery/modis/modis_products_table/mod13c1_v006)


Todo List
---------
- [x] World visualization
- [x] Make the ocean dark \m/
- [x] Multithreading
- [ ] Pad top for title
- [ ] Break into functions
    - [ ] Handle folders/outputs/etc.
    - [ ] Download all new imagery with checks
    - [ ] Create circular legend animation
    - [ ] Month to month comparison
    - [ ] Process NDVI or EVI (add temp, etc.?)
    - [ ] Crop to box (continents)
    - [ ] Annotations during big events?
    - [ ] Resize imagery for GIF, create GIF
    - [ ] Resize imagery for MP4, create MP4
- [ ] Next steps
    - [ ] Overlay temp data on vegetation data with alphas?
