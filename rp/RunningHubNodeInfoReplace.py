import random

class RunningHubNodeInfoReplaceNode:
    """Node for creating individual nodeInfo entries with advanced text replacement and line loading capabilities"""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "node_id": ("STRING", {"default": ""}),
                "field_name": ("STRING", {"default": ""}),
                "comment": ("STRING", {"default": ""}),
                "field_value": ("STRING", {"default": "", "multiline": True}),
                "match": ("STRING", {"default": ""}),
                "replace": ("STRING", {"default": "", "multiline": True}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "increment": ("INT", {"default": 1, "min": 1, "max": 1000}),
                "random_mode": (["normal", "reverse", "odd_forward", "even_forward", "odd_reverse", "even_reverse"], {"default": "normal"}),
            }
        }

    RETURN_TYPES = ("NODEINFO", "INT")
    RETURN_NAMES = ("node_info", "new_seed")
    FUNCTION = "create_node_info"
    CATEGORY = "🌻 Addoor/RHAPI"

    def create_node_info(self, node_id: str, field_name: str, comment: str, field_value: str, match: str, replace: str, seed: int, increment: int, random_mode: str):
        # Split the field_value and replace into lines
        field_lines = field_value.split('\n')
        replace_lines = replace.split('\n') if replace else []

        # Prepare the lines based on the random_mode
        if random_mode == "reverse":
            field_lines = field_lines[::-1]
            replace_lines = replace_lines[::-1]
        elif random_mode == "odd_forward":
            field_lines = field_lines[::2]
            replace_lines = replace_lines[::2]
        elif random_mode == "even_forward":
            field_lines = field_lines[1::2]
            replace_lines = replace_lines[1::2]
        elif random_mode == "odd_reverse":
            field_lines = field_lines[::-1][::2]
            replace_lines = replace_lines[::-1][::2]
        elif random_mode == "even_reverse":
            field_lines = field_lines[::-1][1::2]
            replace_lines = replace_lines[::-1][1::2]

        # Ensure we have at least one line
        if not field_lines:
            field_lines = [""]
        if not replace_lines:
            replace_lines = [""]

        # Select a line based on the seed
        random.seed(seed)
        selected_line = field_lines[seed % len(field_lines)]

        # Perform text replacement
        if match and replace_lines:
            replace_value = replace_lines[seed % len(replace_lines)]
            selected_line = selected_line.replace(match, replace_value)

        node_info = {
            "nodeId": node_id,
            "fieldName": field_name,
            "fieldValue": selected_line
        }

        # Increment the seed for potential future use
        new_seed = seed + increment

        return (node_info, new_seed)

