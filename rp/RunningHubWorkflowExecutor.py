import requests
import json
import time
import logging
from . import validate_api_key, BASE_URL

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RunningHubWorkflowExecutorNode:
    """Node for executing RunningHub workflows and monitoring task status"""
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "api_key": ("STRING", {"default": ""}),
                "workflow_id": ("STRING", {"default": ""}),
                "node_info_list": ("NODEINFOLIST",),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "max_attempts": ("INT", {"default": 60, "min": 1, "max": 1000}),
                "interval_seconds": ("FLOAT", {"default": 5.0, "min": 1.0, "max": 60.0}),
            }
        }
    
    RETURN_TYPES = ("FILEURL_LIST", "STRING", "STRING", "STRING", "STRING", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("file_urls", "task_id", "msg", "promptTips", "taskStatus", "fileType", "code", "json")
    FUNCTION = "execute_workflow_and_monitor"
    CATEGORY = "🌻 Addoor/RHAPI"
    
    def execute_workflow_and_monitor(self, api_key: str, workflow_id: str, node_info_list: list, seed: int, max_attempts: int, interval_seconds: float):
        if not validate_api_key(api_key):
            raise ValueError("Invalid API key")
            
        # 确保 node_info_list 是列表类型
        if not isinstance(node_info_list, list):
            node_info_list = [node_info_list]
        
        # 移除可能的重复项
        unique_node_info = {
            (info.get('nodeId'), info.get('fieldName')): info 
            for info in node_info_list
        }.values()
        
        workflow_data = {
            "workflowId": int(workflow_id),
            "apiKey": api_key,
            "nodeInfoList": list(unique_node_info),
            "seed": seed
        }
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": "Apifox/1.0.0 (https://apifox.com)",
            "Accept": "*/*",
            "Host": "www.runninghub.cn",
            "Connection": "keep-alive"
        }
        
        workflow_endpoint = f"{BASE_URL}/task/openapi/create"
        
        try:
            logger.info(f"Executing workflow with ID: {workflow_id}")
            workflow_response = requests.post(
                workflow_endpoint,
                headers=headers,
                json=workflow_data
            )
            workflow_response.raise_for_status()
            workflow_result = workflow_response.json()
            
            if not workflow_result or 'data' not in workflow_result:
                raise ValueError("Invalid response from workflow execution")
            
            task_id = workflow_result.get('data', {}).get('taskId')
            if not task_id:
                raise ValueError("No task ID returned from workflow execution")
            
            logger.info(f"Workflow executed. Task ID: {task_id}")
            
            # Monitor task status
            task_data = {
                "taskId": task_id,
                "apiKey": api_key
            }
            
            task_endpoint = f"{BASE_URL}/task/openapi/outputs"
            
            for attempt in range(max_attempts):
                try:
                    logger.info(f"Checking task status. Attempt {attempt + 1}/{max_attempts}")
                    task_response = requests.post(
                        task_endpoint,
                        headers=headers,
                        json=task_data
                    )
                    task_response.raise_for_status()
                    task_result = task_response.json()
                    
                    if not task_result or 'data' not in task_result or not task_result['data']:
                        logger.warning("Invalid or empty response from task status check")
                        time.sleep(interval_seconds)
                        continue
                    
                    task_status = task_result['data'][0].get('taskStatus', '')
                    
                    if task_status in ['SUCCEDD', 'FAILED']:
                        logger.info(f"Task completed with status: {task_status}")
                        break
                    elif task_status in ['QUEUED', 'RUNNING']:
                        logger.info(f"Task status: {task_status}. Waiting...")
                        time.sleep(interval_seconds)
                    else:
                        logger.warning(f"Unknown task status: {task_status}")
                        break
                
                except requests.exceptions.RequestException as e:
                    logger.error(f"Error checking task status: {str(e)}")
                    time.sleep(interval_seconds)
            
            # Prepare return values
            msg = workflow_result.get('msg', '')
            prompt_tips = json.dumps(workflow_result.get('data', {}).get('promptTips', ''))
            
            # 处理多个文件URL
            file_urls = []
            if task_result and 'data' in task_result and task_result['data']:
                for item in task_result['data']:
                    if 'fileUrl' in item:
                        file_urls.append(item['fileUrl'])
            
            # 如果没有文件URL，添加空字符串
            if not file_urls:
                file_urls = [""]
                
            file_type = task_result['data'][0].get('fileType', '') if task_result and 'data' in task_result and task_result['data'] else ''
            code = str(task_result.get('code', '')) if task_result else ''
            
            return (file_urls, task_id, msg, prompt_tips, task_status, file_type, code, json.dumps(task_result))
        
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {str(e)}")
            return ([""], "", f"Error: {str(e)}", "{}", "ERROR", "", "error", "")
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {str(e)}")
            return ([""], "", f"Error: Invalid JSON response", "{}", "ERROR", "", "error", "")
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return ([""], "", f"Error: {str(e)}", "{}", "ERROR", "", "error", "")

