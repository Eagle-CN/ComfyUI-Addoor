"""
This node provides a multiline input field for a string.
Input:
    string
Output:
    STRING: A copy of 'string'.
"""
class MultilineString:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "string": ("STRING", {
                    "multiline": True,
                    "default": "",
                }),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("STRING",)
    FUNCTION = "get_string"
    OUTPUT_NODE = True
    CATEGORY = "🌻 Addoor/text"

    def get_string(self, string):
        return (string,)


# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "YANC.MultilineString": MultilineString,
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "YANC.MultilineString": "Multiline String",
}
