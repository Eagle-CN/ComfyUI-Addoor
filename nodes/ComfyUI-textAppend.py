# text_append_node.py

class TextAppendNode:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "current_text": ("STRING", {"multiline": True}),
                "new_text": ("STRING", {"multiline": True}),
                "mode": (["append", "prepend"],),
            },
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "process_text"
    CATEGORY = "🌻 Addoor/text"

    def process_text(self, current_text, new_text, mode):
        current_lines = [line.strip() for line in current_text.split('\n') if line.strip()]
        new_lines = [line.strip() for line in new_text.split('\n') if line.strip()]
        
        result = []
        
        # If current_text is empty, return new_text
        if not current_lines:
            return (new_text,)
        
        if mode == "append":
            for current_line in current_lines:
                for new_line in new_lines:
                    result.append(f"{current_line} {new_line}")
        elif mode == "prepend":
            for current_line in current_lines:
                for new_line in new_lines:
                    result.append(f"{new_line} {current_line}")
        
        return ('\n'.join(result),)

NODE_CLASS_MAPPINGS = {
    "TextAppendNode": TextAppendNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TextAppendNode": "Text Append/Prepend"
}