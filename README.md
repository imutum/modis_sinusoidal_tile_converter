# MODIS 正弦投影瓦片转换工具

**中文** | [English Version](./README_en.md)

![Python](https://img.shields.io/badge/Python-3.1%2B-blue) ![License](https://img.shields.io/badge/License-MIT-green)

## 📌 介绍
**MODIS 正弦投影瓦片转换工具** 是一个 Python 库，用于在 MODIS（中分辨率成像光谱仪）数据所使用的不同坐标系统之间进行转换。

### ✨ 主要功能
- 在 **地理坐标系（GCS）**、**投影坐标系（PCS）** 和 **MODIS 瓦片坐标系（ICSTile）** 之间转换。
- 生成基于 MODIS 正弦投影的 TIFF 文件。
- 使用预定义的 MODIS 瓦片参数，确保转换的准确性。

## 📌 坐标系

1. **GCS: 地理坐标系**
   - 以经纬度表示地面点位置的球面坐标系。
   - (lat, lon)，lat 表示南北方向，lon 表示东西方向。

2. **PCS: 投影坐标系**
   - 以米为单位表示地面点位置的坐标系。
   - (x, y)，x 代表东西方向，y 代表南北方向。

3. **ICSTile: MODIS 瓦片坐标系统**
   - 用图块编号表示的平铺/影像坐标系：
     - **垂直图块编号 (vertical_tile)**，取值范围：0 ~ 17。
     - **水平图块编号 (horizontal_tile)**，取值范围：0 ~ 35。
     - **垂直行号 (line)**，取值范围：-0.5 ~ 1199.5（1km）/ 2399.5（500m）。
     - **水平列号 (sample)**，取值范围：-0.5 ~ 1199.5（1km）/ 2399.5（500m）。

4. **ICSGeo: 地理瓦片/影像坐标系统**
   - 用经纬度表示的平铺/影像坐标系：
     - **纬度 (lat_tile)**，取值范围：-90 ~ 90。
     - **经度 (lon_tile)**，取值范围：-180 ~ 180。

## 🚀 安装
使用 pip 进行安装：
```bash
pip install modis_sinusoidal_tile_converter
```

## 📖 使用方法
### 🔹 坐标转换
在不同的坐标系统之间进行转换：
```python
from modis_sinusoidal_tile_converter import Sinusoidal

# 地理坐标系 转 投影坐标系
Sinusoidal.GCS2PCS(50.0, 93.34342961162473)
# 输出: (6671703.118599138, 5559752.598832616)

# 投影坐标系 转 地理坐标系
Sinusoidal.PCS2GCS(6671703.118599138, 5559752.598832616)
# 输出: (50.0, 93.34342961162473)

# 地理坐标系 转 MODIS 瓦片坐标系
Sinusoidal.GCS2ICSTile(50.0, 93.34342961162473)
# 输出: (4, 24, -0.5, -0.5)
```

### 🔹 文件格式转换
将 NumPy 数组转换为带有 MODIS 正弦投影的 TIFF 文件：
```python
import numpy as np
from modis_sinusoidal_tile_converter.convert import array2tiff

data = np.zeros((1200, 1200), dtype=np.uint16)
array2tiff(data, "h26v05.tiff", hv="h26v05", grid="1km")
```

## 📌 投影参数
- **1km 网格**：每个像素 926.625 米。
- **500m 网格**：每个像素 463.312 米。
- **瓦片系统**：由水平（`hXX`）和垂直（`vXX`）瓦片索引定义。

## 📂 资源
生成 **MODIS_Sinusoidal_Tile_Grid_Corner_Coordinates.csv**：
```bash
python scripts/get_corner_coordinates_of_modis_sinusoidal_tile.py **/*.hdf
```

## 🔗 参考链接
- [MODIS 影像网格](https://modis-land.gsfc.nasa.gov/MODLAND_grid.html)
- [MODIS 瓦片计算器](https://landweb.modaps.eosdis.nasa.gov/cgi-bin/developer/tilemap.cgi)
