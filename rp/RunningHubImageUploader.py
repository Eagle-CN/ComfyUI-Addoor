import requests
import torch
import numpy as np
from PIL import Image
from io import BytesIO
import logging
from . import validate_api_key, BASE_URL

logger = logging.getLogger(__name__)

class RunningHubImageUploaderNode:
    """Node for uploading images to RunningHub"""
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "api_key": ("STRING", {"default": ""}),
                "image": ("IMAGE",),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("filename",)
    FUNCTION = "upload_image"
    CATEGORY = "🌻 Addoor/RHAPI"
    
    def upload_image(self, api_key: str, image: torch.Tensor) -> tuple:
        """
        上传图片到RunningHub服务器

        参数:
            api_key (str): API密钥
            image (torch.Tensor): 输入图像张量

        返回:
            tuple: 包含上传后返回的文件名
        """
        try:
            # 验证API密钥
            if not validate_api_key(api_key):
                raise ValueError("Invalid API key")

            # 检查输入的图像类型
            if not isinstance(image, torch.Tensor):
                raise TypeError(f"Expected image to be a torch.Tensor, but got {type(image)}")
            
            # 将图像张量转换为NumPy数组
            image_np = image.detach().cpu().numpy()
            
            # 处理图像形状
            if image_np.ndim == 4:
                image_np = image_np[0]  # 取第一张图片
                
            if image_np.ndim == 3:
                if image_np.shape[0] in [1, 3, 4]:  # [C, H, W]
                    image_np = np.transpose(image_np, (1, 2, 0))
                elif image_np.shape[2] not in [1, 3, 4]:
                    raise ValueError(f"Unsupported number of channels: {image_np.shape[2]}")
            
            # 确定图像模式
            if image_np.shape[2] == 1:
                mode = "L"
                image_pil = Image.fromarray((image_np.squeeze(-1) * 255).astype(np.uint8), mode)
            elif image_np.shape[2] == 3:
                mode = "RGB"
                image_pil = Image.fromarray((image_np * 255).astype(np.uint8), mode)
            elif image_np.shape[2] == 4:
                mode = "RGBA"
                image_pil = Image.fromarray((image_np * 255).astype(np.uint8), mode)
            else:
                raise ValueError(f"Unsupported number of channels: {image_np.shape[2]}")

            # 将图像保存到BytesIO
            buffer = BytesIO()
            image_pil.save(buffer, format='PNG')
            buffer.seek(0)

            # 检查文件大小
            if buffer.getbuffer().nbytes > 10 * 1024 * 1024:  # 10MB
                raise ValueError("Image size exceeds 10MB limit")

            # 准备上传请求
            upload_url = f"{BASE_URL}/task/openapi/upload"
            files = {
                'file': ('image.png', buffer, 'image/png')
            }
            data = {
                'apiKey': api_key,
                'fileType': 'image',
            }
            headers = {
                "Accept": "*/*",
                "User-Agent": "ComfyUI-RHAPI/1.0",
            }

            # 发送上传请求
            logger.info(f"Uploading image to {upload_url}")
            response = requests.post(upload_url, data=data, files=files, headers=headers)
            response.raise_for_status()

            # 解析响应
            result = response.json()
            if result.get('code') != 0:
                raise Exception(f"Upload failed: {result.get('msg')}")

            filename = result.get('data', {}).get('fileName')
            if not filename:
                raise Exception("Upload succeeded but filename not found in response")

            logger.info(f"Image uploaded successfully. Filename: {filename}")
            return (filename,)

        except Exception as e:
            logger.error(f"Image upload failed: {str(e)}")
            raise 