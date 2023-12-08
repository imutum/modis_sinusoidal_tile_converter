import math

__all__ = ['Sinusoidal']


class Sinusoidal:
    """
    正弦投影
    对于Modis传感器，部分数据使用该种投影方式
    参考网站：https://modis-land.gsfc.nasa.gov/MODLAND_grid.html
    参考网站：https://landweb.modaps.eosdis.nasa.gov/cgi-bin/developer/tilemap.cgi

    常规参数：
    gc: geographic coordinates，地理坐标系，以经纬度表示地面点位置的球面坐标
    rc: rectangular coordinates/geodetic coordinate, 直角坐标系/大地坐标系，以米为单位表示地面点位置的球面坐标

    MODIS传感器特殊参数：
    tcnum: tile/image coordinates in number, 用图块编号表示的平铺/影像坐标系，以图块编号表示:
            垂直图块号(vertical_tile), 数值范围为0~17;
            水平图块号(horizontal_tile), 数值范围为0~35;
            垂直行号(line), 数值范围为-0.5~1199.5;
            水平列号(sample), 数值范围为-0.5~1199.5;

    tcdeg: tile/image coordinates in degree, 用经纬度表示的平铺/影像坐标系，由于
            影像坐标系以平整的方形网格划分影像图块，划分间隔为10°，故图像范围与地理
            坐标系为(-90~90, -180~180)
    """

    @staticmethod
    def tcnum2tcdeg(vertical_tile, horizontal_tile, line, sample):
        lat_tile = 90 - vertical_tile * 10 - (line + 0.5) / 120
        lon_tile = -180 + horizontal_tile * 10 + (sample + 0.5) / 120
        return lat_tile, lon_tile

    @staticmethod
    def tcdeg2tcnum(lat_tile, lon_tile):
        vertical_tile = int((90 - lat_tile) / 10)
        horizontal_tile = int((lon_tile + 180) / 10)
        line = -(lat_tile - 90 + vertical_tile * 10) * 120 - 0.5
        sample = (180 - horizontal_tile * 10 + lon_tile) * 120 - 0.5
        return vertical_tile, horizontal_tile, line, sample

    @staticmethod
    def tcdeg2gc(lat_tile, lon_tile):
        lat_geographic = lat_tile
        lon_geographic = lon_tile / math.cos(lat_geographic / 180 * math.pi)
        math.cos(lat_geographic / 2 * math.pi)
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
        lat_tile, lon_tile = Sinusoidal.tcnum2tcdeg(vertical_tile, horizontal_tile, line, sample)
        return Sinusoidal.tcdeg2gc(lat_tile, lon_tile)

    @staticmethod
    def gc2tcnum(lat_geographic, lon_geographic):
        lat_tile, lon_tile = Sinusoidal.gc2tcdeg(lat_geographic, lon_geographic)
        return Sinusoidal.tcdeg2tcnum(lat_tile, lon_tile)


if __name__ == '__main__':
    print(Sinusoidal.coordinates_tile2mapindex(90.0, 180.0, 2631, 7687))

    res1 = Sinusoidal.gc2tcdeg(
        -50.0,
        15.557238268604122,
    )
    res2 = Sinusoidal.tcnum2tcdeg(14, 19, -0.5, -0.5)
    res3 = Sinusoidal.tcdeg2gc(-50, 10)
    res4 = Sinusoidal.tcnum2gc(14, 19, -0.5, -0.5)
    res5 = Sinusoidal.tcdeg2tcnum(-50, 10)
    geodeg = (1111950.52, -5559752.60)
    print(res1, res2, res3, res4, res5)
    print(Sinusoidal.tcnum2gc(3, 18, 1199.50, 1002.25))
    # 2
    res2 = Sinusoidal.tcnum2tcdeg(14, 19, 300.5, 500.5)
    res5 = Sinusoidal.tcdeg2tcnum(-52.50833333333333, 14.175)
    print(res2, res5)
