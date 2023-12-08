from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version(__package__)
except PackageNotFoundError:
    __version__ = "unknown version"
    
from modis_sinusoidal_tile_converter.sinusoidal import Sinusoidal