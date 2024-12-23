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
        }

    RETURN_TYPES = ("IMAGE", "INT", "INT")
    RETURN_NAMES = ("image", "current_index", "total_images")
    FUNCTION = "index_image"
    CATEGORY = "🌻 Addoor/Util"
    INPUT_IS_LIST = True

    def index_image(self, images, increment, seed):
        if not isinstance(images, list):
            images = [images]
        
        # Ensure increment is an integer, even if it's passed as a list
        increment = int(increment[0] if isinstance(increment, list) else increment)
        # Ensure seed is an integer, even if it's passed as a list
        seed = int(seed[0] if isinstance(seed, list) else seed)

        total_images = len(images)
        

        if self.current_index is None:
            if increment == 0:
                # Random starting point
                random.seed(seed)
                self.current_index = random.randint(0, total_images - 1)
            else:
                # Start from the beginning
                self.current_index = 0

        if increment == 0:
            # Random selection using seed
            random.seed(seed)
            selected_index = random.randint(0, total_images - 1)
        else:
            # Sequential selection based on increment
            selected_index = self.current_index
            self.current_index = (self.current_index + increment) % total_images

        selected_image = images[selected_index]
        return (selected_image, selected_index, total_images)

N_CLASS_MAPPINGS = {
    "AD_ImageIndexer": AD_ImageIndexer,
}

N_DISPLAY_NAME_MAPPINGS = {
    "AD_ImageIndexer": "🌻 Image Indexer",
}

