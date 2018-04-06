# try modis
# https://e4ftl01.cr.usgs.gov/MOLT/MOD13C1.006/2000.06.09/
# http://hdfeos.org/zoo/NSIDC/MOD10C1_Day_CMG_Snow_Cover.py

import os
import matplotlib as mpl
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import numpy as np
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import re

from mpl_toolkits.basemap import Basemap

FILE_NAME = 'MOD13C1.A2000161.006.2015147153014.hdf'

from pyhdf.SD import SD, SDC
hdf = SD(FILE_NAME, SDC.READ)

print(hdf.info())

datasets_dic = hdf.datasets()

for idx,sds in enumerate(datasets_dic.keys()):
    print(idx,sds)

# Read dataset.
data2D = hdf.select('CMG 0.05 Deg 16 days NDVI')
data = data2D[:,:].astype(np.float64)

# Read global attribute.
fattrs = hdf.attributes(full=1)
ga = fattrs["StructMetadata.0"]
gridmeta = ga[0]
    
# Read projection parameters. 
# The needed information is in a global attribute called 'StructMetadata.0'.  
# Use regular expressions to tease out the extents of the grid. 
ul_regex = re.compile(r'''UpperLeftPointMtrs=\(
                          (?P<upper_left_x>[+-]?\d+\.\d+)
                          ,
                          (?P<upper_left_y>[+-]?\d+\.\d+)
                          \)''', re.VERBOSE)
match = ul_regex.search(gridmeta)
x0 = np.float(match.group('upper_left_x')) / 1e6
y0 = np.float(match.group('upper_left_y')) / 1e6

lr_regex = re.compile(r'''LowerRightMtrs=\(
                          (?P<lower_right_x>[+-]?\d+\.\d+)
                          ,
                          (?P<lower_right_y>[+-]?\d+\.\d+)
                          \)''', re.VERBOSE)
match = lr_regex.search(gridmeta)
x1 = np.float(match.group('lower_right_x')) / 1e6
y1 = np.float(match.group('lower_right_y')) / 1e6
ny, nx = data.shape
xinc = (x1 - x0) / nx
yinc = (y1 - y0) / ny

# Construct the grid.  It's already in lat/lon.
x = np.linspace(x0, x0 + xinc*nx, nx)
y = np.linspace(y0, y0 + yinc*ny, ny)
lon, lat = np.meshgrid(x, y)


# Retrieve attributes.
attrs = data2D.attributes(full=1)
lna=attrs["long_name"]
long_name = lna[0]
aoa=attrs["add_offset"]
add_offset = aoa[0]
fva=attrs["_FillValue"]
_FillValue = fva[0]
sfa=attrs["scale_factor"]
scale_factor = sfa[0]        
ua=attrs["units"]
units = ua[0]


fig = plt.figure(dpi=1000)
m = Basemap(projection='cyl', resolution='l',
        llcrnrlat=-90, urcrnrlat = 90,
        llcrnrlon=-180, urcrnrlon = 180)
#m.arcgisimage(service='World_Shaded_Relief', xpixels = 1500, verbose= True)
#m.drawcoastlines(linewidth=0.1)
#m.drawparallels(np.arange(-90., 120., 30.), labels=[1, 0, 0, 0])
#m.drawmeridians(np.arange(-180, 180., 45.), labels=[0, 0, 0, 1])

# Render the image in the projected coordinate system.
m.pcolormesh(lon[::2,::2], lat[::2,::2], data[::2,::2],
             latlon=True, cmap='YlOrRd')

basename = os.path.basename(FILE_NAME)
plt.title('{0}\n{1}'.format(basename, long_name))
fig = plt.gcf()

# plt.show()
pngfile = "{0}.py.png".format(basename)
fig.savefig(pngfile)



