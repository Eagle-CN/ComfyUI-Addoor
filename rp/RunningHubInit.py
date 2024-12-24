from . import validate_api_key

class RunningHubInitNode:
    """Node for initializing RunningHub API connection"""
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "api_key": ("STRING", {"default": "", "multiline": False}),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    FUNCTION = "initialize"
    CATEGORY = "🌻 Addoor/RHAPI"
    
    def initialize(self, api_key: str):
        if not validate_api_key(api_key):
            raise ValueError("Invalid API key format")
        return (api_key,)

