from typing import Tuple, Union

import numpy as np
import rasterio as rio

from modis_sinusoidal_tile_converter import Sinusoidal


def array2tiff(
    arr: np.ndarray,
    tiff_path: str,
    hv: Union[str, Tuple[int, int]],
    grid: str = "1km",
    **kwargs,
):
    # 检查数组维度, 如果是2D数组则增加一个维度
    if len(arr.shape) == 2:
        arr = np.expand_dims(arr, axis=0)
    elif len(arr.shape) != 3:
        raise ValueError("Only support 2D or 3D array")
    # 获取数组的bands, height, width
    bands, height, width = arr.shape
    # 可选的profile信息, 如果没有传入则使用默认值
    profile = kwargs
    profile.update({"compress": kwargs.get("compress", "lzw"), "nodata": kwargs.get("nodata", None)})
    # 必要的profile信息
    if grid == "1km":
        zoom = 1000
    elif grid == "500m":
        zoom = 500
    elif grid == "250m":
        zoom = 250
    else:
        raise ValueError(f"Invalid grid {grid}, should be in range of [1km, 500m, 250m]")
    transform = Sinusoidal.get_tile_transform(hv, zoom=zoom)
    crs = Sinusoidal.get_tile_crs(hv)
    profile.update(
        {
            "dtype": kwargs.get("dtype", arr.dtype),
            "count": bands,
            "width": width,
            "height": height,
            "crs": crs,
            "transform": transform,
        }
    )
    # 写入tiff文件
    with rio.open(tiff_path, "w", **profile) as ds:
        ds.write(arr)
