import requests
import json
from . import validate_api_key

class RunningHubAccountStatusNode:
    """Node for checking account status"""
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "api_key": ("STRING", {"default": ""}),
            }
        }
    
    RETURN_TYPES = ("INT", "INT")
    RETURN_NAMES = ("remain_coins", "current_task_counts")
    FUNCTION = "check_account_status"
    CATEGORY = "🌻 Addoor/RHAPI"
    OUTPUT_NODE = True
    
    def check_account_status(self, api_key: str):
        if not validate_api_key(api_key):
            raise ValueError("Invalid API key")
            
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Apifox/1.0.0 (https://apifox.com)",
            "Accept": "*/*",
            "Host": "www.runninghub.cn",
            "Connection": "keep-alive"
        }
        
        data = {
            "apikey": api_key
        }
        
        endpoint = "https://www.runninghub.cn/uc/openapi/accountStatus"
        
        try:
            response = requests.post(
                endpoint,
                headers=headers,
                json=data
            )
            response.raise_for_status()
            result = response.json()
            
            remain_coins = int(result['data']['remainCoins'])
            current_task_counts = int(result['data']['currentTaskCounts'])
            
            return {
                "ui": {"text": json.dumps(result, indent=2)},
                "result": (remain_coins, current_task_counts)
            }
        except requests.exceptions.RequestException as e:
            error_message = f"API request failed: {str(e)}"
            return {
                "ui": {"text": error_message},
                "result": (0, 0)
            }

