import os
import torch
import numpy as np
from PIL import Image
import csv

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
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff})
            }
        }

    RETURN_TYPES = ("STRING", "IMAGE", "STRING", "STRING", "STRING", "STRING", "INT", "STRING")
    RETURN_NAMES = ("Directory_Output", "Image_List", "Text_List", "File_Path_List", "File_Name_List", "File_Name_With_Extension_List", "Total_Files", "Merged_Text")
    FUNCTION = "process_files"
    OUTPUT_NODE = True
    OUTPUT_IS_LIST = (False, True, True, True, True, True, False, False)
    CATEGORY = "🌻 Addoor/Batch"

    def process_files(self, Directory, Load_Cap, Skip_Frame, Filter_By, Extension, Deep_Search, seed):
        file_extensions = {
            "images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"],
            "text": [".txt", ".csv", ".md", ".json"],
        }
        
        file_paths = []
        if Deep_Search:
            for root, _, files in os.walk(Directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    file_extension = os.path.splitext(file)[1].lower()
                    if (Filter_By == "*" or file_extension in file_extensions.get(Filter_By, [])) and \
                       (Extension == "*" or file.lower().endswith(Extension.lower())):
                        file_paths.append(file_path)
        else:
            for file in os.listdir(Directory):
                file_path = os.path.join(Directory, file)
                if os.path.isfile(file_path):
                    file_extension = os.path.splitext(file)[1].lower()
                    if (Filter_By == "*" or file_extension in file_extensions.get(Filter_By, [])) and \
                       (Extension == "*" or file.lower().endswith(Extension.lower())):
                        file_paths.append(file_path)
        
        file_paths = sorted(file_paths)[Skip_Frame:Skip_Frame + Load_Cap]
        
        image_list = []
        text_list = []
        file_name_list = []
        file_name_with_extension_list = []
        merged_text = ""
        
        for file_path in file_paths:
            file_extension = os.path.splitext(file_path)[1].lower()
            if file_extension in file_extensions["images"]:
                try:
                    img = Image.open(file_path).convert("RGB")
                    image = torch.from_numpy(np.array(img).astype(np.float32) / 255.0).unsqueeze(0)
                    image_list.append(image)
                except Exception as e:
                    print(f"Error loading image '{file_path}': {e}")
            elif file_extension in file_extensions["text"]:
                try:
                    if file_extension == '.csv':
                        with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
                            content = '\n'.join([','.join(row) for row in csv.reader(csvfile)])
                    else:
                        with open(file_path, 'r', encoding='utf-8') as txtfile:
                            content = txtfile.read()
                    text_list.append(content)
                    merged_text += content + "\n\n"
                except Exception as e:
                    print(f"Error reading file '{file_path}': {e}")
            
            file_name_list.append(os.path.splitext(os.path.basename(file_path))[0])
            file_name_with_extension_list.append(os.path.basename(file_path))
        
        total_files = len(file_paths)
        return (Directory, image_list, text_list, file_paths, file_name_list, file_name_with_extension_list, total_files, merged_text.strip())

