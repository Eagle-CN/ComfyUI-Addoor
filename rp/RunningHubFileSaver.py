import os
import requests
import json
import numpy as np
from PIL import Image
from PIL.PngImagePlugin import PngInfo
import subprocess
import mimetypes
import torch
import logging
import io
import re

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class RunningHubFileSaverNode:
    def __init__(self):
        self.compression = 4

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "file_url": ("STRING", {"default": ""}),
                "directory": ("STRING", {"default": "outputs"}),
                "filename_prefix": ("STRING", {"default": "RH_Output"}),
                "filename_delimiter": ("STRING", {"default": "_"}),
                "filename_number_padding": ("INT", {"default": 4, "min": 0, "max": 9, "step": 1}),
                "file_extension": (["auto", "png", "jpg", "jpeg", "txt", "json", "mp4"], {"default": "auto"}),
                "open_output_directory": ("BOOLEAN", {"default": False}),
            },
        }

    RETURN_TYPES = ("STRING", "IMAGE", "STRING")
    RETURN_NAMES = ("output_path", "preview", "file_type")
    FUNCTION = "save_file"
    CATEGORY = "🌻 Addoor/RHAPI"

    def save_file(self, file_url, directory, filename_prefix, filename_delimiter, filename_number_padding, file_extension, open_output_directory):
        try:
            logger.info(f"Attempting to save file from URL: {file_url}")
            
            if not file_url:
                raise ValueError("File URL is empty")

            if not os.path.exists(directory):
                logger.info(f"Creating directory: {directory}")
                os.makedirs(directory)

            response = requests.get(file_url, timeout=30)
            response.raise_for_status()

            content_type = response.headers.get('content-type')
            logger.info(f"Content-Type: {content_type}")

            if file_extension == "auto":
                file_extension = mimetypes.guess_extension(content_type)
                if file_extension:
                    file_extension = file_extension[1:]  # Remove the leading dot
                    if file_extension == "jpeg":
                        file_extension = "jpg"
                else:
                    file_extension = "bin"  # Default to binary if can't guess
                logger.info(f"Auto-detected file extension: {file_extension}")

            file_path = os.path.join(directory, self.generate_filename(directory, filename_prefix, filename_delimiter, filename_number_padding, file_extension))
            logger.info(f"Saving file to: {file_path}")

            preview = None
            if file_extension in ['png', 'jpg', 'jpeg']:
                try:
                    img_data = io.BytesIO(response.content)
                    img = Image.open(img_data)  # Reopen the image after verifying
                    metadata = PngInfo()
                    metadata.add_text("source_url", file_url)
                    img.save(file_path, pnginfo=metadata, compress_level=self.compression)
                    preview = torch.from_numpy(np.array(img).astype(np.float32) / 255.0).unsqueeze(0)
                except Exception as e:
                    logger.error(f"Error processing image: {str(e)}")
                    # If image processing fails, save as binary
                    with open(file_path, 'wb') as f:
                        f.write(response.content)
                    preview = torch.zeros((1, 1, 1, 3))  # Placeholder for failed image
            elif file_extension in ['txt', 'json']:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(response.text)
                preview = torch.zeros((1, 1, 1, 3))  # Placeholder for non-image files
            else:
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                preview = torch.zeros((1, 1, 1, 3))  # Placeholder for other file types

            logger.info(f"File saved successfully to {file_path}")

            if open_output_directory:
                self.open_directory(directory)

            return (file_path, preview, file_extension)

        except requests.exceptions.RequestException as e:
            logger.error(f"Error downloading file: {str(e)}")
        except IOError as e:
            logger.error(f"Error saving file: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")

        return ("", torch.zeros((1, 1, 1, 3)), "")

    def generate_filename(self, directory, prefix, delimiter, number_padding, extension):
        if number_padding == 0:
            return f"{prefix}.{extension}"

        pattern = f"{re.escape(prefix)}{re.escape(delimiter)}(\\d{{{number_padding}}})"
        existing_files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        existing_counters = [
            int(re.search(pattern, filename).group(1))
            for filename in existing_files
            if re.match(pattern, filename)
        ]

        counter = max(existing_counters, default=0) + 1
        return f"{prefix}{delimiter}{counter:0{number_padding}}.{extension}"

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
                    logger.error(f"Could not open directory: {path}")

