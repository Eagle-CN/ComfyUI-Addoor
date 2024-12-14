import random

class AD_PromptReplace:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Content": ("STRING", {"default": "", "multiline": True}),
                "Match": ("STRING", {"default": ""}),
                "Replace": ("STRING", {"default": "", "multiline": True}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff, "step": 1, "control_after_generate": True}),
                "Increment": ("INT", {"default": 1, "min": 1, "max": 1000}),
                "Random_Mode": (["normal", "reverse", "odd_forward", "even_forward", "odd_reverse", "even_reverse"], {"default": "normal"}),
            }
        }

    RETURN_TYPES = ("STRING", "INT")
    RETURN_NAMES = ("Replaced_Text", "new_seed")
    FUNCTION = "replace_prompt"
    CATEGORY = "Addoor"

    def replace_prompt(self, Content: str, Match: str, Replace: str, seed: int, Increment: int, Random_Mode: str):
        # Split the Content and Replace into lines
        content_lines = Content.split('\n')
        replace_lines = Replace.split('\n') if Replace else []

        # Prepare the lines based on the Random_Mode
        if Random_Mode == "reverse":
            content_lines = content_lines[::-1]
            replace_lines = replace_lines[::-1]
        elif Random_Mode == "odd_forward":
            content_lines = content_lines[::2]
            replace_lines = replace_lines[::2]
        elif Random_Mode == "even_forward":
            content_lines = content_lines[1::2]
            replace_lines = replace_lines[1::2]
        elif Random_Mode == "odd_reverse":
            content_lines = content_lines[::-1][::2]
            replace_lines = replace_lines[::-1][::2]
        elif Random_Mode == "even_reverse":
            content_lines = content_lines[::-1][1::2]
            replace_lines = replace_lines[::-1][1::2]

        # Ensure we have at least one line
        if not content_lines:
            content_lines = [""]
        if not replace_lines:
            replace_lines = [""]

        # Select a line based on the seed
        random.seed(seed)
        selected_line = content_lines[seed % len(content_lines)]

        # Perform text replacement
        if Match and replace_lines:
            replace_value = replace_lines[seed % len(replace_lines)]
            selected_line = selected_line.replace(Match, replace_value)

        # Increment the seed for potential future use
        new_seed = seed + Increment

        return (selected_line, new_seed)

N_CLASS_MAPPINGS = {
    "AD_PromptReplace": AD_PromptReplace,
}

N_DISPLAY_NAME_MAPPINGS = {
    "AD_PromptReplace": "🌻 Prompt Replace",
}

