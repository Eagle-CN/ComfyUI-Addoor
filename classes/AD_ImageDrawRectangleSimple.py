import torch
import numpy as np
from PIL import Image, ImageDraw
import torchvision.transforms as t
from comfy_extras import nodes_mask as masks

def tensor_to_image(tensor):
    return t.ToPILImage()(tensor.permute(2, 0, 1))

def image_to_tensor(image):
    return t.ToTensor()(image).permute(1, 2, 0)

def get_sampler_by_name(method):
    if method == "lanczos":
        return Image.LANCZOS
    elif method == "bicubic":
        return Image.BICUBIC
    elif method == "hamming":
        return Image.HAMMING
    elif method == "bilinear":
        return Image.BILINEAR
    elif method == "box":
        return Image.BOX
    elif method == "nearest":
        return Image.NEAREST
    else:
        raise ValueError("Sampler not found.")

class AD_ImageDrawRectangleSimple:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "width": ("INT", {
                    "default": 512,
                    "min": 1,
                    "step": 1
                }),
                "height": ("INT", {
                    "default": 512,
                    "min": 1,
                    "step": 1
                }),
                "left": ("INT", {
                    "default": 50,
                    "min": 0,
                    "step": 1
                }),
                "top": ("INT", {
                    "default": 50,
                    "min": 0,
                    "step": 1
                }),
                "right": ("INT", {
                    "default": 50,
                    "min": 0,
                    "step": 1
                }),
                "bottom": ("INT", {
                    "default": 50,
                    "min": 0,
                    "step": 1
                }),
                "radius": ("INT", {
                    "default": 20,
                    "min": 0,
                    "step": 1
                }),
                "fill_red": ("INT", {
                    "default": 255,
                    "min": 0,
                    "max": 255,
                    "step": 1
                }),
                "fill_green": ("INT", {
                    "default": 255,
                    "min": 0,
                    "max": 255,
                    "step": 1
                }),
                "fill_blue": ("INT", {
                    "default": 255,
                    "min": 0,
                    "max": 255,
                    "step": 1
                }),
                "fill_alpha": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01
                }),
                "SSAA": ("INT", {
                    "default": 4,
                    "min": 1,
                    "max": 16,
                    "step": 1
                }),
                "method": (["lanczos", "bicubic", "hamming", "bilinear", "box", "nearest"],),
            },
        }

    RETURN_TYPES = ("IMAGE", "MASK")
    RETURN_NAMES = ("IMAGE", "MASK")
    FUNCTION = "node"
    CATEGORY = "🌻 Addoor/Util"

    def node(
            self,
            width,
            height,
            left,
            top,
            right,
            bottom,
            radius,
            fill_red,
            fill_green,
            fill_blue,
            fill_alpha,
            SSAA,
            method
    ):
        # Calculate the rectangle coordinates with inward offsets
        rect_left = left * SSAA
        rect_top = top * SSAA
        rect_right = (width - right) * SSAA
        rect_bottom = (height - bottom) * SSAA

        canvas = Image.new("RGBA", (width * SSAA, height * SSAA), (0, 0, 0, 0))
        mask_canvas = Image.new("L", (width * SSAA, height * SSAA), 0)  # Create mask canvas

        draw = ImageDraw.Draw(canvas)
        mask_draw = ImageDraw.Draw(mask_canvas)  # Create mask draw object

        draw.rounded_rectangle(
            (
                (rect_left, rect_top),
                (rect_right, rect_bottom)
            ),
            radius * SSAA,
            (fill_red, fill_green, fill_blue, int(fill_alpha * 255))
        )
        mask_draw.rounded_rectangle(  # Draw white rectangle on mask
            (
                (rect_left, rect_top),
                (rect_right, rect_bottom)
            ),
            radius * SSAA,
            fill=255
        )

        canvas = canvas.resize((width, height), get_sampler_by_name(method))
        mask_canvas = mask_canvas.resize((width, height), get_sampler_by_name(method))

        # Convert PIL Image to tensor
        tensor = image_to_tensor(canvas)
        mask_tensor = torch.from_numpy(np.array(mask_canvas)).float() / 255.0

        # Add batch dimension
        tensor = tensor.unsqueeze(0)
        mask_tensor = mask_tensor.unsqueeze(0)

        return (tensor, mask_tensor)

N_CLASS_MAPPINGS = {
    "AD_ImageDrawRectangleSimple": AD_ImageDrawRectangleSimple,
}

N_DISPLAY_NAME_MAPPINGS = {
    "AD_ImageDrawRectangleSimple": "🌻 Draw Simple Rectangle",
}

