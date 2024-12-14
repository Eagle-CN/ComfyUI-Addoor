import os
import json
import numpy as np
from PIL import Image
from PIL.PngImagePlugin import PngInfo
import subprocess

class AD_ImageSaver:
    def __init__(self):
        self.compression = 4

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Images": ("IMAGE",),
                "Directory": ("STRING", {"default": ""}),
                "Filename_Prefix": ("STRING", {"default": "Image"}),
                "Open_Output_Directory": ("BOOLEAN", {"default": False}),
            },
            "hidden": {"prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO"},
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("Output_Directory",)
    FUNCTION = "save_images"
    OUTPUT_NODE = True
    CATEGORY = "Addoor"

    def save_images(self, Images, Directory, Filename_Prefix, Open_Output_Directory, prompt=None, extra_pnginfo=None):
        try:
            os.makedirs(Directory, exist_ok=True)

            saved_paths = []
            for i, image in enumerate(Images):
                image = image.cpu().numpy()
                image = (image * 255).astype(np.uint8)
                img = Image.fromarray(image)

                metadata = PngInfo()
                if prompt is not None:
                    metadata.add_text("prompt", json.dumps(prompt))
                if extra_pnginfo is not None:
                    for x in extra_pnginfo:
                        metadata.add_text(x, json.dumps(extra_pnginfo[x]))

                file_path = self.get_next_file_path(Directory, Filename_Prefix)
                img.save(file_path, pnginfo=metadata, compress_level=self.compression)
                saved_paths.append(file_path)

            print(f"Saved {len(saved_paths)} images to {Directory}")

            if Open_Output_Directory:
                self.open_directory(Directory)

            return (Directory,)

        except Exception as e:
            print(f"Error saving images: {e}")
            return ("",)

    @staticmethod
    def get_next_file_path(directory, filename_prefix):
        index = 1
        while True:
            file_name = f"{filename_prefix}_{str(index).zfill(4)}.png"
            file_path = os.path.join(directory, file_name)
            if not os.path.exists(file_path):
                return file_path
            index += 1

    @staticmethod
    def open_directory(path):
        if os.name == 'nt':  # Windows
            os.startfile(path)
        elif os.name == 'posix':  # macOS and Linux
            try:
                subprocess.call(['open', path])  # macOS
            except:
                try:
                    subprocess.call(['xdg-open', path])  # Linux
                except:
                    print(f"Could not open directory: {path}")

N_CLASS_MAPPINGS = {
    "AD_ImageSaver": AD_ImageSaver,
}

N_DISPLAY_NAME_MAPPINGS = {
    "AD_ImageSaver": "🌻 Image Saver",
}

