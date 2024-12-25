import os
import hashlib
from PIL import Image, ImageSequence, ImageOps
import numpy as np
import torch
import folder_paths

class AD_LoadImageAdvanced:
    @classmethod
    def INPUT_TYPES(s):
        input_dir = folder_paths.get_input_directory()

        files = []
        for root, dirs, filenames in os.walk(input_dir):
            for filename in filenames:
                full_path = os.path.join(root, filename)
                relative_path = os.path.relpath(full_path, input_dir)
                relative_path = relative_path.replace("\\", "/")
                files.append(relative_path)

        return {"required":
                {"image": (sorted(files), {"image_upload": True}),
                 "strip_extension": ("BOOLEAN", {"default": True}),
                 "rgba": ("BOOLEAN", {"default": False})}
                }

    CATEGORY = "🌻 Addoor/Image"

    RETURN_TYPES = ("IMAGE", "MASK", "STRING")
    RETURN_NAMES = ("IMAGE", "MASK", "FILENAME")

    FUNCTION = "load_image"

    def load_image(self, image, strip_extension, rgba):
        image_path = folder_paths.get_annotated_filepath(image)
        img = Image.open(image_path)
        output_images = []
        output_masks = []
        for i in ImageSequence.Iterator(img):
            i = ImageOps.exif_transpose(i)
            if i.mode == 'I':
                i = i.point(lambda i: i * (1 / 255))
            if rgba:
                image = i.convert("RGBA")
                image = np.array(image).astype(np.float32) / 255.0
                image = torch.from_numpy(image)[None,]
            else:
                image = i.convert("RGB")
                image = np.array(image).astype(np.float32) / 255.0
                image = torch.from_numpy(image)[None,]
            if 'A' in i.getbands():
                mask = np.array(i.getchannel('A')).astype(np.float32) / 255.0
                mask = 1. - torch.from_numpy(mask)
            else:
                mask = torch.zeros((64, 64), dtype=torch.float32, device="cpu")
            output_images.append(image)
            output_masks.append(mask.unsqueeze(0))

        if len(output_images) > 1:
            output_image = torch.cat(output_images, dim=0)
            output_mask = torch.cat(output_masks, dim=0)
        else:
            output_image = output_images[0]
            output_mask = output_masks[0]

        if strip_extension:
            filename = os.path.splitext(image_path)[0]
        else:
            filename = os.path.basename(image_path)

        return (output_image, output_mask, filename,)

    @classmethod
    def IS_CHANGED(s, image, strip_extension, rgba):
        image_path = folder_paths.get_annotated_filepath(image)
        m = hashlib.sha256()
        with open(image_path, 'rb') as f:
            m.update(f.read())
        return m.digest().hex()

    @classmethod
    def VALIDATE_INPUTS(s, image, strip_extension, rgba):
        if not folder_paths.exists_annotated_filepath(image):
            return "Invalid image file: {}".format(image)

        return True

