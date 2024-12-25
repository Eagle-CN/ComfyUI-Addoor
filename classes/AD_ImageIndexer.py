import random

class AD_ImageIndexer:
    def __init__(self):
        self.current_index = 0

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "increment": ("INT", {"default": 1, "min": 0, "max": 1000, "step": 1}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
            },
            "optional": {
                "images_name": ("STRING", {"forceInput": True}),
            }
        }

    RETURN_TYPES = ("IMAGE", "STRING", "INT", "INT")
    RETURN_NAMES = ("image", "image_name", "current_index", "total_items")
    FUNCTION = "index_item"
    CATEGORY = "🌻 Addoor/Batch"
    INPUT_IS_LIST = True

    def index_item(self, images, increment, seed, images_name=None):
        if not isinstance(images, list):
            images = [images]
        
        total_images = len(images)
        
        # Ensure increment and seed are integers
        increment = int(increment[0] if isinstance(increment, list) else increment)
        seed = int(seed[0] if isinstance(seed, list) else seed)

        # Initialize or update current_index
        if self.current_index is None or self.current_index >= total_images:
            if increment == 0:
                random.seed(seed)
                self.current_index = random.randint(0, total_images - 1)
            else:
                self.current_index = 0

        # Select an image
        if increment == 0:
            random.seed(seed)
            selected_index = random.randint(0, total_images - 1)
        else:
            selected_index = self.current_index
            self.current_index = (self.current_index + increment) % total_images

        selected_image = images[selected_index]

        # Handle image_name
        if images_name is not None and isinstance(images_name, list) and len(images_name) > selected_index:
            image_name = images_name[selected_index]
        else:
            image_name = ""

        return (selected_image, image_name, selected_index, total_images)

