import os
import json
import torch
import numpy as np
from PIL import Image, ExifTags
import folder_paths
from nodes import PreviewImage
import mimetypes
import wave

class EnhancedPreview:
    def __init__(self):
        self.supported_image_formats = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp'}
        self.supported_audio_formats = {'.wav', '.mp3'}
        self.supported_text_formats = {'.txt', '.json', '.yaml', '.yml', '.md'}

    def get_file_metadata(self, file_path):
        metadata = {
            "filename": os.path.basename(file_path),
            "size": os.path.getsize(file_path),
            "mime_type": mimetypes.guess_type(file_path)[0],
            "last_modified": os.path.getmtime(file_path)
        }
        return metadata

    def preview_image(self, file_path, metadata):
        image = Image.open(file_path)
        metadata.update({
            "width": image.width,
            "height": image.height,
            "format": image.format,
            "mode": image.mode,
        })
        try:
            exif = image._getexif()
            if exif:
                metadata["exif"] = {
                    ExifTags.TAGS.get(tag_id, tag_id): str(value)
                    for tag_id, value in exif.items()
                }
        except:
            pass
        return metadata

    def preview_audio(self, file_path, metadata):
        if file_path.lower().endswith('.wav'):
            with wave.open(file_path, 'rb') as wav_file:
                metadata.update({
                    "channels": wav_file.getnchannels(),
                    "sample_width": wav_file.getsampwidth(),
                    "frame_rate": wav_file.getframerate(),
                    "n_frames": wav_file.getnframes(),
                })
        return metadata

    def preview_text(self, file_path, metadata):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        metadata.update({
            "preview_length": len(content),
            "preview_lines": len(content.splitlines()),
            "content": content
        })
        return metadata, content

class RunningHubFilePreviewerNode:
    def __init__(self):
        self.output_dir = folder_paths.get_temp_directory()
        self.type = "temp"
        self.enhanced_preview = EnhancedPreview()

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "file_path": ("STRING", {"default": "", "multiline": False}),
            },
            "hidden": {
                "unique_id": "UNIQUE_ID",
                "extra_pnginfo": "EXTRA_PNGINFO",
            },
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "preview_file"
    CATEGORY = "🌻 Addoor/RHAPI"
    OUTPUT_NODE = True

    def preview_file(self, file_path, unique_id=None, extra_pnginfo=None):
        if not os.path.isfile(file_path):
            return {"ui": {"text": [f"File not found: {file_path}"]}, "result": (f"File not found: {file_path}",)}

        try:
            metadata = self.enhanced_preview.get_file_metadata(file_path)
            file_ext = os.path.splitext(file_path)[1].lower()

            if file_ext in self.enhanced_preview.supported_image_formats:
                return self.handle_image(file_path, metadata)
            elif file_ext in self.enhanced_preview.supported_audio_formats:
                return self.handle_audio(file_path, metadata)
            elif file_ext in self.enhanced_preview.supported_text_formats:
                return self.handle_text(file_path, metadata, unique_id, extra_pnginfo)
            else:
                return self.handle_unsupported(metadata)

        except Exception as e:
            error_message = f"Error processing file: {str(e)}"
            return {"ui": {"text": [error_message]}, "result": (error_message,)}

    def handle_image(self, file_path, metadata):
        image = Image.open(file_path)
        image = image.convert('RGB')
        image_np = np.array(image).astype(np.float32) / 255.0
        image_tensor = torch.from_numpy(image_np)[None,]

        preview = PreviewImage()
        saved = preview.save_images(image_tensor, "runninghub/preview", None, None)

        metadata = self.enhanced_preview.preview_image(file_path, metadata)
        
        return {
            "ui": {
                "images": saved["ui"]["images"],
                "text": [f"Image Preview:\n{json.dumps(metadata, indent=2)}"]
            },
            "result": (json.dumps(metadata),)
        }

    def handle_audio(self, file_path, metadata):
        metadata = self.enhanced_preview.preview_audio(file_path, metadata)
        return {
            "ui": {"text": [f"Audio Preview:\n{json.dumps(metadata, indent=2)}"]},
            "result": (json.dumps(metadata),)
        }

    def handle_text(self, file_path, metadata, unique_id, extra_pnginfo):
        metadata, content = self.enhanced_preview.preview_text(file_path, metadata)
        
        if unique_id is not None and extra_pnginfo is not None:
            if isinstance(extra_pnginfo, list) and isinstance(extra_pnginfo[0], dict) and "workflow" in extra_pnginfo[0]:
                workflow = extra_pnginfo[0]["workflow"]
                node = next((x for x in workflow["nodes"] if str(x["id"]) == str(unique_id[0])), None)
                if node:
                    node["widgets_values"] = [content]

        return {
            "ui": {"text": [f"Text Preview:\n{json.dumps(metadata, indent=2)}\n\nContent:\n{content[:1000]}..."]},
            "result": (content,)
        }

    def handle_unsupported(self, metadata):
        return {
            "ui": {"text": [f"Unsupported file type. Metadata:\n{json.dumps(metadata, indent=2)}"]},
            "result": (json.dumps(metadata),)
        }

