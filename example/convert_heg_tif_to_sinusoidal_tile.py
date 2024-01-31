import os

import numpy as np
import pandas as pd
import rasterio as rio
from rasterio import Affine
from rasterio.warp import calculate_default_transform, reproject, Resampling
from mtmtool.time import auto_parse_time_with_datefmt

from modis_sinusoidal_tile_converter import Sinusoidal

# 获取MODIS Sinusoidal Tile Grid Corner Coordinates
#    hv,h,v,ulx,uly,lrx,lry
#    h00v08,0,8,-20015109.354,1111950.519667,-18903158.834333,0.0
#    ......
df_grids = pd.read_csv("MODIS_Sinusoidal_Tile_Grid_Corner_Coordinates.csv")


def convert_heg_tif_to_sinusoidal_tile(filepath):
    # 从文件名中解析出产品名称和时间
    filename = os.path.basename(filepath)
    product_name = filename.split(".")[0]
    timestr = auto_parse_time_with_datefmt(filename, "A%Y%j.%H%M.", "UTC")[0].strftime("%Y%j%H%M%S")

    # 读取MODIS经过HEG处理后的TIFF文件
    with rio.open(filepath) as src:
        band = src.read(1)
        profile = src.profile
        src_crs = src.crs
        src_transform, width, height = calculate_default_transform(
            src.crs, Sinusoidal.crs, src.width, src.height, *src.bounds, resolution=926.625433055
        )

    # 获取MODIS Sinusoidal Tile Grid Corner Coordinates
    ulx, uly = src_transform * (0, 0)
    lrx, lry = src_transform * (height, width)
    df_cover = df_grids[
        ~((ulx >= df_grids["lrx"]) | (lrx <= df_grids["ulx"]) | (uly <= df_grids["lry"]) | (lry >= df_grids["uly"]))
    ]

    # 循环写入每个Tile
    for _, row in df_cover.iterrows():
        # 生成输出文件名
        filename_out = f"{product_name}.1000.{timestr}.H{int(row['h']):02d}V{int(row['v']):02d}.tiff"
        # 生成投影变换参数
        para = list(src_transform.to_gdal())
        para[0] = row["ulx"]
        para[3] = row["uly"]
        _transform = Affine.from_gdal(*para)
        # 投影转换
        data, _ = reproject(
            source=band,
            destination=np.zeros((1200, 1200), dtype=band.dtype),
            src_transform=src_transform,
            src_crs=src_crs,
            dst_nodata=-9999,
            dst_transform=_transform,
            dst_crs=Sinusoidal.crs,
            resampling=Resampling.nearest,
        )
        # 写入文件
        _profile = profile.copy()
        _profile.update(
            {
                "crs": Sinusoidal.crs,
                "transform": _transform,
                "width": int(1200),
                "height": int(1200),
                "nodata": -9999,
            }
        )
        with rio.open(filename_out, "w", **_profile) as dst:
            dst.write(data, 1)
