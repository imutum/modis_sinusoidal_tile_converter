from typing import Tuple, Union

import numpy as np
import rasterio as rio

from modis_sinusoidal_tile_converter import Sinusoidal

GRIDDX_1KM = 926.625433055833
GRIDDY_1KM = -926.625433055833
GRIDDX_500M = 463.312716527917
GRIDDY_500M = -463.312716527917

PROJECTIONPARASDICT = {
    "h00v08": {"ulx": -20015109.354, "uly": 1111950.519667},
    "h00v09": {"ulx": -20015109.354, "uly": 0.0},
    "h00v10": {"ulx": -20015109.354, "uly": -1111950.519667},
    "h01v07": {"ulx": -18903158.834333, "uly": 2223901.039333},
    "h01v08": {"ulx": -18903158.834333, "uly": 1111950.519667},
    "h01v09": {"ulx": -18903158.834333, "uly": 0.0},
    "h01v10": {"ulx": -18903158.834333, "uly": -1111950.519667},
    "h01v11": {"ulx": -18903158.834333, "uly": -2223901.039333},
    "h02v06": {"ulx": -17791208.314667, "uly": 3335851.559},
    "h02v08": {"ulx": -17791208.314667, "uly": 1111950.519667},
    "h02v09": {"ulx": -17791208.314667, "uly": 0.0},
    "h02v10": {"ulx": -17791208.314667, "uly": -1111950.519667},
    "h02v11": {"ulx": -17791208.314667, "uly": -2223901.039333},
    "h03v05": {"ulx": -16679257.795, "uly": 4447802.078667},
    "h03v06": {"ulx": -16679257.795, "uly": 3335851.559},
    "h03v07": {"ulx": -16679257.795, "uly": 2223901.039333},
    "h03v08": {"ulx": -16679257.795, "uly": 1111950.519667},
    "h03v09": {"ulx": -16679257.795, "uly": 0.0},
    "h03v10": {"ulx": -16679257.795, "uly": -1111950.519667},
    "h03v11": {"ulx": -16679257.795, "uly": -2223901.039333},
    "h04v05": {"ulx": -15567307.275333, "uly": 4447802.078667},
    "h04v09": {"ulx": -15567307.275333, "uly": 0.0},
    "h04v10": {"ulx": -15567307.275333, "uly": -1111950.519667},
    "h04v11": {"ulx": -15567307.275333, "uly": -2223901.039333},
    "h05v10": {"ulx": -14455356.755667, "uly": -1111950.519667},
    "h05v11": {"ulx": -14455356.755667, "uly": -2223901.039333},
    "h05v13": {"ulx": -14455356.755667, "uly": -4447802.078667},
    "h06v03": {"ulx": -13343406.236, "uly": 6671703.118},
    "h06v11": {"ulx": -13343406.236, "uly": -2223901.039333},
    "h07v03": {"ulx": -12231455.716333, "uly": 6671703.118},
    "h07v05": {"ulx": -12231455.716333, "uly": 4447802.078667},
    "h07v06": {"ulx": -12231455.716333, "uly": 3335851.559},
    "h07v07": {"ulx": -12231455.716333, "uly": 2223901.039333},
    "h08v03": {"ulx": -11119505.196667, "uly": 6671703.118},
    "h08v04": {"ulx": -11119505.196667, "uly": 5559752.598333},
    "h08v05": {"ulx": -11119505.196667, "uly": 4447802.078667},
    "h08v06": {"ulx": -11119505.196667, "uly": 3335851.559},
    "h08v07": {"ulx": -11119505.196667, "uly": 2223901.039333},
    "h08v08": {"ulx": -11119505.196667, "uly": 1111950.519667},
    "h08v09": {"ulx": -11119505.196667, "uly": 0.0},
    "h08v11": {"ulx": -11119505.196667, "uly": -2223901.039333},
    "h09v02": {"ulx": -10007554.677, "uly": 7783653.637667},
    "h09v03": {"ulx": -10007554.677, "uly": 6671703.118},
    "h09v04": {"ulx": -10007554.677, "uly": 5559752.598333},
    "h09v05": {"ulx": -10007554.677, "uly": 4447802.078667},
    "h09v06": {"ulx": -10007554.677, "uly": 3335851.559},
    "h09v07": {"ulx": -10007554.677, "uly": 2223901.039333},
    "h09v08": {"ulx": -10007554.677, "uly": 1111950.519667},
    "h09v09": {"ulx": -10007554.677, "uly": 0.0},
    "h10v02": {"ulx": -8895604.157333, "uly": 7783653.637667},
    "h10v03": {"ulx": -8895604.157333, "uly": 6671703.118},
    "h10v04": {"ulx": -8895604.157333, "uly": 5559752.598333},
    "h10v05": {"ulx": -8895604.157333, "uly": 4447802.078667},
    "h10v06": {"ulx": -8895604.157333, "uly": 3335851.559},
    "h10v07": {"ulx": -8895604.157333, "uly": 2223901.039333},
    "h10v08": {"ulx": -8895604.157333, "uly": 1111950.519667},
    "h10v09": {"ulx": -8895604.157333, "uly": 0.0},
    "h10v10": {"ulx": -8895604.157333, "uly": -1111950.519667},
    "h10v11": {"ulx": -8895604.157333, "uly": -2223901.039333},
    "h11v01": {"ulx": -7783653.637667, "uly": 8895604.157333},
    "h11v02": {"ulx": -7783653.637667, "uly": 7783653.637667},
    "h11v03": {"ulx": -7783653.637667, "uly": 6671703.118},
    "h11v04": {"ulx": -7783653.637667, "uly": 5559752.598333},
    "h11v05": {"ulx": -7783653.637667, "uly": 4447802.078667},
    "h11v06": {"ulx": -7783653.637667, "uly": 3335851.559},
    "h11v07": {"ulx": -7783653.637667, "uly": 2223901.039333},
    "h11v08": {"ulx": -7783653.637667, "uly": 1111950.519667},
    "h11v09": {"ulx": -7783653.637667, "uly": 0.0},
    "h11v10": {"ulx": -7783653.637667, "uly": -1111950.519667},
    "h11v11": {"ulx": -7783653.637667, "uly": -2223901.039333},
    "h11v12": {"ulx": -7783653.637667, "uly": -3335851.559},
    "h12v01": {"ulx": -6671703.118, "uly": 8895604.157333},
    "h12v02": {"ulx": -6671703.118, "uly": 7783653.637667},
    "h12v03": {"ulx": -6671703.118, "uly": 6671703.118},
    "h12v04": {"ulx": -6671703.118, "uly": 5559752.598333},
    "h12v05": {"ulx": -6671703.118, "uly": 4447802.078667},
    "h12v07": {"ulx": -6671703.118, "uly": 2223901.039333},
    "h12v08": {"ulx": -6671703.118, "uly": 1111950.519667},
    "h12v09": {"ulx": -6671703.118, "uly": 0.0},
    "h12v10": {"ulx": -6671703.118, "uly": -1111950.519667},
    "h12v11": {"ulx": -6671703.118, "uly": -2223901.039333},
    "h12v12": {"ulx": -6671703.118, "uly": -3335851.559},
    "h12v13": {"ulx": -6671703.118, "uly": -4447802.078667},
    "h13v01": {"ulx": -5559752.598333, "uly": 8895604.157333},
    "h13v02": {"ulx": -5559752.598333, "uly": 7783653.637667},
    "h13v03": {"ulx": -5559752.598333, "uly": 6671703.118},
    "h13v04": {"ulx": -5559752.598333, "uly": 5559752.598333},
    "h13v08": {"ulx": -5559752.598333, "uly": 1111950.519667},
    "h13v09": {"ulx": -5559752.598333, "uly": 0.0},
    "h13v10": {"ulx": -5559752.598333, "uly": -1111950.519667},
    "h13v11": {"ulx": -5559752.598333, "uly": -2223901.039333},
    "h13v12": {"ulx": -5559752.598333, "uly": -3335851.559},
    "h13v13": {"ulx": -5559752.598333, "uly": -4447802.078667},
    "h13v14": {"ulx": -5559752.598333, "uly": -5559752.598333},
    "h14v00": {"ulx": -4447802.078667, "uly": 10007554.677},
    "h14v01": {"ulx": -4447802.078667, "uly": 8895604.157333},
    "h14v02": {"ulx": -4447802.078667, "uly": 7783653.637667},
    "h14v03": {"ulx": -4447802.078667, "uly": 6671703.118},
    "h14v04": {"ulx": -4447802.078667, "uly": 5559752.598333},
    "h14v09": {"ulx": -4447802.078667, "uly": 0.0},
    "h14v10": {"ulx": -4447802.078667, "uly": -1111950.519667},
    "h14v11": {"ulx": -4447802.078667, "uly": -2223901.039333},
    "h14v14": {"ulx": -4447802.078667, "uly": -5559752.598333},
    "h14v15": {"ulx": -4447802.078667, "uly": -6671703.118},
    "h14v16": {"ulx": -4447802.078667, "uly": -7783653.637667},
    "h14v17": {"ulx": -4447802.078667, "uly": -8895604.157333},
    "h15v00": {"ulx": -3335851.559, "uly": 10007554.677},
    "h15v01": {"ulx": -3335851.559, "uly": 8895604.157333},
    "h15v02": {"ulx": -3335851.559, "uly": 7783653.637667},
    "h15v03": {"ulx": -3335851.559, "uly": 6671703.118},
    "h15v05": {"ulx": -3335851.559, "uly": 4447802.078667},
    "h15v07": {"ulx": -3335851.559, "uly": 2223901.039333},
    "h15v11": {"ulx": -3335851.559, "uly": -2223901.039333},
    "h15v14": {"ulx": -3335851.559, "uly": -5559752.598333},
    "h15v15": {"ulx": -3335851.559, "uly": -6671703.118},
    "h15v16": {"ulx": -3335851.559, "uly": -7783653.637667},
    "h15v17": {"ulx": -3335851.559, "uly": -8895604.157333},
    "h16v00": {"ulx": -2223901.039333, "uly": 10007554.677},
    "h16v01": {"ulx": -2223901.039333, "uly": 8895604.157333},
    "h16v02": {"ulx": -2223901.039333, "uly": 7783653.637667},
    "h16v05": {"ulx": -2223901.039333, "uly": 4447802.078667},
    "h16v06": {"ulx": -2223901.039333, "uly": 3335851.559},
    "h16v07": {"ulx": -2223901.039333, "uly": 2223901.039333},
    "h16v08": {"ulx": -2223901.039333, "uly": 1111950.519667},
    "h16v09": {"ulx": -2223901.039333, "uly": 0.0},
    "h16v12": {"ulx": -2223901.039333, "uly": -3335851.559},
    "h16v14": {"ulx": -2223901.039333, "uly": -5559752.598333},
    "h16v16": {"ulx": -2223901.039333, "uly": -7783653.637667},
    "h16v17": {"ulx": -2223901.039333, "uly": -8895604.157333},
    "h17v00": {"ulx": -1111950.519667, "uly": 10007554.677},
    "h17v01": {"ulx": -1111950.519667, "uly": 8895604.157333},
    "h17v02": {"ulx": -1111950.519667, "uly": 7783653.637667},
    "h17v03": {"ulx": -1111950.519667, "uly": 6671703.118},
    "h17v04": {"ulx": -1111950.519667, "uly": 5559752.598333},
    "h17v05": {"ulx": -1111950.519667, "uly": 4447802.078667},
    "h17v06": {"ulx": -1111950.519667, "uly": 3335851.559},
    "h17v07": {"ulx": -1111950.519667, "uly": 2223901.039333},
    "h17v08": {"ulx": -1111950.519667, "uly": 1111950.519667},
    "h17v10": {"ulx": -1111950.519667, "uly": -1111950.519667},
    "h17v12": {"ulx": -1111950.519667, "uly": -3335851.559},
    "h17v13": {"ulx": -1111950.519667, "uly": -4447802.078667},
    "h17v15": {"ulx": -1111950.519667, "uly": -6671703.118},
    "h17v16": {"ulx": -1111950.519667, "uly": -7783653.637667},
    "h17v17": {"ulx": -1111950.519667, "uly": -8895604.157333},
    "h18v00": {"ulx": 0.0, "uly": 10007554.677},
    "h18v01": {"ulx": 0.0, "uly": 8895604.157333},
    "h18v02": {"ulx": 0.0, "uly": 7783653.637667},
    "h18v03": {"ulx": 0.0, "uly": 6671703.118},
    "h18v04": {"ulx": 0.0, "uly": 5559752.598333},
    "h18v05": {"ulx": 0.0, "uly": 4447802.078667},
    "h18v06": {"ulx": 0.0, "uly": 3335851.559},
    "h18v07": {"ulx": 0.0, "uly": 2223901.039333},
    "h18v08": {"ulx": 0.0, "uly": 1111950.519667},
    "h18v09": {"ulx": 0.0, "uly": 0.0},
    "h18v14": {"ulx": 0.0, "uly": -5559752.598333},
    "h18v15": {"ulx": 0.0, "uly": -6671703.118},
    "h18v16": {"ulx": 0.0, "uly": -7783653.637667},
    "h18v17": {"ulx": 0.0, "uly": -8895604.157333},
    "h19v00": {"ulx": 1111950.519667, "uly": 10007554.677},
    "h19v01": {"ulx": 1111950.519667, "uly": 8895604.157333},
    "h19v02": {"ulx": 1111950.519667, "uly": 7783653.637667},
    "h19v03": {"ulx": 1111950.519667, "uly": 6671703.118},
    "h19v04": {"ulx": 1111950.519667, "uly": 5559752.598333},
    "h19v05": {"ulx": 1111950.519667, "uly": 4447802.078667},
    "h19v06": {"ulx": 1111950.519667, "uly": 3335851.559},
    "h19v07": {"ulx": 1111950.519667, "uly": 2223901.039333},
    "h19v08": {"ulx": 1111950.519667, "uly": 1111950.519667},
    "h19v09": {"ulx": 1111950.519667, "uly": 0.0},
    "h19v10": {"ulx": 1111950.519667, "uly": -1111950.519667},
    "h19v11": {"ulx": 1111950.519667, "uly": -2223901.039333},
    "h19v12": {"ulx": 1111950.519667, "uly": -3335851.559},
    "h19v15": {"ulx": 1111950.519667, "uly": -6671703.118},
    "h19v16": {"ulx": 1111950.519667, "uly": -7783653.637667},
    "h19v17": {"ulx": 1111950.519667, "uly": -8895604.157333},
    "h20v00": {"ulx": 2223901.039333, "uly": 10007554.677},
    "h20v01": {"ulx": 2223901.039333, "uly": 8895604.157333},
    "h20v02": {"ulx": 2223901.039333, "uly": 7783653.637667},
    "h20v03": {"ulx": 2223901.039333, "uly": 6671703.118},
    "h20v04": {"ulx": 2223901.039333, "uly": 5559752.598333},
    "h20v05": {"ulx": 2223901.039333, "uly": 4447802.078667},
    "h20v06": {"ulx": 2223901.039333, "uly": 3335851.559},
    "h20v07": {"ulx": 2223901.039333, "uly": 2223901.039333},
    "h20v08": {"ulx": 2223901.039333, "uly": 1111950.519667},
    "h20v09": {"ulx": 2223901.039333, "uly": 0.0},
    "h20v10": {"ulx": 2223901.039333, "uly": -1111950.519667},
    "h20v11": {"ulx": 2223901.039333, "uly": -2223901.039333},
    "h20v12": {"ulx": 2223901.039333, "uly": -3335851.559},
    "h20v13": {"ulx": 2223901.039333, "uly": -4447802.078667},
    "h20v15": {"ulx": 2223901.039333, "uly": -6671703.118},
    "h20v16": {"ulx": 2223901.039333, "uly": -7783653.637667},
    "h20v17": {"ulx": 2223901.039333, "uly": -8895604.157333},
    "h21v00": {"ulx": 3335851.559, "uly": 10007554.677},
    "h21v01": {"ulx": 3335851.559, "uly": 8895604.157333},
    "h21v02": {"ulx": 3335851.559, "uly": 7783653.637667},
    "h21v03": {"ulx": 3335851.559, "uly": 6671703.118},
    "h21v04": {"ulx": 3335851.559, "uly": 5559752.598333},
    "h21v05": {"ulx": 3335851.559, "uly": 4447802.078667},
    "h21v06": {"ulx": 3335851.559, "uly": 3335851.559},
    "h21v07": {"ulx": 3335851.559, "uly": 2223901.039333},
    "h21v08": {"ulx": 3335851.559, "uly": 1111950.519667},
    "h21v09": {"ulx": 3335851.559, "uly": 0.0},
    "h21v10": {"ulx": 3335851.559, "uly": -1111950.519667},
    "h21v11": {"ulx": 3335851.559, "uly": -2223901.039333},
    "h21v13": {"ulx": 3335851.559, "uly": -4447802.078667},
    "h21v15": {"ulx": 3335851.559, "uly": -6671703.118},
    "h21v16": {"ulx": 3335851.559, "uly": -7783653.637667},
    "h21v17": {"ulx": 3335851.559, "uly": -8895604.157333},
    "h22v01": {"ulx": 4447802.078667, "uly": 8895604.157333},
    "h22v02": {"ulx": 4447802.078667, "uly": 7783653.637667},
    "h22v03": {"ulx": 4447802.078667, "uly": 6671703.118},
    "h22v04": {"ulx": 4447802.078667, "uly": 5559752.598333},
    "h22v05": {"ulx": 4447802.078667, "uly": 4447802.078667},
    "h22v06": {"ulx": 4447802.078667, "uly": 3335851.559},
    "h22v07": {"ulx": 4447802.078667, "uly": 2223901.039333},
    "h22v08": {"ulx": 4447802.078667, "uly": 1111950.519667},
    "h22v09": {"ulx": 4447802.078667, "uly": 0.0},
    "h22v10": {"ulx": 4447802.078667, "uly": -1111950.519667},
    "h22v11": {"ulx": 4447802.078667, "uly": -2223901.039333},
    "h22v13": {"ulx": 4447802.078667, "uly": -4447802.078667},
    "h22v14": {"ulx": 4447802.078667, "uly": -5559752.598333},
    "h22v15": {"ulx": 4447802.078667, "uly": -6671703.118},
    "h22v16": {"ulx": 4447802.078667, "uly": -7783653.637667},
    "h23v01": {"ulx": 5559752.598333, "uly": 8895604.157333},
    "h23v02": {"ulx": 5559752.598333, "uly": 7783653.637667},
    "h23v03": {"ulx": 5559752.598333, "uly": 6671703.118},
    "h23v04": {"ulx": 5559752.598333, "uly": 5559752.598333},
    "h23v05": {"ulx": 5559752.598333, "uly": 4447802.078667},
    "h23v06": {"ulx": 5559752.598333, "uly": 3335851.559},
    "h23v07": {"ulx": 5559752.598333, "uly": 2223901.039333},
    "h23v08": {"ulx": 5559752.598333, "uly": 1111950.519667},
    "h23v09": {"ulx": 5559752.598333, "uly": 0.0},
    "h23v10": {"ulx": 5559752.598333, "uly": -1111950.519667},
    "h23v11": {"ulx": 5559752.598333, "uly": -2223901.039333},
    "h23v15": {"ulx": 5559752.598333, "uly": -6671703.118},
    "h23v16": {"ulx": 5559752.598333, "uly": -7783653.637667},
    "h24v01": {"ulx": 6671703.118, "uly": 8895604.157333},
    "h24v02": {"ulx": 6671703.118, "uly": 7783653.637667},
    "h24v03": {"ulx": 6671703.118, "uly": 6671703.118},
    "h24v04": {"ulx": 6671703.118, "uly": 5559752.598333},
    "h24v05": {"ulx": 6671703.118, "uly": 4447802.078667},
    "h24v06": {"ulx": 6671703.118, "uly": 3335851.559},
    "h24v07": {"ulx": 6671703.118, "uly": 2223901.039333},
    "h24v10": {"ulx": 6671703.118, "uly": -1111950.519667},
    "h24v12": {"ulx": 6671703.118, "uly": -3335851.559},
    "h24v15": {"ulx": 6671703.118, "uly": -6671703.118},
    "h24v16": {"ulx": 6671703.118, "uly": -7783653.637667},
    "h25v02": {"ulx": 7783653.637667, "uly": 7783653.637667},
    "h25v03": {"ulx": 7783653.637667, "uly": 6671703.118},
    "h25v04": {"ulx": 7783653.637667, "uly": 5559752.598333},
    "h25v05": {"ulx": 7783653.637667, "uly": 4447802.078667},
    "h25v06": {"ulx": 7783653.637667, "uly": 3335851.559},
    "h25v07": {"ulx": 7783653.637667, "uly": 2223901.039333},
    "h25v08": {"ulx": 7783653.637667, "uly": 1111950.519667},
    "h25v09": {"ulx": 7783653.637667, "uly": 0.0},
    "h26v02": {"ulx": 8895604.157333, "uly": 7783653.637667},
    "h26v03": {"ulx": 8895604.157333, "uly": 6671703.118},
    "h26v04": {"ulx": 8895604.157333, "uly": 5559752.598333},
    "h26v05": {"ulx": 8895604.157333, "uly": 4447802.078667},
    "h26v06": {"ulx": 8895604.157333, "uly": 3335851.559},
    "h26v07": {"ulx": 8895604.157333, "uly": 2223901.039333},
    "h26v08": {"ulx": 8895604.157333, "uly": 1111950.519667},
    "h27v03": {"ulx": 10007554.677, "uly": 6671703.118},
    "h27v04": {"ulx": 10007554.677, "uly": 5559752.598333},
    "h27v05": {"ulx": 10007554.677, "uly": 4447802.078667},
    "h27v06": {"ulx": 10007554.677, "uly": 3335851.559},
    "h27v07": {"ulx": 10007554.677, "uly": 2223901.039333},
    "h27v08": {"ulx": 10007554.677, "uly": 1111950.519667},
    "h27v09": {"ulx": 10007554.677, "uly": 0.0},
    "h27v10": {"ulx": 10007554.677, "uly": -1111950.519667},
    "h27v11": {"ulx": 10007554.677, "uly": -2223901.039333},
    "h27v12": {"ulx": 10007554.677, "uly": -3335851.559},
    "h27v14": {"ulx": 10007554.677, "uly": -5559752.598333},
    "h28v03": {"ulx": 11119505.196667, "uly": 6671703.118},
    "h28v04": {"ulx": 11119505.196667, "uly": 5559752.598333},
    "h28v05": {"ulx": 11119505.196667, "uly": 4447802.078667},
    "h28v06": {"ulx": 11119505.196667, "uly": 3335851.559},
    "h28v07": {"ulx": 11119505.196667, "uly": 2223901.039333},
    "h28v08": {"ulx": 11119505.196667, "uly": 1111950.519667},
    "h28v09": {"ulx": 11119505.196667, "uly": 0.0},
    "h28v10": {"ulx": 11119505.196667, "uly": -1111950.519667},
    "h28v11": {"ulx": 11119505.196667, "uly": -2223901.039333},
    "h28v12": {"ulx": 11119505.196667, "uly": -3335851.559},
    "h28v13": {"ulx": 11119505.196667, "uly": -4447802.078667},
    "h28v14": {"ulx": 11119505.196667, "uly": -5559752.598333},
    "h29v03": {"ulx": 12231455.716333, "uly": 6671703.118},
    "h29v05": {"ulx": 12231455.716333, "uly": 4447802.078667},
    "h29v06": {"ulx": 12231455.716333, "uly": 3335851.559},
    "h29v07": {"ulx": 12231455.716333, "uly": 2223901.039333},
    "h29v08": {"ulx": 12231455.716333, "uly": 1111950.519667},
    "h29v09": {"ulx": 12231455.716333, "uly": 0.0},
    "h29v10": {"ulx": 12231455.716333, "uly": -1111950.519667},
    "h29v11": {"ulx": 12231455.716333, "uly": -2223901.039333},
    "h29v12": {"ulx": 12231455.716333, "uly": -3335851.559},
    "h29v13": {"ulx": 12231455.716333, "uly": -4447802.078667},
    "h30v04": {"ulx": 13343406.236, "uly": 5559752.598333},
    "h30v05": {"ulx": 13343406.236, "uly": 4447802.078667},
    "h30v06": {"ulx": 13343406.236, "uly": 3335851.559},
    "h30v07": {"ulx": 13343406.236, "uly": 2223901.039333},
    "h30v08": {"ulx": 13343406.236, "uly": 1111950.519667},
    "h30v09": {"ulx": 13343406.236, "uly": 0.0},
    "h30v10": {"ulx": 13343406.236, "uly": -1111950.519667},
    "h30v11": {"ulx": 13343406.236, "uly": -2223901.039333},
    "h30v12": {"ulx": 13343406.236, "uly": -3335851.559},
    "h30v13": {"ulx": 13343406.236, "uly": -4447802.078667},
    "h31v04": {"ulx": 14455356.755667, "uly": 5559752.598333},
    "h31v06": {"ulx": 14455356.755667, "uly": 3335851.559},
    "h31v07": {"ulx": 14455356.755667, "uly": 2223901.039333},
    "h31v08": {"ulx": 14455356.755667, "uly": 1111950.519667},
    "h31v09": {"ulx": 14455356.755667, "uly": 0.0},
    "h31v10": {"ulx": 14455356.755667, "uly": -1111950.519667},
    "h31v11": {"ulx": 14455356.755667, "uly": -2223901.039333},
    "h31v12": {"ulx": 14455356.755667, "uly": -3335851.559},
    "h31v13": {"ulx": 14455356.755667, "uly": -4447802.078667},
    "h32v07": {"ulx": 15567307.275333, "uly": 2223901.039333},
    "h32v08": {"ulx": 15567307.275333, "uly": 1111950.519667},
    "h32v09": {"ulx": 15567307.275333, "uly": 0.0},
    "h32v10": {"ulx": 15567307.275333, "uly": -1111950.519667},
    "h32v11": {"ulx": 15567307.275333, "uly": -2223901.039333},
    "h32v12": {"ulx": 15567307.275333, "uly": -3335851.559},
    "h33v07": {"ulx": 16679257.795, "uly": 2223901.039333},
    "h33v08": {"ulx": 16679257.795, "uly": 1111950.519667},
    "h33v09": {"ulx": 16679257.795, "uly": 0.0},
    "h33v10": {"ulx": 16679257.795, "uly": -1111950.519667},
    "h33v11": {"ulx": 16679257.795, "uly": -2223901.039333},
    "h34v07": {"ulx": 17791208.314667, "uly": 2223901.039333},
    "h34v08": {"ulx": 17791208.314667, "uly": 1111950.519667},
    "h34v09": {"ulx": 17791208.314667, "uly": 0.0},
    "h34v10": {"ulx": 17791208.314667, "uly": -1111950.519667},
    "h35v08": {"ulx": 18903158.834333, "uly": 1111950.519667},
    "h35v09": {"ulx": 18903158.834333, "uly": 0.0},
    "h35v10": {"ulx": 18903158.834333, "uly": -1111950.519667},
}


# 将不同类型输入的hv转为字符串
def get_hv_string(hv: Union[str, Tuple[int, int]]) -> str:
    # 如果hv是字符串, 并且包含逗号, 则转为元组
    if isinstance(hv, str) and "," in hv:
        hv = tuple(map(int, hv.split(",")))
    # 检查hv
    if isinstance(hv, str):  # 检查hv是否是字符串, 如果是则直接返回
        return hv
    elif isinstance(hv, tuple) and len(hv) == 2:  # 检查hv是否是元组, 如果是则转为字符串
        return f"h{hv[0]:02d}v{hv[1]:02d}"
    else:
        raise ValueError(f"Invalid hv {hv}, should be str (like 'h01v01', '1,1') or tuple of int")


def get_transform(hv: str, grid: str = "1km") -> rio.Affine:
    # 根据grid获取dx, dy
    if grid == "1km":
        dx = GRIDDX_1KM
        dy = GRIDDY_1KM
    elif grid == "500m":
        dx = GRIDDX_500M
        dy = GRIDDY_500M
    else:
        raise ValueError("Only support 1km or 500m grid")
    # 根据hv获取ulx, uly
    if hv not in PROJECTIONPARASDICT:
        raise ValueError(f"Invalid hv {hv}, please check the PROJECTIONPARASDICT keys in '.convert.py'")
    ulx = PROJECTIONPARASDICT[hv]["ulx"]
    uly = PROJECTIONPARASDICT[hv]["uly"]
    # 返回rio.Affine对象
    ProjectionPara = (ulx, dx, 0, uly, 0, dy)
    crs_transform = rio.Affine.from_gdal(*map(float, ProjectionPara))
    return crs_transform


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
    profile.update(
        {
            "dtype": kwargs.get("dtype", arr.dtype),
            "count": bands,
            "width": width,
            "height": height,
            "crs": Sinusoidal.crs,
            "transform": get_transform(get_hv_string(hv), grid),
        }
    )
    # 写入tiff文件
    with rio.open(tiff_path, "w", **profile) as ds:
        ds.write(arr)