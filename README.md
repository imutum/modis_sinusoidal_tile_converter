# modis_sinusoidal_tile_converter
 A simple Python tool for converting geographic coordinates into MODIS (Moderate-Resolution Imaging Spectroradiometer) tile numbers.
## Install
```
# Run in the console
pip install modis_sinusoidal_tile_converter
```
## Usage
```
# Open python
python
>>> from modis_sinusoidal_tile_converter import Sinusoidal
>>> Sinusoidal.get_bounding_coordinates_of_sinusoidal_tiles(4, 24) # display bounding coordinates
(40.0, 50.0, 78.32443735993672, 108.90066788022885)
>>> Sinusoidal.gc2rc(50.0, 93.34342961162473)
(6671703.118599138, 5559752.598832616)
>>> Sinusoidal.rc2gc(6671703.118599138, 5559752.598832616)
(50.0, 93.34342961162473)
>>> Sinusoidal.gc2tcnum(50.0, 93.34342961162473)
(4, 24, -0.5, -0.5000000000008527)
>>> Sinusoidal.tcnum2gc(4, 24, -0.5, -0.5)
(50.0, 93.34342961162473)
```
## Resources
```MODIS_Sinusoidal_Tile_Grid_Corner_Coordinates.csv```
# References
- [MODLAND_grid](https://modis-land.gsfc.nasa.gov/MODLAND_grid.html)  
- [MODLAND Tile Calculator](https://landweb.modaps.eosdis.nasa.gov/cgi-bin/developer/tilemap.cgi)