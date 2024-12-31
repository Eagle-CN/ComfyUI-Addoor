import os
import json
import numpy as np
from PIL import Image
from PIL.PngImagePlugin import PngInfo
import subprocess
import folder_paths

class AD_ImageSaver:
    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()
        self.compression = 4
        self.type = "output"
        self.prefix_append = ""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "folder": ("STRING", {"default": ""}),
                "filename_prefix": ("STRING", {"default": "ComfyUI"}),
                "overwrite_warning": ("BOOLEAN", {"default": False}),
                "include_metadata": ("BOOLEAN", {"default": True}),
                "extension": (["png", "jpg"],),
                "quality": ("INT", {"default": 95, "min": 0, "max": 100}),
                "open_output_directory": ("BOOLEAN", {"default": False}),
            },
            "optional": {
                "filename_opt": ("STRING", {"forceInput": True}),
            },
            "hidden": {"prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO"},
        }

    RETURN_TYPES = ()
    FUNCTION = "save_images"
    OUTPUT_NODE = True
    CATEGORY = "🌻 Addoor/Image"

    def save_images(self, images, folder, filename_prefix, overwrite_warning, include_metadata, 
                   extension, quality, open_output_directory, filename_opt=None, prompt=None, extra_pnginfo=None):
        try:
            # 处理保存路径
            if folder:
                # 如果提供了文件夹路径，从 ComfyUI 根目录开始
                comfy_path = os.path.dirname(self.output_dir)  # 获取 ComfyUI 根目录
                full_output_folder = os.path.join(comfy_path, folder)
            else:
                # 如果没有提供，使用默认输出目录
                full_output_folder = self.output_dir

            os.makedirs(full_output_folder, exist_ok=True)
            results = list()

            for batch_number, image in enumerate(images):
                i = 255. * image.cpu().numpy()
                img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
                metadata = None

                if not filename_opt:
                    filename_with_batch_num = filename_prefix.replace("%batch_num%", str(batch_number))
                    counter = 1

                    if os.path.exists(full_output_folder) and os.listdir(full_output_folder):
                        filtered_filenames = list(filter(
                            lambda filename: filename.startswith(filename_with_batch_num + "_")
                            and filename[len(filename_with_batch_num) + 1:-4].isdigit(),
                            os.listdir(full_output_folder)
                        ))

                        if filtered_filenames:
                            max_counter = max(
                                int(filename[len(filename_with_batch_num) + 1:-4])
                                for filename in filtered_filenames
                            )
                            counter = max_counter + 1

                    file = f"{filename_with_batch_num}_{counter:05}.{extension}"
                else:
                    if len(images) == 1:
                        file = f"{filename_opt}.{extension}"
                    else:
                        raise Exception("Multiple images and filename detected: Images will overwrite themselves!")

                save_path = os.path.join(full_output_folder, file)

                if os.path.exists(save_path) and overwrite_warning:
                    raise Exception("Filename already exists.")
                else:
                    if extension == "png":
                        if include_metadata:
                            metadata = PngInfo()
                            if prompt is not None:
                                metadata.add_text("prompt", json.dumps(prompt))
                            if extra_pnginfo is not None:
                                for x in extra_pnginfo:
                                    metadata.add_text(x, json.dumps(extra_pnginfo[x]))
                        img.save(save_path, pnginfo=metadata, compress_level=self.compression)
                    else:  # jpg
                        if include_metadata:
                            metadata = {}
                            if prompt is not None:
                                metadata["prompt"] = prompt
                            if extra_pnginfo is not None:
                                for key, value in extra_pnginfo.items():
                                    metadata[key] = value
                                metadata_json = json.dumps(metadata)
                                img.info["comment"] = metadata_json
                        img.save(save_path, quality=quality)

                # 计算相对路径用于预览
                subfolder = os.path.relpath(full_output_folder, self.output_dir) if folder else ""
                results.append({
                    "filename": file,
                    "subfolder": subfolder,
                    "type": self.type
                })

            if open_output_directory:
                self.open_directory(full_output_folder)

            return {"ui": {"images": results}}

        except Exception as e:
            print(f"Error saving images: {e}")
            return {"ui": {"images": []}}

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

