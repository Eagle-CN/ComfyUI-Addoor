import requests
from . import validate_api_key, BASE_URL

class RunningHubAccountStatusNode:
    """Node for checking account status"""
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "api_key": ("STRING", {"default": ""}),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    FUNCTION = "check_account_status"
    CATEGORY = "RunningHub"
    
    def check_account_status(self, api_key: str):
        if not validate_api_key(api_key):
            raise ValueError("Invalid API key")
            
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": "Apifox/1.0.0 (https://apifox.com)",
            "Accept": "*/*",
            "Host": "www.runninghub.cn",
            "Connection": "keep-alive"
        }
        
        endpoint = f"{BASE_URL}/task/openapi/account-status"
        
        try:
            response = requests.get(
                endpoint,
                headers=headers
            )
            response.raise_for_status()
            return (response.text,)
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"API request failed: {str(e)}")

