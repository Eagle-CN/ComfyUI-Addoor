"""
@author: ComfyUI Addoor
@title: ComfyUI-PromptSaver
@description: Save prompts to CSV file with customizable naming pattern
@version: 1.0.0
"""

import os
import csv
import folder_paths
from typing import Dict, Any

class AD_PromptSaver:
    """Save prompts to CSV file with customizable naming pattern"""
    
    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()
    
    @classmethod
    def INPUT_TYPES(cls) -> Dict[str, Any]:
        return {
            "required": {
                "prompt": ("STRING", {"multiline": True}),
                "csv_filename": ("STRING", {"default": "prompts.csv"}),
                "folder": ("STRING", {"default": ""}),
                "filename_prefix": ("STRING", {"default": "Image"}),
                "filename_delimiter": ("STRING", {"default": "_"}),
                "filename_number_padding": ("INT", {"default": 4, "min": 0, "max": 9, "step": 1}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("status",)
    FUNCTION = "save_prompt"
    CATEGORY = "🌻 Addoor/prompt"

    def generate_entry_name(self, filename_prefix: str, filename_delimiter: str, folder: str, filename_number_padding: int) -> str:
        """Generate the entry name using the specified pattern"""
        if folder:
            # 如果提供了文件夹路径，从 ComfyUI 根目录开始
            comfy_path = os.path.dirname(self.output_dir)
            full_output_folder = os.path.join(comfy_path, folder)
        else:
            # 如果没有提供，使用默认输出目录
            full_output_folder = self.output_dir

        # 确保目录存在
        os.makedirs(full_output_folder, exist_ok=True)

        # 获取目录中现有的文件数量
        counter = 1
        pattern = f"{filename_prefix}{filename_delimiter}"
        existing_files = [f for f in os.listdir(full_output_folder) if f.startswith(pattern)]
        
        if existing_files:
            numbers = []
            for f in existing_files:
                try:
                    num = int(f[len(pattern):].split('.')[0])
                    numbers.append(num)
                except ValueError:
                    continue
            if numbers:
                counter = max(numbers) + 1
                
        # 使用指定的填充长度
        if filename_number_padding > 0:
            return f"{filename_prefix}{filename_delimiter}{counter:0{filename_number_padding}d}"
        else:
            return f"{filename_prefix}"

    def save_prompt(self, prompt: str, csv_filename: str, folder: str,
                   filename_prefix: str, filename_delimiter: str, filename_number_padding: int) -> tuple:
        """Save prompt to CSV file"""
        try:
            # 处理保存路径
            if folder:
                # 如果提供了文件夹路径，从 ComfyUI 根目录开始
                comfy_path = os.path.dirname(self.output_dir)
                full_output_folder = os.path.join(comfy_path, folder)
            else:
                # 如果没有提供，使用默认输出目录
                full_output_folder = self.output_dir
            
            os.makedirs(full_output_folder, exist_ok=True)
            
            # CSV文件完整路径
            csv_path = os.path.join(full_output_folder, csv_filename)
            
            # 生成条目名称
            entry_name = self.generate_entry_name(filename_prefix, filename_delimiter, folder, filename_number_padding)
            
            # 准备要写入的行
            new_row = [entry_name, prompt]
            
            # 检查文件是否存在并写入
            file_exists = os.path.exists(csv_path)
            
            mode = 'a' if file_exists else 'w'
            with open(csv_path, mode, newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                # 如果是新文件，写入标题行
                if not file_exists:
                    writer.writerow(['Name', 'Prompt'])
                writer.writerow(new_row)
            
            return (f"Successfully saved prompt for {entry_name}",)
            
        except Exception as e:
            return (f"Error saving prompt: {str(e)}",)

# 节点注册
NODE_CLASS_MAPPINGS = {
    "AD_prompt-saver": AD_PromptSaver
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "AD_prompt-saver": "AD Prompt Saver"
}