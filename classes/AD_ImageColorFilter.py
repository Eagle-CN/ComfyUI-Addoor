import numpy as np
from PIL import Image, ImageEnhance
from skimage import color, exposure
import torch

class AD_ImageColorFilter:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "exposure": ("INT", {"default": 0, "min": -100, "max": 100, "step": 1}),
                "clarity": ("INT", {"default": 0, "min": -100, "max": 100, "step": 1}),
                "highlights": ("INT", {"default": 0, "min": -100, "max": 100, "step": 1}),
                "shadows": ("INT", {"default": 0, "min": -100, "max": 100, "step": 1}),
                "contrast": ("INT", {"default": 0, "min": -100, "max": 100, "step": 1}),
                "saturation": ("INT", {"default": 0, "min": -100, "max": 100, "step": 1}),
                "vibrance": ("INT", {"default": 0, "min": -100, "max": 100, "step": 1}),
                "temperature": ("INT", {"default": 0, "min": -100, "max": 100, "step": 1}),
                "sharpness": ("INT", {"default": 0, "min": -100, "max": 100, "step": 1}),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "apply_filter"
    CATEGORY = "Addoor"

    def apply_filter(self, image, exposure, clarity, highlights, shadows, contrast, saturation, vibrance, temperature, sharpness):
        # Ensure image is in the correct format
        if isinstance(image, torch.Tensor):
            if image.dim() == 4:  # Batch of images
                image = image.squeeze(0)  # Remove batch dimension
            if image.shape[0] == 3:  # If channels are first
                image = image.permute(1, 2, 0)  # CHW to HWC
            image = image.cpu().numpy()

        # Ensure image is float32 and in 0-1 range
        image = image.astype(np.float32)
        if image.max() > 1.0:
            image /= 255.0

        # Ensure image is RGB
        if image.shape[-1] != 3:
            if image.shape[0] == 3:  # If it's in CHW format
                image = np.transpose(image, (1, 2, 0))
            elif image.shape[-1] == 1:  # Grayscale
                image = np.repeat(image, 3, axis=-1)
            else:
                raise ValueError(f"Unsupported image shape: {image.shape}")

        # Convert to PIL Image
        image_pil = Image.fromarray((image * 255).astype(np.uint8))

        # Apply exposure adjustment
        image_pil = ImageEnhance.Brightness(image_pil).enhance(1 + (exposure / 100))

        # Apply clarity (local contrast)
        image_np = np.array(image_pil).astype(np.float32) / 255.0
        image_np = exposure.equalize_adapthist(image_np, clip_limit=(clarity / 100) + 1)

        # Apply highlights and shadows adjustments
        image_np = exposure.adjust_gamma(image_np, 1 - (highlights / 200), 1 + (shadows / 200))

        # Apply contrast
        image_np = exposure.adjust_sigmoid(image_np, cutoff=0.5, gain=(contrast / 10) + 1)

        # Apply saturation
        image_hsv = color.rgb2hsv(image_np)
        image_hsv[:, :, 1] = np.clip(image_hsv[:, :, 1] * (1 + (saturation / 100)), 0, 1)
        image_np = color.hsv2rgb(image_hsv)

        # Apply vibrance (increase saturation of less-saturated colors)
        max_channel = np.max(image_np, axis=2)
        min_channel = np.min(image_np, axis=2)
        saturation_mask = 1 - (max_channel - min_channel) / (max_channel + 1e-8)  # Avoid division by zero
        image_hsv = color.rgb2hsv(image_np)
        image_hsv[:, :, 1] = np.clip(image_hsv[:, :, 1] + (vibrance / 100) * saturation_mask[:, :, np.newaxis], 0, 1)
        image_np = color.hsv2rgb(image_hsv)

        # Apply temperature (color balance)
        temperature_matrix = np.array([1 + (temperature / 100), 1, 1 - (temperature / 100)])
        image_np = image_np * temperature_matrix

        # Convert back to PIL Image for sharpness
        image_pil = Image.fromarray((np.clip(image_np, 0, 1) * 255).astype(np.uint8))

        # Apply sharpness
        image_pil = ImageEnhance.Sharpness(image_pil).enhance(1 + (sharpness / 100))

        # Convert back to numpy array
        image_np = np.array(image_pil).astype(np.float32) / 255.0

        # Clip values and convert back to torch tensor
        image_np = np.clip(image_np, 0, 1)
        return (torch.from_numpy(image_np).unsqueeze(0).permute(2, 0, 1).float(),)

N_CLASS_MAPPINGS = {
    "AD_ImageColorFilter": AD_ImageColorFilter,
}

N_DISPLAY_NAME_MAPPINGS = {
    "AD_ImageColorFilter": "🌻 Image Color Filter",
}

