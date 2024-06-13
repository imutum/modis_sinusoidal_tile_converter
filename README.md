# modis_sinusoidal_tile_converter
 A simple Python tool for converting geographic coordinates system into MODIS (Moderate-Resolution Imaging Spectroradiometer) tile coordinates system.
## Introduction
MODIS sensor, some data uses this projection method

Conventional coordinate system parameter explanation:    

1. GCS: Geographic Coordinate System, a spherical coordinate system representing the position of a point on the ground in latitude and longitude, (lat, lon), with lat representing the north-south direction and lon representing the east-west direction.  

2. PCS: Projected Coordinate System, a coordinate system representing the position of a point on the ground usually in meters, (x, y), with x representing the east-west direction and y representing the north-south direction.  

Parameters of MODIS Sinusoidal Projection:  

3. ICSTile: Tile/Image Coordinates System, a tiling/image coordinate system represented by tile numbers:  
    * Vertical tile number (vertical_tile), with values ranging from 0 to 17;  
    * Horizontal tile number (horizontal_tile), with values ranging from 0 to 35;  
    * Vertical line number (line), with values ranging from -0.5 to 1199.5(1km)/2399.5(500m);  
    * Horizontal column number (sample), with values ranging from -0.5 to 1199.5(1km)/2399.5(500m);  

4. ICSGeo: Geographic Tile/Image Coordinate System, a tiling/image coordinate system represented by latitude and longitude:
    * Latitude (lat_tile), with values ranging from -90 to 90;  
    * Longitude (lon_tile), with values ranging from -180 to 180;

Note: 
- The pixel center coordinates at the top left corner of the tile are (0.0, 0.0), and the top left corner coordinates of the pixel are (-0.5, -0.5).
- Failure in high latitude regions.
## Install
```
# Run in the console
pip install modis_sinusoidal_tile_converter
```
## Usage
Open python, and some examples
### Coordinates Convert:  
```
>>> from modis_sinusoidal_tile_converter import Sinusoidal
>>> Sinusoidal.GCS2PCS(50.0, 93.34342961162473)
(6671703.118599138, 5559752.598832616)
>>> Sinusoidal.PCS2GCS(6671703.118599138, 5559752.598832616)
(50.0, 93.34342961162473)
>>> Sinusoidal.GCS2ICSTile(50.0, 93.34342961162473)
(4, 24, -0.5, -0.5)
>>> Sinusoidal.ICSTile2GCS(4, 24, -0.5, -0.5)
(50.0, 93.34342961162473)
```
### File Format Convert:
```
# write to sinusoidal tiff file
>>> import numpy as np
>>> from modis_sinusoidal_tile_converter.convert import array2tiff
>>> array2tiff(np.zeros((1200, 1200), dtype=np.uint16), "h26v05.tiff", hv="h26v06", grid="1km")
```
## Resources
```MODIS_Sinusoidal_Tile_Grid_Corner_Coordinates.csv```

How to get this file?
```
## the pattern “**” will match any files and zero or more directories, 
# subdirectories and symbolic links to directories
python scripts\get_corner_coordinates_of_modis_sinusoidal_tile.py **/*.hdf
``` 
# References
- [MODLAND_grid](https://modis-land.gsfc.nasa.gov/MODLAND_grid.html)  
- [MODLAND Tile Calculator](https://landweb.modaps.eosdis.nasa.gov/cgi-bin/developer/tilemap.cgi)
