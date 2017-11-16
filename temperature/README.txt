                          USCRN/USRCRN SUBHOURLY FILES 
                          
                            UPDATED: 2017-07-06 

README CONTENTS:                          
    1. GENERAL INFORMATION
    2. DATA VERSION / STATUS UPDATES
    3. DIRECTORY / FILE ORGANIZATION
    4. DATA FIELDS / FORMATS / IMPORTANT NOTES

********************************************************************************

1. GENERAL INFORMATION

NCDC provides access to subhourly (5-minute) data from the U.S. Climate 
Reference Network / U.S. Regional Climate Reference Network (USCRN/USRCRN) via 
anonymous ftp at:

        ftp://ftp.ncdc.noaa.gov/pub/data/uscrn/products/subhourly01

and an identical web interface at:

        http://www1.ncdc.noaa.gov/pub/data/uscrn/products/subhourly01

Before using these data, be sure to review this document carefully, as well
as any announcements within the main (subhourly01) directory. 

********************************************************************************

2. DATA VERSION / STATUS UPDATES

Status and Version Information for U.S. Climate Reference Network Data

  ##########################
  
Version change:     2.1 to 2.1.1
Commencement Date:  2017-06-20
Completion Date:    2017-06-30
Variables impacted: Precipitation

    Effective June 30, 2017, recalculation using the Official Algorithm
for Precipitation (OAP) 2.1.1 has been completed. The purpose of this 
recalculation is described in Appendix A of the OAP 2.1 documentation:
https://www1.ncdc.noaa.gov/pub/data/uscrn/documentation/maintenance/2016-05/USCRN_OAP2.1.Description_PrecipChanges.pdf

  ##########################
  
Status change:      Correction
Correction Applied: 2017-05-01
Variables impacted: Precipitation for 3 stations
	
    From July 2016 until May 1, 2017, the precipitation values for 
the following stations and time periods were mistakenly missing on 
the website and in the FTP product files:
		NC Asheville 8 SSW          2004-05-01 to 2004-11-01 
		SC McClellanville 7 NE      2005-05-01 to 2005-11-01
		CA Stovepipe Wells 1 SW     2004-05-01 to 2005-06-01
Precipitation data for these stations/time periods that were downloaded
during the affected time period should be re-acquired. 

  ##########################
  
Version change:     2.0 to 2.1 
Commencement Date:  2016-05-12 
Completion Date:    2016-06-13
Variables impacted: Precipitation
                    Relative Humidity (RH)
                    Temperatures from RH Sensor
                    Thermometer Shield Aspiration Fan Speeds
                    Air Temperature (when fan speeds are low)
                      
    Beginning May 12, 2016, USCRN changed the current data set to 
version 2.1 from v2.0. This version change was retroactively applied to 
all USCRN/USRCRN stations for their period-of-record 5-minute measurements 
from 2016-05-12 until 2016-06-13. [Note that during this period of 
reprocessing, data on the website and in these FTP products contained 
a mixture of v2.0 and v2.1 values.]
    Version 2.1 includes minor precipitation algorithm changes and 
changes/additions to the quality control ranges for acceptable 
relative humidity (RH) values, temperatures measured with the 
RH sensors, and for the speed of the fans which are used to 
aspirate the air temperature sensors. For precipitation, the Official 
Algorithm for Precipitation (OAP) v2.1 was implemented which  
addresses a minor correction to v2.0 that guards against
overally large (> 0.3 mm) precipitation residuals from one hour 
being transferred to the next hour. Further information can be found at 
http://www.ncdc.noaa.gov/crn/documentation.html.

  ##########################
  
Version change:     1.0 to 2.0 
Commencement Date:  2015-08-17
Completion Date:    2015-09-15
Variables impacted: Precipitation

    The original Official Algorithm for Precipitation 
(OAP) version 1.0 was operational until August 17, 2015 and used a 
pairwise comparison and moving reference depth to calculate 
precipitation. Precipitation data accessed and/or downloaded 
prior to this date were calculated using OAP v1.0. 
    Beginning August 17, 2015, all precipitation data were 
calculated using a new processing algorithm, OAP v2.0. In addition, 
the v2.0 algorithm was retroactively applied to all USCRN/USRCRN 
stations for their periods of record (PORs) starting when 5-minute 
data began being collected. The reprocessing took approximately four
weeks to recalculate all station's existing values from v1.0 to v2.0
for their PORs and was completed on September 15, 2015. 
    OAP v2.0 marked a fundamental shift in the procedures used to calculate 
precipitation. The new algorithm uses a weighted average approach 
based on each sensor's noise level. It has greatly improved the 
network's capacity to detect lighter precipitation with greater 
confidence. For details, see Leeper et. al., 2015, 
(http://journals.ametsoc.org/doi/abs/10.1175/JTECH-D-14-00185.1) and
http://www.ncdc.noaa.gov/crn/documentation.html.

********************************************************************************

3. DIRECTORY / FILE ORGANIZATION

Subhourly01 data are divided into yearly subdirectories/files from 2006 through 
the present year. [Note to past users: prior to 2013-04-18, all subhourly 
data were stored in a single file, rather than separate yearly files.]
        
Yearly subdirectories contain a single ASCII text file for each USCRN/USRCRN 
station. Files list that station's subhourly data for the year and are 
typically updated each hour. Filenames use the following convention:

        CRNS01TT-MM-YYYY-${name}.txt

   CRNS01 = filename prefix to denote CRN Subhourly01 data 
       TT = 2-character file format number (currently 01)
       MM = interval of observation in minutes (currently 05)
     YYYY = 4-digit year
  ${name} = station name (state location vector) (e.g. AZ_Tucson_11_W)
  
    The 2-character sequence TT indicates the file format number and is updated 
    when the file format is changed.   
  
********************************************************************************

4. DATA FIELDS / FORMATS

Each station file contains fixed-width formatted fields with a single set of 
subhourly (5-minute) data per line. A summary table of the fields and a 
detailed listing of field definitions/column formats are shown below. 

Fortran users will find the column widths and counts useful. 

The file "HEADERS.txt", found in the subhourly01 directory, is designed to be 
prepended to the data for use with spreadsheet programs, data extraction tools 
(e.g. awk) or any other programming language. This file contains the following 
three lines:

    1. Field Number
    2. Field Name
    3. Unit of Measure

Please be sure to refer to the "Important Notes" section below for essential 
information.

All subhourly data are calculated over the 5-minute period *ending* at the 
UTC/LST times shown. Please note that the station's Local Standard Time is 
always used, regardless of its Daylight Savings status.  

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

   1    WBANNO  [5 chars]  cols 1 -- 5 
          The station WBAN number.

   2    UTC_DATE  [8 chars]  cols 7 -- 14 
          The UTC date of the observation.

   3    UTC_TIME  [4 chars]  cols 16 -- 19 
          The UTC time at the end of the 5-minute observation period. For example, 
          0420 designates the observational period starting just after 0415 
          and ending at 0420; and 0000 designates the last 5-minute period 
          of the previous day.

   4    LST_DATE  [8 chars]  cols 21 -- 28 
          The Local Standard Time (LST) date of the observation.

   5    LST_TIME  [4 chars]  cols 30 -- 33 
          The Local Standard Time (LST) time at the end of the 5-minute period 
          (see UTC_TIME description).

   6    CRX_VN  [6 chars]  cols 35 -- 40 
          The version number of the station datalogger program that was in 
          effect at the time of the observation. Note: This field should be 
          treated as text (i.e. string).

   7    LONGITUDE  [7 chars]  cols 42 -- 48 
          Station longitude, using WGS-84.

   8    LATITUDE  [7 chars]  cols 50 -- 56 
          Station latitude, using WGS-84.

   9    AIR_TEMPERATURE  [7 chars]  cols 58 -- 64 
          Average temperature, in degrees C. See Notes F and G.

   10   PRECIPITATION  [7 chars]  cols 66 -- 72 
          Total amount of precipitation, in mm. See Notes F and H.

   11   SOLAR_RADIATION  [6 chars]  cols 74 -- 79 
          Average global solar radiation received, in watts/meter^2.

   12   SR_FLAG  [1 chars]  cols 81 -- 81 
          QC flag for the average global solar radiation measurement. See Note 
          I.

   13   SURFACE_TEMPERATURE  [7 chars]  cols 83 -- 89 
          Average infrared surface temperature, in degrees C. See Note J.

   14   ST_TYPE  [1 chars]  cols 91 -- 91 
          The type of infrared surface temperature measurement: 'R' denotes 
          raw (uncorrected); 'C' denotes corrected; and 'U' is shown if the 
          type is unknown/missing. See Note J.

   15   ST_FLAG  [1 chars]  cols 93 -- 93 
          QC flag for the surface temperature measurement. See Note I.

   16   RELATIVE_HUMIDITY  [5 chars]  cols 95 -- 99 
          Relative humidity average, as a percentage. See Note K.

   17   RH_FLAG  [1 chars]  cols 101 -- 101 
          QC flag for the relative humidity measurement. See Note I.

   18   SOIL_MOISTURE_5  [7 chars]  cols 103 -- 109 
          Average soil moisture (volumetric water content in m^3/m^3) at 5 
          cm below the surface. See Note M.

   19   SOIL_TEMPERATURE_5  [7 chars]  cols 111 -- 117 
          Average soil temperature at 5 cm below the surface, in degrees C. 
          See Note M.

   20   WETNESS  [5 chars]  cols 119 -- 123 
          The presence or absence of moisture due to precipitation, in Ohms. 
          High values (>= 1000) indicate an absence of moisture.  Low values 
          (< 1000) indicate the presence of moisture.

   21   WET_FLAG  [1 chars]  cols 125 -- 125 
          QC flag for the wetness measurement. See Note I.

   22   WIND_1_5  [6 chars]  cols 127 -- 132 
          Average wind speed, in meters per second, at a height of 1.5 meters.

   23   WIND_FLAG  [1 chars]  cols 134 -- 134 
          QC flag for the wind speed measurement. See Note I.

    IMPORTANT NOTES:
        A.  All fields are separated from adjacent fields by at least one space.
        B.  Leading zeros are omitted.
        C.  Missing data are indicated by the lowest possible integer for a 
            given column format, such as -9999.0 for 7-character fields with 
            one decimal place or -99.000 for 7-character fields with three
            decimal places.
        D.  Subhourly data are calculated over the 5-minute period which *ends*
            at the time shown.
        E.  There are no quality flags for these derived quantities. When the 
            raw data are flagged as erroneous, these derived values are not 
            calculated, and are instead reported as missing. Therefore, these 
            fields may be assumed to always be good (unflagged) data, except 
            when they are reported as missing.
        F.  The 5-minute values reported in this dataset are calculated using 
            multiple independent measurements for temperature and precipitation. 
        G.  USCRN/USRCRN stations have multiple co-located temperature sensors 
            that make 10-second independent measurements used for the average. 
        H.  USCRN/USRCRN stations use a weighing bucket gauge outfitted with 
            three redundant, but independent, load cell sensors to monitor gauge
            depth. As a supplement, a disdrometer (wetness sensor) is used to 
            detect wetness. 
        I.  Quality control flags indicate the following: 0 denotes good data, 
            1 denotes field-length overflow, and 3 denotes erroneous data.
        J.  On 2013-01-07 at 1500 UTC, USCRN began reporting corrected surface 
            temperature measurements for some stations. These changes  
            impact previous users of the data because the corrected values 
            differ from uncorrected values. To distinguish between uncorrected 
            (raw) and corrected surface temperature measurements, a surface 
            temperature type field was added to the data product. The 
            possible values of the this field are "R" to denote raw surface 
            temperature measurements, "C" to denote corrected surface 
            temperature measurements, and "U" for unknown/missing.
        K.  All USCRN stations now report 5-minute relative humidity averages, 
            however the two Asheville, NC stations reported only hourly RH 
            values until 2007-02-22.
        L.  USRCRN stations do not measure solar radiation, surface temperature,
            relative humidity, wind speed or soil variables, so those fields 
            are shown as missing data.
        M.  USCRN stations have multiple co-located soil sensors that record 
            independent measurements. The soil values reported in this dataset 
            are calculated from these multiple independent measurements. Soil 
            moisture is the ratio of water volume over sample volume 
            (m^3 water/m^3 soil).
        N.  In accordance with Service Change Notice 14-25 from the National 
            Weather Service, NCDC stopped providing data from the 72 
            Southwest Regional Climate Reference Network (USRCRN) stations on 
            June 1, 2014. The historical data for these stations remain 
            available.