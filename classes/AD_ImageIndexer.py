import random
import os

class AD_ImageIndexer:
    # 定义需要忽略的系统文件
    IGNORED_FILES = {'.DS_Store', 'Thumbs.db', '.gitignore', 'desktop.ini'}
    
    def __init__(self):
        self.current_index = None

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "increment": ("INT", {"default": 1, "min": 0, "max": 1000, "step": 1}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
            },
            "optional": {
                "image_names": ("STRING", {"forceInput": True}),
                "index": ("INT", {
                    "default": 0, 
                    "min": 0, 
                    "max": 0xffffffffffffffff, 
                    "forceInput": True,
                    "tooltip": "Start from this row (0 or 1 for first image)"
                }),
            }
        }

    RETURN_TYPES = ("IMAGE", "STRING", "INT", "INT")
    RETURN_NAMES = ("image", "image_name", "current_index", "total_images")
    FUNCTION = "index_image"
    CATEGORY = "🌻 Addoor/Batch"
    INPUT_IS_LIST = True

    def filter_system_files(self, names):
        """过滤系统文件"""
        if names is None:
            return None
        return [name for name in names if os.path.basename(name) not in self.IGNORED_FILES]

    def index_image(self, images, increment, seed, image_names=None, index=None):
        if not isinstance(images, list):
            images = [images]
            
        # 过滤系统文件
        if image_names is not None:
            if not isinstance(image_names, list):
                image_names = [image_names]
            image_names = self.filter_system_files(image_names)
        
        # 确保increment和seed是整数
        increment = int(increment[0] if isinstance(increment, list) else increment)
        seed = int(seed[0] if isinstance(seed, list) else seed)
        # 确保index是整数
        if index is not None:
            index = int(index[0] if isinstance(index, list) else index)

        total_images = len(images)

        # 处理index输入
        if index is not None:
            # 调整索引以从0开始内部计数，但将0和1都视为第一张图
            adjusted_index = max(0, index - 1)
            self.current_index = adjusted_index % total_images
        elif self.current_index is None:
            if increment == 0:
                # 随机起点
                random.seed(seed)
                self.current_index = random.randint(0, total_images - 1)
            else:
                # 从头开始
                self.current_index = 0

        if increment == 0:
            # 使用种子进行随机选择
            random.seed(seed)
            selected_index = random.randint(0, total_images - 1)
        else:
            # 基于增量的顺序选择
            selected_index = self.current_index
            self.current_index = (self.current_index + increment) % total_images

        selected_image = images[selected_index]
        # 如果没有提供名称列表，使用索引作为名称
        selected_name = (image_names[selected_index] if image_names and selected_index < len(image_names) 
                        else f"image_{selected_index}")
        
        return (selected_image, selected_name, selected_index, total_images)

