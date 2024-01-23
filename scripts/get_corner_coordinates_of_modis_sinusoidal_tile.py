import os
import glob
import re
import argparse

import pandas as pd
from pyhdf.SD import SD, SDC, SDS

parser = argparse.ArgumentParser(description="Get MODIS Sinusoidal Tile Grid Corner Coordinates")
parser.add_argument("path", help="Path of MODIS Sinusoidal Tile Grid Corner Coordinates")


def get_corner_coordinates_from_modis_hdf(path):
    # 使用pyhdf读取hdf文件
    fp = SD(path, mode=SDC.READ)
    # 获取文件中的属性信息
    infos = fp.attributes()["StructMetadata.0"]
    # 从属性信息中提取坐标信息
    coordinates = re.findall("UpperLeftPointMtrs=\((.*?),(.*?)\).*?LowerRightMtrs=\((.*?),(.*?)\)", infos, re.S)[0]
    # 将坐标信息转换为浮点数
    coordinates = [float(i) for i in coordinates]
    return coordinates


def batch_read_hdf_to_generate_hv_csv(paths: list):
    if not isinstance(paths, list):
        raise TypeError("Parameter(paths) must be list")
    hvdict = {}
    paths = sorted(paths)
    for i in paths:
        print(i)
        # 获取文件名称
        filename = os.path.basename(i)
        # 获取文件分幅号, MODIS文件格式中，文件名中间的h09v07就是分幅号, h表示横向，v表示纵向
        # MOD09GA.A2021002.h09v07.061.2021012063102.hdf
        # MCD19A2.A2021365.h32v08.061.2023157173848.hdf
        hv = filename.split(".")[2]  # h09v07
        # 如果分幅号在字典中已经存在，则跳过
        if hv in hvdict:
            continue
        # 获取分幅号对应的坐标信息
        coordinates = get_corner_coordinates_from_modis_hdf(i)
        h = int(hv[1:3])
        v = int(hv[4:6])
        # 将分幅号和坐标信息存入字典
        hvdict[hv] = [h, v] + coordinates
    # 将字典转换为DataFrame
    if len(hvdict) == 0:
        return pd.DataFrame()
    df = pd.DataFrame.from_dict(hvdict, orient="index").reset_index()
    df.columns = ["hv", "h", "v", "ulx", "uly", "lrx", "lry"]
    df.sort_values(["h", "v"], inplace=True)
    df["h"] = df["h"].astype(int)
    df["v"] = df["v"].astype(int)
    return df


if __name__ == "__main__":
    args = parser.parse_args()
    # 获取文件列表
    path_re_str = args.path
    paths = list(glob.glob(path_re_str, recursive=True))
    print(f"文件数量: {len(paths)}")  # 输出文件数量
    # 读取文件，生成MODIS_Sinusoidal_Tile_Grid_Corner_Coordinates.csv文件
    df = batch_read_hdf_to_generate_hv_csv(paths)
    df.to_csv("MODIS_Sinusoidal_Tile_Grid_Corner_Coordinates.csv", index=False)
