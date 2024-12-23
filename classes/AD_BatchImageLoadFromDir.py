import os
import torch
import numpy as np
from PIL import Image

class AD_BatchImageLoadFromDir:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "Directory": ("STRING", {"default": ""}),
                "Load_Cap": ("INT", {"default": 100, "min": 1, "max": 1000}),
                "Skip_Frame": ("INT", {"default": 0, "min": 0, "max": 100}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff})
            }
        }

    RETURN_TYPES = ("IMAGE", "STRING", "STRING", "STRING", "INT")
    RETURN_NAMES = ("Images", "Image_Paths", "Image_Names_suffix", "Image_Names", "Count")
    FUNCTION = "load_images"
    OUTPUT_NODE = True
    OUTPUT_IS_LIST = (True, True, True, True, False)
    CATEGORY = "🌻 Addoor/Batch Operation"

    def load_images(self, Directory, Load_Cap, Skip_Frame):
        image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp']
        file_paths = []
        for root, dirs, files in os.walk(Directory):
            for file in files:
                if any(file.lower().endswith(ext) for ext in image_extensions):
                    file_paths.append(os.path.join(root, file))
        file_paths = sorted(file_paths)[Skip_Frame:Skip_Frame + Load_Cap]
        
        images = []
        image_paths = []
        image_names_suffix = []
        image_names = []
        
        for file_path in file_paths:
            try:
                img = Image.open(file_path).convert("RGB")
                image = torch.from_numpy(np.array(img).astype(np.float32) / 255.0).unsqueeze(0)
                images.append(image)
                image_paths.append(file_path)
                image_names_suffix.append(os.path.basename(file_path))
                image_names.append(os.path.splitext(os.path.basename(file_path))[0])
            except Exception as e:
                print(f"Error loading image '{file_path}': {e}")
        
        count = len(images)
        return (images, image_paths, image_names_suffix, image_names, count)

N_CLASS_MAPPINGS = {
    "AD_BatchImageLoadFromDir": AD_BatchImageLoadFromDir,
}

N_DISPLAY_NAME_MAPPINGS = {
    "AD_BatchImageLoadFromDir": "🌻 Batch Image Load From Directory",
}

