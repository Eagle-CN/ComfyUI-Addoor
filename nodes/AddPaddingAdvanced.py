"""
@author: ComfyNodePRs
@title: ComfyUI Advanced Padding
@description: Advanced padding node with scaling capabilities
@version: 1.0.0
@project: https://github.com/ComfyNodePRs/advanced-padding
@author: https://github.com/ComfyNodePRs
"""

import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
import numpy as np
import torch
import torchvision.transforms as t


class AD_PaddingAdvanced:
    def __init__(self):
        pass
     
    FUNCTION = "process_image"
    CATEGORY = "🌻 Addoor/image"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "scale_by": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.1,
                    "max": 8.0,
                    "step": 0.05,
                    "display": "number"
                }),
                "upscale_method": (["nearest-exact", "bilinear", "bicubic", "lanczos"], {"default": "lanczos"}),
                "left": ("INT", {"default": 0, "step": 1, "min": 0, "max": 4096}),
                "top": ("INT", {"default": 0, "step": 1, "min": 0, "max": 4096}),
                "right": ("INT", {"default": 0, "step": 1, "min": 0, "max": 4096}),
                "bottom": ("INT", {"default": 0, "step": 1, "min": 0, "max": 4096}),
                "color": ("STRING", {"default": "#ffffff"}),
                "transparent": ("BOOLEAN", {"default": False}),
            },
            "optional": {
                "background": ("IMAGE",),
            }
        }
    
    RETURN_TYPES = ("IMAGE", "MASK")
    RETURN_NAMES = ("image", "mask")

    def add_padding(self, image, left, top, right, bottom, color="#ffffff", transparent=False):
        padded_images = []
        image = [self.tensor2pil(img) for img in image]
        for img in image:
            padded_image = Image.new("RGBA" if transparent else "RGB", 
                 (img.width + left + right, img.height + top + bottom), 
                 (0, 0, 0, 0) if transparent else self.hex_to_tuple(color))
            padded_image.paste(img, (left, top))
            padded_images.append(self.pil2tensor(padded_image))
        return torch.cat(padded_images, dim=0)
     
    def create_mask(self, image, left, top, right, bottom):
        masks = []
        image = [self.tensor2pil(img) for img in image]
        for img in image:
            shape = (left, top, img.width + left, img.height + top)
            mask_image = Image.new("L", (img.width + left + right, img.height + top + bottom), 255)
            draw = ImageDraw.Draw(mask_image)
            draw.rectangle(shape, fill=0)
            masks.append(self.pil2tensor(mask_image))
        return torch.cat(masks, dim=0)

    def scale_image(self, image, scale_by, method):
        scaled_images = []
        image = [self.tensor2pil(img) for img in image]
        
        resampling_methods = {
            "nearest-exact": Image.Resampling.NEAREST,
            "bilinear": Image.Resampling.BILINEAR,
            "bicubic": Image.Resampling.BICUBIC,
            "lanczos": Image.Resampling.LANCZOS,
        }
        
        for img in image:
            # 计算新尺寸
            new_width = int(img.width * scale_by)
            new_height = int(img.height * scale_by)
            
            # 使用选定的方法进行缩放
            scaled_img = img.resize(
                (new_width, new_height),
                resampling_methods.get(method, Image.Resampling.LANCZOS)
            )
            scaled_images.append(self.pil2tensor(scaled_img))
            
        return torch.cat(scaled_images, dim=0)
     
    def hex_to_tuple(self, color):
        if not isinstance(color, str):
            raise ValueError("Color must be a hex string")
        color = color.strip("#")
        return tuple([int(color[i:i + 2], 16) for i in range(0, len(color), 2)])
     
    def tensor2pil(self, image):
        return Image.fromarray(np.clip(255. * image.cpu().numpy().squeeze(), 0, 255).astype(np.uint8))
    
    def pil2tensor(self, image):
        return torch.from_numpy(np.array(image).astype(np.float32) / 255.0).unsqueeze(0)

    def composite_with_background(self, image, background):
        """将图片居中合成到背景上"""
        image_pil = self.tensor2pil(image[0])  # 获取第一帧
        bg_pil = self.tensor2pil(background[0])
        
        # 创建新的景图像
        result = bg_pil.copy()
        
        # 计算居中位置
        x = (bg_pil.width - image_pil.width) // 2
        y = (bg_pil.height - image_pil.height) // 2
        
        # 如果前景图比背景大，需要裁剪
        if image_pil.width > bg_pil.width or image_pil.height > bg_pil.height:
            # 计算裁剪区域
            crop_left = max(0, (image_pil.width - bg_pil.width) // 2)
            crop_top = max(0, (image_pil.height - bg_pil.height) // 2)
            crop_right = min(image_pil.width, crop_left + bg_pil.width)
            crop_bottom = min(image_pil.height, crop_top + bg_pil.height)
            
            # 裁剪图片
            image_pil = image_pil.crop((crop_left, crop_top, crop_right, crop_bottom))
            
            # 更新粘贴位置
            x = max(0, (bg_pil.width - image_pil.width) // 2)
            y = max(0, (bg_pil.height - image_pil.height) // 2)
        
        # 如果前景图有透明通道，使用alpha通道合成
        if image_pil.mode == 'RGBA':
            result.paste(image_pil, (x, y), image_pil)
        else:
            result.paste(image_pil, (x, y))
        
        return self.pil2tensor(result)

    def process_image(self, image, scale_by, upscale_method, left, top, right, bottom, color, transparent, background=None):
        # 首先进行缩放
        if scale_by != 1.0:
            image = self.scale_image(image, scale_by, upscale_method)
        
        # 添加padding
        padded_image = self.add_padding(image, left, top, right, bottom, color, transparent)
        
        # 如果有背景图，进行合成
        if background is not None:
            result = []
            for i in range(len(padded_image)):
                # 处理每一帧
                frame = padded_image[i:i+1]
                composited = self.composite_with_background(frame, background)
                result.append(composited)
            padded_image = torch.cat(result, dim=0)
        
        # 创建mask
        mask = self.create_mask(image, left, top, right, bottom)
        
        return (padded_image, mask)


class AD_ImageConcat:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image1": ("IMAGE",),
                "image2": ("IMAGE",),
                "direction": (["horizontal", "vertical"], {"default": "horizontal"}),
                "match_size": ("BOOLEAN", {"default": True}),
                "method": (["lanczos", "bicubic", "bilinear", "nearest"], {"default": "lanczos"}),
            }
        }
    
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "concat_images"
    CATEGORY = "🌻 Addoor/image"

    def concat_images(self, image1, image2, direction="horizontal", match_size=False, method="lanczos"):
        try:
            # 转换为 PIL 图像
            img1 = tensor_to_image(image1[0])
            img2 = tensor_to_image(image2[0])
            
            # 确保两张图片的模式相同
            if img1.mode != img2.mode:
                if 'A' in img1.mode or 'A' in img2.mode:
                    img1 = img1.convert('RGBA')
                    img2 = img2.convert('RGBA')
                else:
                    img1 = img1.convert('RGB')
                    img2 = img2.convert('RGB')

            # 如果需要匹配尺寸
            if match_size:
                if direction == "horizontal":
                    # 横向拼接，匹配高度
                    if img1.height != img2.height:
                        new_height = img2.height
                        new_width = int(img1.width * (new_height / img1.height))
                        img1 = img1.resize(
                            (new_width, new_height),
                            get_sampler_by_name(method)
                        )
                else:  # vertical
                    # 纵向拼接，匹配宽度
                    if img1.width != img2.width:
                        new_width = img2.width
                        new_height = int(img1.height * (new_width / img1.width))
                        img1 = img1.resize(
                            (new_width, new_height),
                            get_sampler_by_name(method)
                        )

            # 创建新图像
            if direction == "horizontal":
                new_width = img1.width + img2.width
                new_height = max(img1.height, img2.height)
            else:  # vertical
                new_width = max(img1.width, img2.width)
                new_height = img1.height + img2.height

            # 创建新的画布
            mode = img1.mode
            new_image = Image.new(mode, (new_width, new_height))

            # 计算粘贴位置（居中对齐）
            if direction == "horizontal":
                y1 = (new_height - img1.height) // 2
                y2 = (new_height - img2.height) // 2
                new_image.paste(img1, (0, y1))
                new_image.paste(img2, (img1.width, y2))
            else:  # vertical
                x1 = (new_width - img1.width) // 2
                x2 = (new_width - img2.width) // 2
                new_image.paste(img1, (x1, 0))
                new_image.paste(img2, (x2, img1.height))

            # 转换回 tensor
            tensor = image_to_tensor(new_image)
            tensor = tensor.unsqueeze(0)
            tensor = tensor.permute(0, 2, 3, 1)
            
            return (tensor,)
            
        except Exception as e:
            print(f"Error concatenating images: {str(e)}")
            return (image1,)


# 添加颜色常量
COLORS = [
    "white", "black", "red", "green", "blue", "yellow", "purple", "orange",
    "gray", "brown", "pink", "cyan", "custom"
]

# 颜色映射
color_mapping = {
    "white": "#FFFFFF",
    "black": "#000000",
    "red": "#FF0000",
    "green": "#00FF00",
    "blue": "#0000FF",
    "yellow": "#FFFF00",
    "purple": "#800080",
    "orange": "#FFA500",
    "gray": "#808080",
    "brown": "#A52A2A",
    "pink": "#FFC0CB",
    "cyan": "#00FFFF"
}

def get_color_values(color_name, color_hex, mapping):
    """获取颜色值"""
    if color_name == "custom":
        return color_hex
    return mapping.get(color_name, "#000000")

# 添加图像处理工具函数
def get_sampler_by_name(method: str) -> int:
    """Get PIL resampling method by name."""
    samplers = {
        "lanczos": Image.LANCZOS,
        "bicubic": Image.BICUBIC,
        "hamming": Image.HAMMING,
        "bilinear": Image.BILINEAR,
        "box": Image.BOX,
        "nearest": Image.NEAREST
    }
    return samplers.get(method, Image.LANCZOS)

class AD_ColorImage:
    """Create a solid color image with advanced options."""
    
    def __init__(self):
        pass

    # 预定义颜色映射
    COLOR_PRESETS = {
        "white": "#FFFFFF",
        "black": "#000000",
        "red": "#FF0000",
        "green": "#00FF00",
        "blue": "#0000FF",
        "yellow": "#FFFF00",
        "purple": "#800080",
        "orange": "#FFA500",
        "gray": "#808080",
        "custom": "custom"
    }
     
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "width": ("INT", {
                    "default": 512,
                    "min": 1,
                    "max": 8192,
                    "step": 1
                }),
                "height": ("INT", {
                    "default": 512,
                    "min": 1,
                    "max": 8192,
                    "step": 1
                }),
                "color": (list(cls.COLOR_PRESETS.keys()), {
                    "default": "white"
                }),
                "hex_color": ("STRING", {
                    "default": "#FFFFFF",
                    "multiline": False
                }),
                "alpha": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01
                }),
            },
            "optional": {
                "reference_image": ("IMAGE",),
            }
        }
    
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    FUNCTION = "create_color_image"
    CATEGORY = "🌻 Addoor/image"

    def hex_to_rgb(self, hex_color: str) -> tuple:
        """Convert hex color to RGB tuple."""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def create_color_image(
        self,
        width: int,
        height: int,
        color: str,
        hex_color: str,
        alpha: float,
        reference_image = None
    ):
        try:
            # 如果有参考图片，使用其尺寸
            if reference_image is not None:
                _, height, width, _ = reference_image.shape
            
            # 获取颜色值
            if color == "custom":
                rgb_color = self.hex_to_rgb(hex_color)
            else:
                rgb_color = self.hex_to_rgb(self.COLOR_PRESETS[color])
            
            # 创建图像
            canvas = Image.new(
                "RGBA",
                (width, height),
                (*rgb_color, int(alpha * 255))
            )
            
            # 转换为 tensor
            tensor = image_to_tensor(canvas)
            tensor = tensor.unsqueeze(0)
            tensor = tensor.permute(0, 2, 3, 1)
            
            return (tensor,)
            
        except Exception as e:
            print(f"Error creating color image: {str(e)}")
            canvas = Image.new(
                "RGB",
                (width, height),
                (0, 0, 0)
            )
            tensor = image_to_tensor(canvas)
            tensor = tensor.unsqueeze(0)
            tensor = tensor.permute(0, 2, 3, 1)
            return (tensor,)

def tensor_to_image(tensor):
    """Convert tensor to PIL Image."""
    if len(tensor.shape) == 4:
        tensor = tensor.squeeze(0)  # 移除 batch 维度
    return t.ToPILImage()(tensor.permute(2, 0, 1))

def image_to_tensor(image):
    """Convert PIL Image to tensor."""
    tensor = t.ToTensor()(image)
    return tensor

NODE_CLASS_MAPPINGS = {
    "AD_advanced-padding": AD_PaddingAdvanced,
    "AD_image-concat": AD_ImageConcat,
    "AD_color-image": AD_ColorImage,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "AD_advanced-padding": "AD Advanced Padding",
    "AD_image-concat": "AD Image Concatenation",
    "AD_color-image": "AD Color Image",
} 