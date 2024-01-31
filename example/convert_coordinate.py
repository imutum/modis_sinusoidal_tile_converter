from modis_sinusoidal_tile_converter import Sinusoidal


if __name__ == "__main__":
    # ============旧版测试============
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

    # ============新版测试============
    # 获取图块的经纬度范围
    print("============示例: 获取图块的经纬度范围============")
    vertical_tile, horizontal_tile = 4, 24
    print(f"Input---> vertical_tile: {vertical_tile}, horizontal_tile: {horizontal_tile}")
    result = Sinusoidal.get_bounding_coordinates_of_sinusoidal_tiles(vertical_tile, horizontal_tile)
    lat_min, lat_max, lon_min, lon_max = result
    print(f"Output--> lat_min: {lat_min}, lat_max: {lat_max}, lon_min: {lon_min}, lon_max: {lon_max}")

    # 地理坐标系与图块坐标系互转
    print("============示例: 地理坐标系与图块坐标系互转============")
    lat, lon = 50.0, 93.34342961162473
    print(f"Input---> lat: {lat}, lon: {lon}")
    vertical_tile, horizontal_tile, line, sample = Sinusoidal.gc2tcnum(50.0, 93.34342961162473)
    print(
        f"Output--> vertical_tile: {vertical_tile}, horizontal_tile: {horizontal_tile}, line: {line}, sample: {sample}"
    )
    print(
        f"Input---> vertical_tile: {vertical_tile}, horizontal_tile: {horizontal_tile}, line: {line}, sample: {sample}"
    )
    lat, lon = Sinusoidal.tcnum2gc(vertical_tile, horizontal_tile, line, sample)
    print(f"Output--> lat: {lat}, lon: {lon}")

    # 地理坐标系与直角坐标系互转
    print("============示例: 地理坐标系与直角坐标系互转============")
    lat, lon = 50.0, 93.34342961162473
    print(f"Input---> lat: {lat}, lon: {lon}")
    x, y = Sinusoidal.gc2rc(lat, lon)
    print(f"Output--> x: {x}, y: {y}")
    print(f"Input---> x: {x}, y: {y}")
    lat, lon = Sinusoidal.rc2gc(x, y)
    print(f"Output--> lat: {lat}, lon: {lon}")
