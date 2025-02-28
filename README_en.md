# MODIS Sinusoidal Tile Converter

[简体中文](./README.md) | **English**

![Python](https://img.shields.io/badge/Python-3.1%2B-blue) ![License](https://img.shields.io/badge/License-MIT-green)

## 📌 Introduction
The **MODIS Sinusoidal Tile Converter** is a Python tool for transforming geographic coordinates into the MODIS (Moderate-Resolution Imaging Spectroradiometer) sinusoidal tiling system.

### ✨ Features
- Convert between Geographic (GCS), Projected (PCS), and MODIS Tile (ICSTile) coordinate systems.
- Generate MODIS sinusoidal projection-based TIFF files.
- Predefined MODIS tile parameters ensure accurate transformations.

## 📌 Coordinate System Parameter Explanation
1. **GCS: Geographic Coordinate System**
   - A spherical coordinate system representing a point’s position on Earth using latitude and longitude.
   - (lat, lon), where lat indicates north-south direction, and lon indicates east-west direction.

2. **PCS: Projected Coordinate System**
   - A coordinate system representing a point’s position in meters.
   - (x, y), where x represents east-west direction, and y represents north-south direction.

3. **ICSTile: Tile/Image Coordinates System**
   - A tiling/image coordinate system defined by tile numbers:
     - **Vertical tile number (vertical_tile)**: 0 to 17.
     - **Horizontal tile number (horizontal_tile)**: 0 to 35.
     - **Vertical line number (line)**: -0.5 to 1199.5 (1km) / 2399.5 (500m).
     - **Horizontal column number (sample)**: -0.5 to 1199.5 (1km) / 2399.5 (500m).

4. **ICSGeo: Geographic Tile/Image Coordinate System**
   - A tiling/image coordinate system represented by latitude and longitude:
     - **Latitude (lat_tile)**: -90 to 90.
     - **Longitude (lon_tile)**: -180 to 180.


## 🚀 Installation
Install via pip:
```bash
pip install modis_sinusoidal_tile_converter
```

## 📖 Usage
### 🔹 Coordinate Conversion
Convert between geographic, projected, and MODIS tile coordinates:
```python
from modis_sinusoidal_tile_converter import Sinusoidal

# Geographic to Projected
Sinusoidal.GCS2PCS(50.0, 93.34342961162473)
# Output: (6671703.118599138, 5559752.598832616)

# Projected to Geographic
Sinusoidal.PCS2GCS(6671703.118599138, 5559752.598832616)
# Output: (50.0, 93.34342961162473)

# Geographic to MODIS Tile
Sinusoidal.GCS2ICSTile(50.0, 93.34342961162473)
# Output: (4, 24, -0.5, -0.5)
```

### 🔹 File Format Conversion
Convert a NumPy array into a georeferenced MODIS sinusoidal TIFF file:
```python
import numpy as np
from modis_sinusoidal_tile_converter.convert import array2tiff

data = np.zeros((1200, 1200), dtype=np.uint16)
array2tiff(data, "h26v05.tiff", hv="h26v05", grid="1km")
```

## 📌 Projection Parameters
- **1km Grid**: Resolution of 926.625 meters per pixel.
- **500m Grid**: Resolution of 463.312 meters per pixel.
- **Tile System**: Defined by horizontal (`hXX`) and vertical (`vXX`) tile indices.

## 📂 Resources
To generate **MODIS_Sinusoidal_Tile_Grid_Corner_Coordinates.csv**:
```bash
python scripts/get_corner_coordinates_of_modis_sinusoidal_tile.py **/*.hdf
```

## 📜 License
This project is licensed under the **MIT License**.

## 🔗 References
- [MODIS Land Grid](https://modis-land.gsfc.nasa.gov/MODLAND_grid.html)
- [MODIS Tile Calculator](https://landweb.modaps.eosdis.nasa.gov/cgi-bin/developer/tilemap.cgi)
