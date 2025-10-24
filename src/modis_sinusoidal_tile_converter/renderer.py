import numpy as np
from pathlib import Path
from PIL import Image
from matplotlib import colormaps

class Renderer:
    """瓦片渲染器
    
    将瓦片数据渲染为各种格式的图像
    """

    @staticmethod
    def clip_and_normalize(data, vmin=0, vmax=1):
        """剪裁和归一化数据
        
        Args:
            data: 输入数据数组
            vmin: 数据范围最小值
            vmax: 数据范围最大值
        """
        data = np.clip(data, vmin, vmax)
        data = (data - vmin) / (vmax - vmin)
        return data

    @staticmethod
    def to_image(rgba) -> Image.Image:
        return Image.fromarray(rgba, mode='RGBA')


    @staticmethod
    def to_rgba(data: np.ndarray, nan_mask: np.ndarray = None, colormap: str = "gray") -> np.ndarray:
        # 应用色带
        cmap = colormaps[colormap]
        rgba = cmap(data)  # 返回RGBA数组，shape为(H, W, 4)
        
        # 将RGBA从0-1范围转换到0-255
        rgba = (rgba * 255).astype(np.uint8)
        
        # 将nan位置设为完全透明
        rgba[nan_mask, 3] = 0
        
        return rgba
    
    @staticmethod
    def save(image: Image.Image, output_path: str, format: str = "PNG"):
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        image.save(output_path, format)
    
    @staticmethod
    def render_single_band(data: np.ndarray, output_path: str=None, format: str="WEBP", colormap: str = "gray",
                       vmin=0, vmax=1, nan_value=None):
        """渲染为彩色图像（使用matplotlib色带）
        
        Args:
            data: 输入数据数组
            output_path: 输出文件路径
            format: 输出文件格式
            colormap: 色带名称，如 'viridis', 'jet', 'plasma' 等
            vmin: 数据范围最小值
            vmax: 数据范围最大值
            nan_value: 指定哪个值应被视为NaN，如果为None，则使用np.isnan(data)
        """
        if data.ndim != 2:
            raise ValueError("数据必须是2D数组")
        data_copy = data.copy()

        # 处理nan_value
        nan_mask = np.zeros_like(data_copy, dtype=bool)
        if nan_value is not None:
            nan_mask[data_copy == nan_value] = True
        else:
            nan_mask = np.isnan(data_copy)

        clipped_data = Renderer.clip_and_normalize(data_copy, vmin, vmax)
        rgba = Renderer.to_rgba(clipped_data, nan_mask, colormap)
        image = Renderer.to_image(rgba)
        if output_path is not None:
            Renderer.save(image, output_path, format)
        return image
    