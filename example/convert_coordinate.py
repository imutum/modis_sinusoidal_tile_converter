from modis_sinusoidal_tile_converter import Sinusoidal

if __name__ == "__main__":
    # 获取图块的经纬度范围
    print("============示例: 获取图块的经纬度范围============")
    vertical_tile, horizontal_tile = 4, 24
    print(f"Input---> vertical_tile: {vertical_tile}, horizontal_tile: {horizontal_tile}")
    result = Sinusoidal.tile_GCSBox(vertical_tile, horizontal_tile)
    lat_min, lon_min, lat_max, lon_max = result
    print(f"Output--> lat_min: {lat_min}, lon_min: {lon_min}, lat_max: {lat_max}, lon_max: {lon_max}")

    # 地理坐标系与图块坐标系互转
    print("============示例: 地理坐标系与图块坐标系互转============")
    lat, lon = 50.0, 94.34342961162473
    print(f"Input---> lat: {lat}, lon: {lon}")
    vertical_tile, horizontal_tile, line, sample = Sinusoidal.GCS2ICSTile(lat, lon)
    print(
        f"Output--> vertical_tile: {vertical_tile}, horizontal_tile: {horizontal_tile}, line: {line}, sample: {sample}"
    )
    print(
        f"Input---> vertical_tile: {vertical_tile}, horizontal_tile: {horizontal_tile}, line: {line}, sample: {sample}"
    )
    lat, lon = Sinusoidal.ICSTile2GCS(vertical_tile, horizontal_tile, line, sample)
    print(f"Output--> lat: {lat}, lon: {lon}")

    # 地理坐标系与直角坐标系互转
    print("============示例: 地理坐标系与直角坐标系互转============")
    lat, lon = 50.0, 93.34342961162473
    print(f"Input---> lat: {lat}, lon: {lon}")
    x, y = Sinusoidal.GCS2PCS(lat, lon)
    print(f"Output--> x: {x}, y: {y}")
    print(f"Input---> x: {x}, y: {y}")
    lat, lon = Sinusoidal.PCS2GCS(x, y)
    print(f"Output--> lat: {lat}, lon: {lon}")
