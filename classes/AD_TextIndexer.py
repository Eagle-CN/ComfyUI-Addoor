class AD_TextIndexer:
    def __init__(self):
        self.current_index = None

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "texts": ("STRING", {"forceInput": True}),  # 改为文本列表输入
                "increment": ("INT", {"default": 1, "min": 0, "max": 1000, "step": 1}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
            },
            "optional": {
                "index": ("INT", {
                    "default": 0, 
                    "min": 0, 
                    "max": 0xffffffffffffffff, 
                    "forceInput": True,
                    "tooltip": "Start from this row (0 or 1 for first text)"
                }),
            }
        }

    RETURN_TYPES = ("STRING", "INT", "INT")
    RETURN_NAMES = ("text", "current_index", "total_texts")
    FUNCTION = "index_text"
    CATEGORY = "🌻 Addoor/Batch"
    INPUT_IS_LIST = True  # 表示输入是列表

    def index_text(self, texts, increment, seed, index=None):
        if not isinstance(texts, list):
            texts = [texts]
        
        # 确保increment和seed是整数
        increment = int(increment[0] if isinstance(increment, list) else increment)
        seed = int(seed[0] if isinstance(seed, list) else seed)
        # 确保index是整数
        if index is not None:
            index = int(index[0] if isinstance(index, list) else index)

        total_texts = len(texts)

        # 处理index输入
        if index is not None:
            # 调整索引以从0开始内部计数，但将0和1都视为第一个文本
            adjusted_index = max(0, index - 1)
            self.current_index = adjusted_index % total_texts
        elif self.current_index is None:
            if increment == 0:
                # 随机起点
                import random
                random.seed(seed)
                self.current_index = random.randint(0, total_texts - 1)
            else:
                # 从头开始
                self.current_index = 0

        if increment == 0:
            # 使用种子进行随机选择
            import random
            random.seed(seed)
            selected_index = random.randint(0, total_texts - 1)
        else:
            # 基于增量的顺序选择
            selected_index = self.current_index
            self.current_index = (self.current_index + increment) % total_texts

        selected_text = texts[selected_index]
        return (selected_text, selected_index, total_texts) 