import math
import numpy as np
from pyproj import CRS, Proj
from typing import Tuple
from rasterio import Affine

__all__ = ["WebMercator"]


class WebMercator:
    """
    WebMercator投影
    参考网站: https://en.wikipedia.org/wiki/Web_Mercator_projection
    """
    crs = CRS.from_epsg(3857)
    tile_meters_ulx = -20037508.3427892
    tile_meters_uly = 20037508.3427892
    tile_meters_brx = 20037508.3427892
    tile_meters_bry = -20037508.3427892
    pixels_per_tile = 256

    @staticmethod
    def _check_tile_xyz_valid(x:int, y:int, z:int):
        """检查瓦片编号是否合法"""
        # 检查x, y, z的取值范围，z为层级，x, y为瓦片编号，瓦片编号为0-2^z-1
        if x < 0 or x >= 2**z:
            raise ValueError(f"x({x}) should be in range of [0, {2**z})")
        if y < 0 or y >= 2**z:
            raise ValueError(f"y({y}) should be in range of [0, {2**z})")
        if z < 0 or z >= 21:
            raise ValueError(f"z({z}) should be in range of [0, 21)")

    @staticmethod
    def PCS2ICSTile(x:float | np.ndarray, y:float | np.ndarray, z:int)->Tuple[int | np.ndarray, int | np.ndarray]:
        """将投影坐标系转换为目标缩放级别(z)下的图块瓦片号(x, y)"""
        # 计算图块瓦片号
        tile_count = 2**z # 瓦片总数
        tile_meters_total_x = WebMercator.tile_meters_brx - WebMercator.tile_meters_ulx # 水平方向投影坐标系米数
        tile_meters_total_y = WebMercator.tile_meters_uly - WebMercator.tile_meters_bry # 垂直方向投影坐标系米数
        tile_x = np.floor((x - WebMercator.tile_meters_ulx) / tile_meters_total_x * tile_count).astype(int) # 水平方向瓦片号
        tile_y = np.floor((y - WebMercator.tile_meters_bry) / tile_meters_total_y * tile_count).astype(int) # 垂直方向瓦片号
        return tile_x, tile_y

    @staticmethod
    def get_tile_crs()->CRS:
        """获取瓦片坐标系"""
        return WebMercator.crs

    @staticmethod
    def get_tile_bounds(x:int, y:int, z:int)->Tuple[float, float, float, float]:
        """获取瓦片边界坐标"""
        earth_circumference = WebMercator.tile_meters_brx - WebMercator.tile_meters_ulx
        tile_size_meters = earth_circumference / (2 ** z) # 每个瓦片的大小
        
        tile_ulx = WebMercator.tile_meters_ulx + x * tile_size_meters # 瓦片左上角x坐标
        tile_uly = WebMercator.tile_meters_uly - y * tile_size_meters # 瓦片左上角y坐标
        tile_brx = WebMercator.tile_meters_ulx + (x+1) * tile_size_meters # 瓦片右下角x坐标
        tile_bry = WebMercator.tile_meters_uly - (y+1) * tile_size_meters # 瓦片右下角y坐标
        return round(tile_ulx, 6), round(tile_uly, 6), round(tile_brx, 6), round(tile_bry, 6)

    @staticmethod
    def get_tile_transform(x:int, y:int, z:int)->Affine:
        """获取瓦片六参数投影变换矩阵, 用于将瓦片坐标系转换为地理坐标系"""
        # 检查瓦片编号是否合法
        WebMercator._check_tile_xyz_valid(x, y, z)
        # 计算瓦片变换矩阵
        ulx, uly, brx, bry = WebMercator.get_tile_bounds(x, y, z)   
        pixel_size = (brx - ulx) / WebMercator.pixels_per_tile # 每个像素的大小
        return Affine.from_gdal(ulx, pixel_size, 0, uly, 0, -pixel_size)