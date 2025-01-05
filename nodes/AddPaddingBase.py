"""
@author: ealkanat
@title: ComfyUI Easy Padding
@description: A simple custom node for creates padding for given image
@version: 1.0.2
@project: https://github.com/erkana/comfyui_easy_padding
@author: https://github.com/erkana
"""

import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
import numpy as np
import torch


class AddPaddingBase:
     def __init__(self):
        pass
     
     FUNCTION = "resize"
     CATEGORY = "🌻 Addoor/image"

     def add_padding(self, image, left, top, right, bottom, color="#ffffff", transparent=False):
            padded_images = []
            image = [self.tensor2pil(img) for img in image]
            for img in image:
                padded_image = Image.new("RGBA" if transparent else "RGB", 
                     (img.width + left + right, img.height + top + bottom), 
                     (0, 0, 0, 0) if transparent else self.hex_to_tuple(color))
                padded_image.paste(img, (left, top))
                padded_images.append(self.pil2tensor(padded_image))
            return torch.cat(padded_images, dim=0)
     
     def create_mask(self, image, left, top, right, bottom):
            masks = []
            image = [self.tensor2pil(img) for img in image]
            for img in image:
                shape = (left, top, img.width + left, img.height + top)
                mask_image = Image.new("L", (img.width + left + right, img.height + top + bottom), 255)
                draw = ImageDraw.Draw(mask_image)
                draw.rectangle(shape, fill=0)
                masks.append(self.pil2tensor(mask_image))
            return torch.cat(masks, dim=0)
     
     def hex_to_float(self, color):
        if not isinstance(color, str):
            raise ValueError("Color must be a hex string")
        color = color.strip("#")
        return int(color, 16) / 255.0
     
     def hex_to_tuple(self, color):
        if not isinstance(color, str):
            raise ValueError("Color must be a hex string")
        color = color.strip("#")
        return tuple([int(color[i:i + 2], 16) for i in range(0, len(color), 2)])
     
     # Tensor to PIL
     def tensor2pil(self, image):
        return Image.fromarray(np.clip(255. * image.cpu().numpy().squeeze(), 0, 255).astype(np.uint8))
    
     # PIL to Tensor
     def pil2tensor(self, image):
        return torch.from_numpy(np.array(image).astype(np.float32) / 255.0).unsqueeze(0)



class AddPadding(AddPaddingBase):

    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "left": ("INT", {"default": 0, "step": 1, "min": 0, "max": 4096}),
                "top": ("INT", {"default": 0, "step": 1, "min": 0, "max": 4096}),
                "right": ("INT", {"default": 0, "step": 1, "min": 0, "max": 4096}),
                "bottom": ("INT", {"default": 0, "step": 1, "min": 0, "max": 4096}),
                "color": ("STRING", {"default": "#ffffff"}),
                "transparent": ("BOOLEAN", {"default": False}),
            },
        }
    
    RETURN_TYPES = ("IMAGE", "MASK")

    def resize(self, image, left, top, right, bottom, color, transparent):
        return (self.add_padding(image, left, top, right, bottom, color, transparent),
                self.create_mask(image, left, top, right, bottom),)


NODE_CLASS_MAPPINGS = {
    "comfyui-easy-padding": AddPadding,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "comfyui-easy-padding": "ComfyUI Easy Padding",
}