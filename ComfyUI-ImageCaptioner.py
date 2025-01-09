"""
@name: "ComfyUI ImageCaptioner"
@version: "1.1.1"
@author: "ComfyNodePRs"
@description: "Image captioning and text chat toolkit for ComfyUI using Qwen models"
"""

import os
import json
import base64
import numpy as np
import torch
from PIL import Image
from io import BytesIO

try:
    from openai import OpenAI
except ImportError:
    print("请先安装 openai: pip install openai")

# 添加常量配置
DEFAULT_MAX_TOKENS = 512
MAX_TOKENS_LIMIT = 1024

class ImageCaptioner:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "user_prompt": ("STRING", {"default": "请问有什么可以帮您？", "multiline": True}),
                "system_prompt": ("STRING", {
                    "default": "你是一位专业的 AI 助手，擅长图像分析和文字对话。在描述图片时，请注意细节并使用专业的术语；在对话时，保持友好和专业。",
                    "multiline": True
                }),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "dashscope_api_key": ("STRING", {"default": "", "multiline": False}),
            },
            "optional": {
                "image": ("IMAGE",),
                "max_tokens": ("INT", {
                    "default": DEFAULT_MAX_TOKENS,
                    "min": 1, 
                    "max": MAX_TOKENS_LIMIT,
                    "step": 1,
                    "display": "number"
                })
            }
        }
    
    RETURN_TYPES = ("STRING",)
    FUNCTION = "generate_response"
    CATEGORY = "🌻 Addoor/API"

    def post_process_prompt(self, response_data):
        try:
            if not response_data or not isinstance(response_data, dict):
                return "Error: Invalid response format"
            
            # 从返回的JSON中提取文本内容
            if 'choices' in response_data and len(response_data['choices']) > 0:
                message = response_data['choices'][0].get('message', {})
                content = message.get('content', '')
                if content:
                    return content.strip()
            
            return "Error: No valid content in response"
            
        except Exception as e:
            return f"Error processing response: {str(e)}"

    def create_text_completion(self, client, system_prompt, user_prompt, max_tokens=None):
        """纯文本对话请求"""
        # 确保 max_tokens 不超过限制
        max_tokens = min(max_tokens or DEFAULT_MAX_TOKENS, MAX_TOKENS_LIMIT)
        
        params = {
            "model": "qwen-plus",
            "messages": [
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': user_prompt}
            ],
            "max_tokens": max_tokens
        }
            
        completion = client.chat.completions.create(**params)
        return completion

    def create_image_completion(self, client, system_prompt, user_prompt, image_url, max_tokens=None):
        """图像描述请求"""
        # 确保 max_tokens 不超过限制
        max_tokens = min(max_tokens or DEFAULT_MAX_TOKENS, MAX_TOKENS_LIMIT)
        
        params = {
            "model": "qwen-vl-plus",
            "messages": [{
                "role": "user",
                "content": [
                    {"type": "text", "text": user_prompt},
                    {"type": "image_url", "image_url": {"url": image_url}}
                ]
            }],
            "max_tokens": max_tokens
        }
            
        completion = client.chat.completions.create(**params)
        return completion

    def generate_response(self, user_prompt, system_prompt, seed, dashscope_api_key, image=None, max_tokens=None):
        # seed 参数仅用于 ComfyUI 节点系统，不传递给 API
        try:
            # 初始化客户端
            client = OpenAI(
                api_key=dashscope_api_key,
                base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
            )
            
            # 判断是否有图片输入
            if image is not None:
                # 处理图片
                image_np = image[0].cpu().numpy()
                image_np = (image_np * 255).astype(np.uint8)
                image_pil = Image.fromarray(image_np)
                
                # 转换为base64
                with BytesIO() as output:
                    image_pil.save(output, format="PNG")
                    image_bytes = output.getvalue()
                base64_image = base64.b64encode(image_bytes).decode("utf-8")
                image_url = f"data:image/png;base64,{base64_image}"
                
                # 使用图像模式
                completion = self.create_image_completion(
                    client, system_prompt, user_prompt, image_url,
                    max_tokens=max_tokens
                )
            else:
                # 使用纯文本模式
                completion = self.create_text_completion(
                    client, system_prompt, user_prompt,
                    max_tokens=max_tokens
                )

            # 获取响应并转换为字典格式
            response_dict = json.loads(completion.model_dump_json())
            
            # 处理响应
            processed_response = self.post_process_prompt(response_dict)
            return (processed_response,)
                
        except Exception as e:
            return (f"Error: {str(e)}",)

NODE_CLASS_MAPPINGS = {
    "ImageCaptioner": ImageCaptioner
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ImageCaptioner": "AI Chat & Image Captioner"
}

