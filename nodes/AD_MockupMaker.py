import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
import PIL.ImageFilter as ImageFilter
import numpy as np
import torch
import torchvision.transforms as t
import math

class AD_MockupMaker:
    """Create mockup with scaled image overlay and blurred background."""
    
    def __init__(self):
        pass

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    FUNCTION = "create_mockup"
    CATEGORY = "🌻 Addoor/image"
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "overlay_image": ("IMAGE",),
                "background_image": ("IMAGE",),
                "target_width": ("INT", {
                    "default": 512,
                    "min": 64,
                    "max": 4096,
                    "step": 8,
                    "description": "Target width for the overlay"
                }),
                "target_height": ("INT", {
                    "default": 512,
                    "min": 64,
                    "max": 4096,
                    "step": 8,
                    "description": "Target height for the overlay"
                }),
                "corner_radius": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 500,
                    "step": 1,
                    "description": "Radius for rounded corners"
                }),
                "offset_x": ("INT", {
                    "default": 0,
                    "min": -1000,
                    "max": 1000,
                    "step": 1,
                    "description": "Horizontal offset in pixels"
                }),
                "offset_y": ("INT", {
                    "default": 0,
                    "min": -1000,
                    "max": 1000,
                    "step": 1,
                    "description": "Vertical offset in pixels"
                }),
                "blur_radius": ("FLOAT", {
                    "default": 10.0,
                    "min": 0.0,
                    "max": 50.0,
                    "step": 0.5,
                    "description": "Gaussian blur radius for background"
                }),
                "SSAA": ("INT", {
                    "default": 2,
                    "min": 1,
                    "max": 4,
                    "step": 1,
                    "description": "Super Sampling Anti-Aliasing factor"
                }),
                "method": (["lanczos", "bicubic", "bilinear"], {
                    "default": "lanczos",
                    "description": "Resampling method"
                }),
            },
            "optional": {
                "watermark": ("IMAGE",),
                "mask": ("MASK",),
            }
        }

    def add_corners(self, image, radius, ssaa=1):
        """Add rounded corners to an image."""
        if radius <= 0:
            return image
            
        # 调整圆角半径以适应SSAA
        working_radius = radius * ssaa
        
        # 创建圆角蒙版
        mask = Image.new('L', image.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle(
            [(0, 0), (image.width, image.height)],
            radius=working_radius,
            fill=255
        )
        
        # 确保图像为RGBA模式
        output = image.convert('RGBA')
        output.putalpha(mask)
        
        return output

    def fit_and_crop(self, image, target_width, target_height, method, ssaa=1):
        """Fit image to target size maintaining aspect ratio and crop if necessary."""
        # 计算SSAA尺寸
        ssaa_width = target_width * ssaa
        ssaa_height = target_height * ssaa
        
        # 计算目标尺寸与原始尺寸的比例
        width_ratio = ssaa_width / image.width
        height_ratio = ssaa_height / image.height
        
        # 使用较大的比例来确保填充目标区域
        scale = max(width_ratio, height_ratio)
        
        # 缩放图像
        new_width = int(image.width * scale)
        new_height = int(image.height * scale)
        resized = image.resize((new_width, new_height), method)
        
        # 计算裁切区域
        left = (new_width - ssaa_width) // 2
        top = (new_height - ssaa_height) // 2
        right = left + ssaa_width
        bottom = top + ssaa_height
        
        # 裁切到目标尺寸
        cropped = resized.crop((left, top, right, bottom))
        return cropped

    def create_mockup(
        self,
        overlay_image,
        background_image,
        target_width: int,
        target_height: int,
        corner_radius: int,
        offset_x: int,
        offset_y: int,
        blur_radius: float,
        SSAA: int,
        method: str,
        watermark = None,
        mask = None,
    ):
        try:
            print("Starting mockup creation...")
            
            # 1. 初始化图像
            overlay = tensor_to_image(overlay_image[0])
            background = tensor_to_image(background_image[0])
            
            print(f"Original sizes - Overlay: {overlay.size}, Background: {background.size}")
            
            # 2. 调整背景图尺寸并模糊
            background = background.resize(
                (overlay.width, overlay.height),
                get_sampler_by_name(method)
            )
            
            if blur_radius > 0:
                background = background.filter(ImageFilter.GaussianBlur(radius=blur_radius))
            
            # 3. 缩放并裁切主图
            scaled_overlay = self.fit_and_crop(
                overlay,
                target_width,
                target_height,
                get_sampler_by_name(method),
                SSAA
            )
            
            print(f"After scaling - Overlay: {scaled_overlay.size}")
            
            # 4. 转换为RGBA模式
            scaled_overlay = scaled_overlay.convert('RGBA')
            
            # 5. 添加圆角
            if corner_radius > 0:
                scaled_overlay = self.add_corners(scaled_overlay, corner_radius, SSAA)
            
            # 6. 如果使用了SSAA，缩小到目标尺寸
            if SSAA > 1:
                scaled_overlay = scaled_overlay.resize(
                    (target_width, target_height),
                    get_sampler_by_name(method)
                )
            
            # 7. 应用mask遮罩（如果有）
            if mask is not None:
                try:
                    # 处理mask维度
                    if len(mask.shape) == 3:
                        mask = mask.squeeze(0)
                    if len(mask.shape) == 3:
                        mask = mask.squeeze(-1)
                    
                    # 转换mask为PIL Image
                    mask_array = mask.cpu().numpy()
                    mask_array = (mask_array * 255).astype(np.uint8)
                    mask_img = Image.fromarray(mask_array, mode='L')
                    
                    # 首先将mask调整到原图尺寸
                    mask_img = mask_img.resize(
                        (background.width, background.height),
                        get_sampler_by_name(method)
                    )
                    
                    # 然后裁切出需要的部分（与scaled_overlay相同大小的区域）
                    crop_x = (background.width - scaled_overlay.width) // 2 + offset_x
                    crop_y = (background.height - scaled_overlay.height) // 2 + offset_y
                    mask_img = mask_img.crop((
                        crop_x,
                        crop_y,
                        crop_x + scaled_overlay.width,
                        crop_y + scaled_overlay.height
                    ))
                    
                    print(f"Mask size: {mask_img.size}, Overlay size: {scaled_overlay.size}")
                    
                    # 获取当前alpha通道
                    r, g, b, a = scaled_overlay.split()
                    
                    # 合并mask和现有alpha通道
                    if corner_radius > 0:
                        # 如果有圆角，将mask与现有alpha通道相乘
                        combined_alpha = Image.fromarray(
                            (np.array(mask_img) * np.array(a) / 255).astype(np.uint8)
                        )
                    else:
                        # 如果没有圆角，直接使用mask
                        combined_alpha = mask_img
                    
                    # 更新alpha通道
                    scaled_overlay.putalpha(combined_alpha)
                    print("Mask applied successfully")
                    
                except Exception as e:
                    print(f"Error processing mask: {str(e)}")
                    import traceback
                    traceback.print_exc()
            
            print(f"Final overlay size: {scaled_overlay.size}")
            
            # 8. 准备最终合成
            result = background.copy()
            result = result.convert('RGBA')
            
            # 9. 计算粘贴位置并合成主图
            paste_x = (background.width - scaled_overlay.width) // 2 + offset_x
            paste_y = (background.height - scaled_overlay.height) // 2 + offset_y
            
            temp = Image.new('RGBA', result.size, (0, 0, 0, 0))
            temp.paste(scaled_overlay, (paste_x, paste_y), scaled_overlay)
            result = Image.alpha_composite(result, temp)
            
            # 10. 添加水印（如果有）
            if watermark is not None:
                try:
                    watermark_img = tensor_to_image(watermark[0])
                    watermark_img = watermark_img.convert('RGBA')
                    watermark_img = watermark_img.resize(
                        (background.width, background.height),
                        get_sampler_by_name(method)
                    )
                    result = Image.alpha_composite(result, watermark_img)
                except Exception as e:
                    print(f"Error processing watermark: {str(e)}")
            
            # 11. 最终转换
            result = result.convert('RGB')
            tensor = image_to_tensor(result)
            tensor = tensor.unsqueeze(0)
            tensor = tensor.permute(0, 2, 3, 1)
            
            print("Mockup creation completed successfully")
            return (tensor,)
            
        except Exception as e:
            print(f"Error in create_mockup: {str(e)}")
            import traceback
            traceback.print_exc()
            return (overlay_image,)

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
    "AD_mockup-maker": AD_MockupMaker,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "AD_mockup-maker": "AD Mockup Maker",
} 