import os
import torch
import numpy as np
from PIL import Image

def get_image_files(directory):
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp']
    file_paths = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if any(file.lower().endswith(ext) for ext in image_extensions):
                file_paths.append(os.path.join(root, file))
    return sorted(file_paths)

def extract_file_names(file_paths, skip, load):
    start_index = skip
    end_index = skip + load
    subset_file_paths = file_paths[start_index:end_index]
    return [os.path.splitext(os.path.basename(path))[0] for path in subset_file_paths]

def extract_file_paths(file_paths, skip, load):
    start_index = skip
    end_index = skip + load
    return file_paths[start_index:end_index]

def pilToImage(image):
    return torch.from_numpy(np.array(image).astype(np.float32) / 255.0).unsqueeze(0)

def load_image(image_path):
    try:
        img = Image.open(image_path)
        image = img.convert("RGB")
        loaded_image = pilToImage(image)
        return loaded_image
    except Exception as e:
        print(f"加载图片 '{image_path}' 时出错: {e}")
        return None

class AD_BatchImageLoadFromDir:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "Directory": ("STRING", {"default": ""}),
                "Load_Cap": ("INT", {"default": 100, "min": 1, "max": 1000}),
                "Skip_Frame": ("INT", {"default": 0, "min": 0, "max": 100})
            }
        }

    RETURN_TYPES = ("IMAGE", "STRING", "STRING", "STRING", "INT")
    RETURN_NAMES = ("Images", "Image_Paths", "Image_Names_suffix", "Image_Names", "Count")
    FUNCTION = "load_images"
    OUTPUT_NODE = True
    OUTPUT_IS_LIST = (True, True, True, True, False)
    CATEGORY = "Addoor"

    def load_images(self, Directory, Load_Cap, Skip_Frame):
        file_paths = get_image_files(Directory)
        
        if not file_paths:
            return ([], [], [], [], 0)
        
        valid_file_paths = extract_file_paths(file_paths, Skip_Frame, Load_Cap)
        images = []
        for file_path in valid_file_paths:
            image = load_image(file_path)
            if image is not None:
                images.append(image)
        
        image_names_suffix = [os.path.basename(path) for path in valid_file_paths]
        image_names = extract_file_names(file_paths, Skip_Frame, Load_Cap)
        count = len(images)
        
        return (images, valid_file_paths, image_names_suffix, image_names, count)

N_CLASS_MAPPINGS = {
    "AD_BatchImageLoadFromDir": AD_BatchImageLoadFromDir,
}

N_DISPLAY_NAME_MAPPINGS = {
    "AD_BatchImageLoadFromDir": "AD Batch Image Load From Directory",  # 从目录批量加载图片
}

