import math

from pyproj import CRS, Proj
from typing import Tuple
from rasterio import Affine

__all__ = ["Sinusoidal"]


class Sinusoidal:
    """
    Sinusoidal正弦投影
    对于MODIS传感器, 部分数据使用该种投影方式
    参考网站: https://modis-land.gsfc.nasa.gov/MODLAND_grid.html
    参考网站: https://landweb.modaps.eosdis.nasa.gov/cgi-bin/developer/tilemap.cgi

    常规坐标系参数说明:
    GCS: Geographic Coordinate System, 地理坐标系, 以经纬度表示地面点位置的球面坐标, (lat, lon), lat南北方向, lon东西方向
    PCS: Projected Coordinate System, 投影坐标系, 一般以米为单位表示地面点位置的坐标, (x, y), x东西方向, y南北方向

    MODIS正弦投影的参数说明:
    ICSTile: Tile/Image Coordinates System, 用图块编号表示的平铺/影像坐标系:
            垂直图块号(vertical_tile), 数值范围为0~17;
            水平图块号(horizontal_tile), 数值范围为0~35;
            垂直行号(line), 数值范围为-0.5~1199.5(1km)2399.5(500m);
            水平列号(sample), 数值范围为-0.5~1199.5(1km)2399.5(500m);

    ICSGeo: Geographic Tile/Image Coordinate System, 用经纬度表示的平铺/影像坐标系:
            纬度(lat_tile), 数值范围为-90~90;
            经度(lon_tile), 数值范围为-180~180;

    注意: 此处图块左上角的像素中心坐标为 (0.0, 0.0), 图块左上角的像素左上角坐标为 (-0.5, -0.5)
    """

    wkt = 'PROJCS["MODIS_Sinusoidal",GEOGCS["GCS_Sphere",DATUM["D_Sphere",SPHEROID["Sphere",6371007.181,0]],PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433]],PROJECTION["Sinusoidal"],PARAMETER["longitude_of_center",0],PARAMETER["false_easting",0],PARAMETER["false_northing",0],UNIT["metre",1,AUTHORITY["EPSG","9001"]]]'

    tile_size_meters_1km = 926.625433055833
    tile_size_meters_500m = 463.312716527917
    tile_size_meters_250m = 231.656358263958
    tile_meters_ulx = -20015109.354
    tile_meters_uly = 10007554.677
    

    crs = CRS.from_wkt(wkt)

    default_precision = 8

    @staticmethod
    def _check_tile(vertical_tile: int, horizontal_tile: int):
        """检查图块编号是否合法"""
        if vertical_tile < 0 or vertical_tile > 17:
            raise ValueError(f"vertical_tile({vertical_tile}) should be in range of [0, 17]")
        if horizontal_tile < 0 or horizontal_tile > 35:
            raise ValueError(f"horizontal_tile({horizontal_tile}) should be in range of [0, 35]")

    @staticmethod
    def _check_geo(lat: float, lon: float):
        """检查经纬度是否合法"""
        if lat < -90 or lat > 90:
            raise ValueError(f"lat({lat}) should be in range of [-90, 90]")
        if lon < -180 or lon > 180:
            raise ValueError(f"lon({lat}) should be in range of [-180, 180]")

    @staticmethod
    def ICSTile2ICSGeo(vertical_tile, horizontal_tile, line, sample, grid="1km"):
        """转换平铺坐标系到地理影像坐标系
        :param vertical_tile: 垂直图块号
        :param horizontal_tile: 水平图块号
        :param line: 垂直行号
        :param sample: 水平列号
        :return: (lat_tile, lon_tile), 纬度为南北方向, 经度为东西方向"""
        Sinusoidal._check_tile(vertical_tile, horizontal_tile)
        if grid == "1km":
            lat_tile = 90 - vertical_tile * 10 - (line + 0.5) / 120
            lon_tile = -180 + horizontal_tile * 10 + (sample + 0.5) / 120
        elif grid == "500m":
            lat_tile = 90 - vertical_tile * 10 - (line + 0.5) / 240
            lon_tile = -180 + horizontal_tile * 10 + (sample + 0.5) / 240
        else:
            raise ValueError(f"grid({grid}) should be in ['1km', '500m']")
        return lat_tile, lon_tile

    @staticmethod
    def ICSGeo2ICSTile(lat_tile, lon_tile, grid="1km"):
        """转换地理影像坐标系到平铺坐标系
        :param lat_tile: 纬度
        :param lon_tile: 经度
        :return: (vertical_tile, horizontal_tile, line, sample)"""
        Sinusoidal._check_geo(lat_tile, lon_tile)
        vertical_tile = int((90 - lat_tile) / 10)
        horizontal_tile = int((lon_tile + 180) / 10)
        if grid == "1km":
            line = round(-(lat_tile - 90 + vertical_tile * 10) * 120 - 0.5, Sinusoidal.default_precision)
            sample = round((180 - horizontal_tile * 10 + lon_tile) * 120 - 0.5, Sinusoidal.default_precision)
        elif grid == "500m":
            line = round(-(lat_tile - 90 + vertical_tile * 10) * 240 - 0.5, Sinusoidal.default_precision)
            sample = round((180 - horizontal_tile * 10 + lon_tile) * 240 - 0.5, Sinusoidal.default_precision)
        else:
            raise ValueError(f"grid({grid}) should be in ['1km', '500m']")
        return vertical_tile, horizontal_tile, line, sample

    @staticmethod
    def ICSGeo2GCS(lat_tile, lon_tile):
        """转换地理影像坐标系到地理坐标系
        :param lat_tile: 纬度
        :param lon_tile: 经度
        :return: (lat_gcs, lon_gcs), 纬度为南北方向, 经度为东西方向"""
        Sinusoidal._check_geo(lat_tile, lon_tile)
        lat_gcs = lat_tile
        lon_gcs = lon_tile / math.cos(math.radians(lat_gcs))
        return lat_gcs, lon_gcs

    @staticmethod
    def GCS2ICSGeo(lat_gcs, lon_gcs):
        """转换地理坐标系到地理影像坐标系
        :param lat_gcs: 纬度
        :param lon_gcs: 经度
        :return: (lat_tile, lon_tile), 纬度为南北方向, 经度为东西方向"""
        Sinusoidal._check_geo(lat_gcs, lon_gcs)
        lat_tile = lat_gcs
        lon_tile = lon_gcs * math.cos(math.radians(lat_gcs))
        return lat_tile, lon_tile

    @staticmethod
    def ICSTile2GCS(vertical_tile, horizontal_tile, line, sample, grid="1km"):
        """转换平铺坐标系到地理坐标系
        :param vertical_tile: 垂直图块号
        :param horizontal_tile: 水平图块号
        :param line: 垂直行号
        :param sample: 水平列号
        :return: (lat_gcs, lon_gcs), 纬度为南北方向, 经度为东西方向"""
        lat_tile, lon_tile = Sinusoidal.ICSTile2ICSGeo(vertical_tile, horizontal_tile, line, sample, grid)
        lat_gcs, lon_gcs = Sinusoidal.ICSGeo2GCS(lat_tile, lon_tile)
        return lat_gcs, lon_gcs

    @staticmethod
    def GCS2ICSTile(lat_gcs, lon_gcs, grid="1km"):
        """转换地理坐标系到平铺坐标系
        :param lat_gcs: 纬度
        :param lon_gcs: 经度
        :return: (vertical_tile, horizontal_tile, line, sample)"""
        lat_tile, lon_tile = Sinusoidal.GCS2ICSGeo(lat_gcs, lon_gcs)
        vertical_tile, horizontal_tile, line, sample = Sinusoidal.ICSGeo2ICSTile(lat_tile, lon_tile, grid)
        return vertical_tile, horizontal_tile, line, sample

    @staticmethod
    def GCS2PCS(lat_gcs, lon_gcs):
        """
        地理坐标系转投影坐标系
        :param lat_gcs: 纬度
        :param lon_gcs: 经度
        :return: (x, y), x 为东西方向, y 为南北方向
        """
        x, y = Proj(Sinusoidal.crs)(lon_gcs, lat_gcs)
        return x, y

    @staticmethod
    def PCS2GCS(x, y):
        """
        投影坐标系转地理坐标系
        :param x: x, 东西方向
        :param y: y, 南北方向
        :return: (lat_gcs, lon_gcs), 纬度为南北方向, 经度为东西方向
        """
        lon_gcs, lat_gcs = Proj(Sinusoidal.crs)(x, y, inverse=True)
        return lat_gcs, lon_gcs

    @staticmethod
    def tile_GCSBox(vertical_tile, horizontal_tile, grid="1km"):
        """
        获取指定图块的地理坐标系矩形范围
        :param vertical_tile: 垂直图块号
        :param horizontal_tile: 水平图块号
        :return: (lat_min, lon_min, lat_max, lon_max)
        """
        # 分别计算四个角点的经纬度, 由于是正弦投影, 所以四个角点都要计算经纬度
        if grid == "1km":
            lat_ul, lon_ul = Sinusoidal.ICSTile2GCS(vertical_tile, horizontal_tile, -0.5, -0.5)  # 左上角
            lat_ur, lon_ur = Sinusoidal.ICSTile2GCS(vertical_tile, horizontal_tile, -0.5, 1199.5)  # 右上角
            lat_lr, lon_lr = Sinusoidal.ICSTile2GCS(vertical_tile, horizontal_tile, 1199.5, 1199.5)  # 右下角
            lat_ll, lon_ll = Sinusoidal.ICSTile2GCS(vertical_tile, horizontal_tile, 1199.5, -0.5)  # 左下角
        elif grid == "500m":
            lat_ul, lon_ul = Sinusoidal.ICSTile2GCS(vertical_tile, horizontal_tile, -0.5, -0.5)
            lat_ur, lon_ur = Sinusoidal.ICSTile2GCS(vertical_tile, horizontal_tile, -0.5, 2399.5)
            lat_lr, lon_lr = Sinusoidal.ICSTile2GCS(vertical_tile, horizontal_tile, 2399.5, 2399.5)
            lat_ll, lon_ll = Sinusoidal.ICSTile2GCS(vertical_tile, horizontal_tile, 2399.5, -0.5)
        lat_min = min(lat_ul, lat_lr, lat_ur, lat_ll)
        lat_max = max(lat_ul, lat_lr, lat_ur, lat_ll)
        lon_min = min(lon_ul, lon_lr, lon_ur, lon_ll)
        lon_max = max(lon_ul, lon_lr, lon_ur, lon_ll)
        return lat_min, lon_min, lat_max, lon_max

    @staticmethod
    def tile_PCSGRing(vertical_tile, horizontal_tile, grid="1km"):
        """
        获取指定图块的环直角坐标(GRing, 四个角点的坐标), 高纬度地区失效
        :param vertical_tile: 垂直图块号
        :param horizontal_tile: 水平图块号
        :return: (x_ul, y_ul, x_ur, y_ur, x_lr, y_lr, x_ll, y_ll), x 为东西方向, y 为南北方向
        """
        if grid == "1km":
            lat_ul, lon_ul = Sinusoidal.ICSTile2GCS(vertical_tile, horizontal_tile, -0.5, -0.5)
            x_ul, y_ul = Sinusoidal.GCS2PCS(lat_ul, lon_ul)
            lat_ur, lon_ur = Sinusoidal.ICSTile2GCS(vertical_tile, horizontal_tile, -0.5, 1199.5)
            x_ur, y_ur = Sinusoidal.GCS2PCS(lat_ur, lon_ur)
            lat_lr, lon_lr = Sinusoidal.ICSTile2GCS(vertical_tile, horizontal_tile, 1199.5, 1199.5)
            x_lr, y_lr = Sinusoidal.GCS2PCS(lat_lr, lon_lr)
            lat_ll, lon_ll = Sinusoidal.ICSTile2GCS(vertical_tile, horizontal_tile, 1199.5, -0.5)
            x_ll, y_ll = Sinusoidal.GCS2PCS(lat_ll, lon_ll)
        elif grid == "500m":
            lat_ul, lon_ul = Sinusoidal.ICSTile2GCS(vertical_tile, horizontal_tile, -0.5, -0.5)
            x_ul, y_ul = Sinusoidal.GCS2PCS(lat_ul, lon_ul)
            lat_ur, lon_ur = Sinusoidal.ICSTile2GCS(vertical_tile, horizontal_tile, -0.5, 2399.5)
            x_ur, y_ur = Sinusoidal.GCS2PCS(lat_ur, lon_ur)
            lat_lr, lon_lr = Sinusoidal.ICSTile2GCS(vertical_tile, horizontal_tile, 2399.5, 2399.5)
            x_lr, y_lr = Sinusoidal.GCS2PCS(lat_lr, lon_lr)
            lat_ll, lon_ll = Sinusoidal.ICSTile2GCS(vertical_tile, horizontal_tile, 2399.5, -0.5)
            x_ll, y_ll = Sinusoidal.GCS2PCS(lat_ll, lon_ll)
        return x_ul, y_ul, x_ur, y_ur, x_lr, y_lr, x_ll, y_ll

    @staticmethod
    def get_tile_bounds(hv: str) -> Tuple[float, float]:
        h = int(hv[1:3])
        v = int(hv[4:6])
        dh = Sinusoidal.tile_meters_ulx / 18 
        dv = Sinusoidal.tile_meters_uly / 9
        h_ulx = Sinusoidal.tile_meters_ulx - h * dh
        v_uly = Sinusoidal.tile_meters_uly - v * dv
        h_brx = Sinusoidal.tile_meters_ulx - (h+1) * dh
        v_bry = Sinusoidal.tile_meters_uly - (v+1) * dv
        return round(h_ulx, 6), round(v_uly, 6), round(h_brx, 6), round(v_bry, 6)

    @staticmethod
    def get_tile_crs(hv: str=None) -> CRS:
        return Sinusoidal.crs

    @staticmethod
    def get_tile_transform(hv: str, zoom: int = 1000) -> Affine:
        tile_map_dict = {
            1000: Sinusoidal.tile_size_meters_1km,
            500: Sinusoidal.tile_size_meters_500m,
            250: Sinusoidal.tile_size_meters_250m,
        }
        ulx, uly, _, _ = Sinusoidal.get_tile_bounds(hv)
        return Affine.from_gdal(ulx, tile_map_dict[zoom], 0, uly, 0, -tile_map_dict[zoom])
