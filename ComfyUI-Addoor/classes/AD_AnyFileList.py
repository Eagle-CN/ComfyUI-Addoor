import os
import torch
import numpy as np
from PIL import Image
import csv

FILE_EXTENSIONS = {
    "images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"],
    "text": [".txt", ".csv", ".md", ".json"],
    # Add more categories as needed
}

def get_files(directory, filter_by="*", extension="*", deep_search=False):
    file_paths = []
    
    if deep_search:
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                file_extension = os.path.splitext(file)[1].lower()
                if (filter_by == "*" or file_extension in FILE_EXTENSIONS.get(filter_by, [])) and \
                   (extension == "*" or file.lower().endswith(extension.lower())):
                    file_paths.append(file_path)
    else:
        for file in os.listdir(directory):
            file_path = os.path.join(directory, file)
            if os.path.isfile(file_path):
                file_extension = os.path.splitext(file)[1].lower()
                if (filter_by == "*" or file_extension in FILE_EXTENSIONS.get(filter_by, [])) and \
                   (extension == "*" or file.lower().endswith(extension.lower())):
                    file_paths.append(file_path)
    
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
        print(f"Error loading image '{image_path}': {e}")
        return None

def read_text_file(file_path):
    try:
        if file_path.lower().endswith('.csv'):
            with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                return '\n'.join([','.join(row) for row in reader])
        else:
            with open(file_path, 'r', encoding='utf-8') as txtfile:
                return txtfile.read()
    except Exception as e:
        print(f"Error reading file '{file_path}': {e}")
        return None

class AD_AnyFileList:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "Directory": ("STRING", {"default": ""}),
                "Load_Cap": ("INT", {"default": 100, "min": 1, "max": 1000}),
                "Skip_Frame": ("INT", {"default": 0, "min": 0, "max": 100}),
                "Filter_By": (["*", "images", "text"],),
                "Extension": ("STRING", {"default": "*"}),
                "Deep_Search": ("BOOLEAN", {"default": False}),
            }
        }

    RETURN_TYPES = ("STRING", "IMAGE", "STRING", "STRING", "STRING", "STRING", "INT", "STRING")
    RETURN_NAMES = ("Directory_Output", "Image_List", "Text_List", "File_Path_List", "File_Name_List", "File_Name_With_Extension_List", "Total_Files", "Merged_Text")
    FUNCTION = "process_files"
    OUTPUT_NODE = True
    OUTPUT_IS_LIST = (False, True, True, True, True, True, False, False)
    CATEGORY = "Addoor"

    def process_files(self, Directory, Load_Cap, Skip_Frame, Filter_By, Extension, Deep_Search):
        file_paths = get_files(Directory, Filter_By, Extension, Deep_Search)
        
        if not file_paths:
            return (Directory, [], [], [], [], [], 0, "")
        
        valid_file_paths = extract_file_paths(file_paths, Skip_Frame, Load_Cap)
        image_list = []
        text_list = []
        merged_text = ""
        
        for file_path in valid_file_paths:
            if file_path.lower().endswith(tuple(FILE_EXTENSIONS["images"])):
                image = load_image(file_path)
                if image is not None:
                    image_list.append(image)
            elif file_path.lower().endswith(tuple(FILE_EXTENSIONS["text"])):
                content = read_text_file(file_path)
                if content is not None:
                    text_list.append(content)
                    merged_text += content + "\n\n"
        
        file_name_with_extension_list = [os.path.basename(path) for path in valid_file_paths]
        file_name_list = extract_file_names(file_paths, Skip_Frame, Load_Cap)
        total_files = len(valid_file_paths)
        
        return (Directory, image_list, text_list, valid_file_paths, file_name_list, file_name_with_extension_list, total_files, merged_text.strip())

N_CLASS_MAPPINGS = {
    "AD_AnyFileList": AD_AnyFileList,
}

N_DISPLAY_NAME_MAPPINGS = {
    "AD_AnyFileList": "AD Any File List",  # 任意文件列表
}

