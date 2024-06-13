import numpy as np

from modis_sinusoidal_tile_converter.convert import array2tiff

arr = np.zeros((1200, 1200), dtype=np.uint16)
hv = "h26v05"
array2tiff(arr, f"{hv}.tiff", hv="h26v06", grid="1km")
