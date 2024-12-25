import random

class AD_PromptReplace:
    def __init__(self):
        self.current_index = None

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Content": ("STRING", {"default": "", "multiline": True}),
                "Match": ("STRING", {"default": ""}),
                "Replace": ("STRING", {"default": "", "multiline": True}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "Increment": ("INT", {"default": 1, "min": 0, "max": 1000}),
            }
        }

    RETURN_TYPES = ("STRING", "INT")
    RETURN_NAMES = ("Replaced_Text", "new_seed")
    FUNCTION = "replace_prompt"
    CATEGORY = "🌻 Addoor/Utilities"

    def replace_prompt(self, Content: str, Match: str, Replace: str, seed: int, Increment: int):
        content_lines = Content.split('\n')
        replace_lines = Replace.split('\n') if Replace else []

        if not content_lines:
            content_lines = [""]
        if not replace_lines:
            replace_lines = [""]

        # Initialize current_index if it's None
        if self.current_index is None:
            if Increment == 0:
                # Random starting point
                random.seed(seed)
                self.current_index = random.randint(0, len(replace_lines) - 1)
            else:
                # Start from the beginning
                self.current_index = 0

        # Select a line based on increment
        if Increment == 0:
            # Random selection using seed
            random.seed(seed)
            selected_index = random.randint(0, len(replace_lines) - 1)
        else:
            # Sequential selection based on increment
            selected_index = self.current_index
            self.current_index = (self.current_index + Increment) % len(replace_lines)

        selected_replace = replace_lines[selected_index]

        # Perform text replacement
        replaced_content = Content.replace(Match, selected_replace) if Match else Content

        return (replaced_content, seed)

