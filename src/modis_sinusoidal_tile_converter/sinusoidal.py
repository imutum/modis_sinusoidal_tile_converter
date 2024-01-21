import math
from pyproj import Proj, CRS

__all__ = ["Sinusoidal"]


class Sinusoidal:
    """
    正弦投影
    对于Modis传感器, 部分数据使用该种投影方式
    参考网站: https://modis-land.gsfc.nasa.gov/MODLAND_grid.html
    参考网站: https://landweb.modaps.eosdis.nasa.gov/cgi-bin/developer/tilemap.cgi

    常规参数:
    gc: geographic coordinates, 地理坐标系, 以经纬度表示地面点位置的球面坐标, (lat, lon), 先南北方向后东西方向
    rc: rectangular coordinates, 直角坐标系, 以米为单位表示地面点位置的坐标, (x, y), 先东西方向后南北方向

    MODIS传感器特殊参数:
    tcnum: tile/image coordinates in number, 用图块编号表示的平铺/影像坐标系, 以图块编号表示:
            垂直图块号(vertical_tile), 数值范围为0~17;
            水平图块号(horizontal_tile), 数值范围为0~35;
            垂直行号(line), 数值范围为-0.5~1199.5;
            水平列号(sample), 数值范围为-0.5~1199.5;

    tcdeg: tile/image coordinates in degree, 用经纬度表示的平铺/影像坐标系, 由于
            影像坐标系以平整的方形网格划分影像图块, 划分间隔为10°, 故图像范围与地理
            坐标系为(-90~90, -180~180)

    注意: 此处图块左上角的像素中心坐标为 (0.0, 0.0), 图块左上角的像素左上角坐标为 (-0.5, -0.5)
    """

    wkt = 'PROJCS["MODIS_Sinusoidal",GEOGCS["GCS_Sphere",DATUM["D_Sphere",SPHEROID["Sphere",6371007.181,0]],PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433]],PROJECTION["Sinusoidal"],PARAMETER["longitude_of_center",0],PARAMETER["false_easting",0],PARAMETER["false_northing",0],UNIT["metre",1,AUTHORITY["EPSG","9001"]]]'

    crs = CRS.from_wkt(wkt)

    # 检查图块编号是否合法
    @staticmethod
    def check_tile_number(vertical_tile: int, horizontal_tile: int):
        """检查图块编号是否合法

        Parameters
        ----------
        vertical_tile : int
            垂直图块号
        horizontal_tile : int
            水平图块号
        """
        if vertical_tile < 0 or vertical_tile > 17:
            raise ValueError("vertical_tile should be in range of [0, 17]")
        if horizontal_tile < 0 or horizontal_tile > 35:
            raise ValueError("horizontal_tile should be in range of [0, 35]")

    @staticmethod
    def tcnum2tcdeg(vertical_tile, horizontal_tile, line, sample):
        Sinusoidal.check_tile_number(vertical_tile, horizontal_tile)
        lat_tile = 90 - vertical_tile * 10 - (line + 0.5) / 120
        lon_tile = -180 + horizontal_tile * 10 + (sample + 0.5) / 120
        return lat_tile, lon_tile

    @staticmethod
    def tcdeg2tcnum(lat_tile, lon_tile):
        vertical_tile = int((90 - lat_tile) / 10)
        horizontal_tile = int((lon_tile + 180) / 10)
        line = -(lat_tile - 90 + vertical_tile * 10) * 120 - 0.5
        sample = (180 - horizontal_tile * 10 + lon_tile) * 120 - 0.5
        return vertical_tile, horizontal_tile, round(line, 8), round(sample, 8)  # 保留8位小数

    @staticmethod
    def tcdeg2gc(lat_tile, lon_tile):
        lat_geographic = lat_tile
        lon_geographic = lon_tile / math.cos(lat_geographic / 180 * math.pi)
        return lat_geographic, lon_geographic

    @staticmethod
    def gc2tcdeg(lat_geographic, lon_geographic):
        lat_tile = lat_geographic
        lon_tile = lon_geographic * math.cos(lat_geographic / 180 * math.pi)
        math.cos(lat_geographic / 2 * math.pi)
        return lat_tile, lon_tile

    @staticmethod
    def coordinates_tile2mapindex(lat_tile, lon_tile, vertical, horizental):
        vertical_pos = int(vertical * (-lat_tile + 90) / 180)
        horizental_pos = int(horizental * (lon_tile + 180) / 360)
        if vertical_pos == vertical:
            vertical_pos -= 1
        if horizental_pos == horizental:
            horizental_pos -= 1
        return vertical_pos, horizental_pos

    @staticmethod
    def tcnum2gc(vertical_tile, horizontal_tile, line, sample):
        """转换图块坐标系到地理坐标系
        :param vertical_tile: 垂直图块号
        :param horizontal_tile: 水平图块号
        :param line: 垂直行号
        :param sample: 水平列号
        :return: (lat_geographic, lon_geographic), 纬度为南北方向, 经度为东西方向"""
        lat_tile, lon_tile = Sinusoidal.tcnum2tcdeg(vertical_tile, horizontal_tile, line, sample)
        return Sinusoidal.tcdeg2gc(lat_tile, lon_tile)

    @staticmethod
    def gc2tcnum(lat_geographic, lon_geographic):
        """转换地理坐标系到图块坐标系
        :param lat_geographic: 纬度
        :param lon_geographic: 经度
        :return: (vertical_tile, horizontal_tile, line, sample)"""
        lat_tile, lon_tile = Sinusoidal.gc2tcdeg(lat_geographic, lon_geographic)
        return Sinusoidal.tcdeg2tcnum(lat_tile, lon_tile)

    @staticmethod
    def gc2rc(lat_geographic, lon_geographic):
        """
        地理坐标系转大地坐标系
        :param lat_geographic: 纬度
        :param lon_geographic: 经度
        :return: (x, y), x 为东西方向, y 为南北方向
        """
        x, y = Proj(Sinusoidal.crs)(lon_geographic, lat_geographic)
        return x, y

    @staticmethod
    def rc2gc(x, y):
        """
        大地坐标系转地理坐标系
        :param x: x, 东西方向
        :param y: y, 南北方向
        :return: (lat_geographic, lon_geographic), 纬度为南北方向, 经度为东西方向
        """
        lon_geographic, lat_geographic = Proj(Sinusoidal.crs)(x, y, inverse=True)
        return lat_geographic, lon_geographic

    @staticmethod
    def get_bounding_coordinates_of_sinusoidal_tiles(vertical_tile, horizontal_tile):
        """
        获取指定图块的经纬度坐标矩形范围
        :param vertical_tile: 垂直图块号
        :param horizontal_tile: 水平图块号
        :return: (lat_min, lat_max, lon_min, lon_max)
        """
        # 分别计算四个角点的经纬度, 由于是正弦投影, 所以四个角点都要计算经纬度
        lat_ul, lon_ul = Sinusoidal.tcnum2gc(vertical_tile, horizontal_tile, -0.5, -0.5)  # 左上角
        lat_ur, lon_ur = Sinusoidal.tcnum2gc(vertical_tile, horizontal_tile, -0.5, 1199.5)  # 右上角
        lat_lr, lon_lr = Sinusoidal.tcnum2gc(vertical_tile, horizontal_tile, 1199.5, 1199.5)  # 右下角
        lat_ll, lon_ll = Sinusoidal.tcnum2gc(vertical_tile, horizontal_tile, 1199.5, -0.5)  # 左下角
        lat_min = min(lat_ul, lat_lr, lat_ur, lat_ll)
        lat_max = max(lat_ul, lat_lr, lat_ur, lat_ll)
        lon_min = min(lon_ul, lon_lr, lon_ur, lon_ll)
        lon_max = max(lon_ul, lon_lr, lon_ur, lon_ll)
        return lat_min, lat_max, lon_min, lon_max
