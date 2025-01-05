import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
import numpy as np
import torch
import torchvision.transforms as t

class AD_PosterMaker:
    """Advanced poster maker with scaling, border, background and composition."""
    
    COLOR_PRESETS = {
        "white": "#FFFFFF",
        "black": "#000000",
        "gray": "#808080",
        "custom": "custom"
    }
    
    def __init__(self):
        pass

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    FUNCTION = "create_poster"
    CATEGORY = "🌻 Addoor/image"
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "scale": ("FLOAT", {
                    "default": 0.8,
                    "min": 0.1,
                    "max": 1.0,
                    "step": 0.05,
                    "description": "Scale factor for the inner image"
                }),
                "border_size": ("INT", {
                    "default": 32,
                    "min": 0,
                    "max": 256,
                    "step": 4,
                    "description": "Border size in pixels"
                }),
                "border_color": (list(cls.COLOR_PRESETS.keys()), {
                    "default": "white"
                }),
                "border_hex": ("STRING", {
                    "default": "#FFFFFF",
                    "multiline": False
                }),
                "background_color": (list(cls.COLOR_PRESETS.keys()), {
                    "default": "white"
                }),
                "background_hex": ("STRING", {
                    "default": "#FFFFFF",
                    "multiline": False
                }),
                "position": (["left", "right", "top", "bottom"], {
                    "default": "right",
                    "description": "Position of the original image"
                }),
                "method": (["lanczos", "bicubic", "bilinear"], {
                    "default": "lanczos",
                    "description": "Resampling method"
                }),
            },
            "optional": {
                "watermark": ("IMAGE",),
                "original_image": ("IMAGE",),
            }
        }

    def hex_to_rgb(self, hex_color: str) -> tuple:
        """Convert hex color to RGB tuple."""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def create_poster(
        self,
        image,
        scale: float,
        border_size: int,
        border_color: str,
        border_hex: str,
        background_color: str,
        background_hex: str,
        position: str,
        method: str,
        watermark = None,
        original_image = None,
    ):
        try:
            # 转换输入图像为PIL
            original = tensor_to_image(image[0])
            
            # 创建带边框的图
            bg_rgb = self.hex_to_rgb(self.COLOR_PRESETS[background_color] if background_color != "custom" else background_hex)
            background = Image.new(
                "RGB",
                (original.width + border_size * 2, original.height + border_size * 2),
                bg_rgb
            )
            background.paste(original, (border_size, border_size))
            
            # 处理水印
            if watermark is not None:
                watermark_img = tensor_to_image(watermark[0])
                if watermark_img.mode != 'RGBA':
                    watermark_img = watermark_img.convert('RGBA')
                watermark_img = watermark_img.resize(background.size, get_sampler_by_name(method))
                background = background.convert('RGBA')
                background = Image.alpha_composite(background, watermark_img)
                background = background.convert('RGB')
            
            # 获取目标尺寸（根据original_image或原始image）
            if original_image is not None:
                _, target_h, target_w, _ = original_image.shape
                target_img = tensor_to_image(original_image[0])
            else:
                target_w, target_h = original.size
                target_img = original
            
            # 根据拼接方向调整边框图尺寸
            is_horizontal = position in ["left", "right"]
            if is_horizontal:
                # 横排，高度需要匹配
                ratio = target_h / background.height
                new_width = int(background.width * ratio)
                new_height = target_h
            else:
                # 竖排，宽度需要匹配
                ratio = target_w / background.width
                new_width = target_w
                new_height = int(background.height * ratio)
            
            # 调整边框图尺寸
            background = background.resize((new_width, new_height), get_sampler_by_name(method))
            print(f"Adjusted background size: {new_width}x{new_height}")
            
            # 创建最终图像并拼接
            if is_horizontal:
                final_width = new_width + target_w
                final_height = max(new_height, target_h)
            else:
                final_width = max(new_width, target_w)
                final_height = new_height + target_h
            
            final_image = Image.new("RGB", (final_width, final_height))
            
            # 根据位置拼接
            if position == "left":
                final_image.paste(target_img, (0, 0))
                final_image.paste(background, (target_w, 0))
            elif position == "right":
                final_image.paste(background, (0, 0))
                final_image.paste(target_img, (new_width, 0))
            elif position == "top":
                final_image.paste(target_img, (0, 0))
                final_image.paste(background, (0, target_h))
            else:  # bottom
                final_image.paste(background, (0, 0))
                final_image.paste(target_img, (0, new_height))
            
            # 转换回tensor
            tensor = image_to_tensor(final_image)
            tensor = tensor.unsqueeze(0)
            tensor = tensor.permute(0, 2, 3, 1)
            
            return (tensor,)
            
        except Exception as e:
            print(f"Error creating poster: {str(e)}")
            return (image,)

def get_sampler_by_name(method: str) -> int:
    """Get PIL resampling method by name."""
    samplers = {
        "lanczos": Image.LANCZOS,
        "bicubic": Image.BICUBIC,
        "bilinear": Image.BILINEAR,
    }
    return samplers.get(method, Image.LANCZOS)

def tensor_to_image(tensor):
    """Convert tensor to PIL Image."""
    if len(tensor.shape) == 4:
        tensor = tensor.squeeze(0)
    return t.ToPILImage()(tensor.permute(2, 0, 1))

def image_to_tensor(image):
    """Convert PIL Image to tensor."""
    tensor = t.ToTensor()(image)
    return tensor

NODE_CLASS_MAPPINGS = {
    "AD_poster-maker": AD_PosterMaker,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "AD_poster-maker": "AD Poster Maker",
} 