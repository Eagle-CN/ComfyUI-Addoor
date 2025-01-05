"""
@name: "ComfyUI FofrToolkit",
@version: (1,0,0),
@author: "fofr",
@description: "Experimental toolkit for comfyui.",
@project: "https://github.com/fofr/comfyui-fofr-toolkit",
@url: "https://github.com/fofr",
"""


class ToolkitIncrementer:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "current_index": (
                    "INT",
                    {
                        "default": 0,
                        "min": 0,
                        "max": 0xFFFFFFFFFFFFFFFF,
                        "control_after_generate": True,
                    },
                ),
            },
            "optional": {
                "max": (
                    "INT",
                    {"default": 10, "min": 0, "max": 0xFFFFFFFFFFFFFFFF},
                ),
            },
        }

    RETURN_TYPES = ("INT", "STRING")
    RETURN_NAMES = ("INT", "STRING")
    FUNCTION = "increment"
    CATEGORY = "🌻 Addoor/Utilities"

    def increment(self, current_index, max=0):
        if max == 0:
            result = current_index
        else:
            result = current_index % (max + 1)
            
        return (result, str(result))


class ToolkitWidthAndHeightFromAspectRatio:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "aspect_ratio": (
                    [
                        "1:1",
                        "1:2",
                        "2:1",
                        "2:3",
                        "3:2",
                        "3:4",
                        "4:3",
                        "4:5",
                        "5:4",
                        "9:16",
                        "16:9",
                        "9:21",
                        "21:9",
                    ],
                    {"default": "1:1"},
                ),
                "target_size": ("INT", {"default": 1024, "min": 64, "max": 8192}),
            },
            "optional": {
                "multiple_of": ("INT", {"default": 8, "min": 1, "max": 1024}),
            },
        }

    RETURN_TYPES = ("INT", "INT")
    RETURN_NAMES = ("width", "height")
    FUNCTION = "width_and_height_from_aspect_ratio"
    CATEGORY = "🌻 Addoor/Utilities"

    def width_and_height_from_aspect_ratio(
        self, aspect_ratio, target_size, multiple_of=8
    ):
        w, h = map(int, aspect_ratio.split(":"))
        scale = (target_size**2 / (w * h)) ** 0.5
        width = round(w * scale / multiple_of) * multiple_of
        height = round(h * scale / multiple_of) * multiple_of
        return (width, height)


class ToolkitWidthAndHeightForImageScaling:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "target_size": (
                    "INT",
                    {"default": 1024, "min": 64, "max": 8192},
                ),
            },
            "optional": {
                "multiple_of": ("INT", {"default": 8, "min": 1, "max": 1024}),
            },
        }

    RETURN_TYPES = ("INT", "INT")
    RETURN_NAMES = ("width", "height")
    FUNCTION = "scale_image_to_target"
    CATEGORY = "🌻 Addoor/Utilities"

    def scale_image_to_target(self, image, target_size, multiple_of=8):
        h, w = image.shape[1:3]
        scale = (target_size**2 / (w * h)) ** 0.5
        width = round(w * scale / multiple_of) * multiple_of
        height = round(h * scale / multiple_of) * multiple_of
        return (width, height)


NODE_CLASS_MAPPINGS = {
    "Incrementer 🪴": ToolkitIncrementer,
    "Width and height from aspect ratio 🪴": ToolkitWidthAndHeightFromAspectRatio,
    "Width and height for scaling image to ideal resolution 🪴": ToolkitWidthAndHeightForImageScaling,
}
