import random

class AD_ImageIndexer:
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
                "index": ("INT", {
                    "default": 0, 
                    "min": 0, 
                    "max": 0xffffffffffffffff, 
                    "forceInput": True,
                    "tooltip": "Start from this row (0 or 1 for first image)"
                }),
            }
        }

    RETURN_TYPES = ("IMAGE", "INT", "INT")
    RETURN_NAMES = ("image", "current_index", "total_images")
    FUNCTION = "index_image"
    CATEGORY = "🌻 Addoor/Batch"
    INPUT_IS_LIST = True

    def index_image(self, images, increment, seed, index=None):
        if not isinstance(images, list):
            images = [images]
        
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
        return (selected_image, selected_index, total_images)

