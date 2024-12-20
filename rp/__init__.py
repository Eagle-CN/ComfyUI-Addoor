"""
RunningHub API (RHAPI) for ComfyUI
Provides nodes for interacting with RunningHub API
"""

import os
import configparser
import base64
import hashlib

BASE_URL = "https://www.runninghub.cn"

def validate_api_key(api_key: str) -> bool:
    """Validate the format of the API key"""
    if not api_key or len(api_key) != 32:
        return False
    return True

class EncryptionManager:
    @staticmethod
    def verify_license_key(license_key, user_id, phone):
        expected_key = EncryptionManager.generate_license_key(user_id, phone)
        return license_key == expected_key

    @staticmethod
    def generate_license_key(user_id, phone):
        unique_key = f"{user_id}:{phone}".encode()
        hash_object = hashlib.sha256(unique_key)
        hash_digest = hash_object.digest()
        license_key = base64.urlsafe_b64encode(hash_digest).decode()[:32]
        return license_key

def load_nodes():
    # 读取配置文件
    config = configparser.ConfigParser()
    config_path = os.path.join(os.path.dirname(__file__), 'config.ini')
    config.read(config_path)

    # 从配置文件中获取许可证密钥和用户ID
    license_key = config.get('License', 'COMFYUI_RHAPI_LICENSE_KEY', fallback=None)
    user_id = config.get('License', 'COMFYUI_RHAPI_USER_ID', fallback=None)
    phone = config.get('License', 'COMFYUI_RHAPI_PHONE', fallback=None)

    # 如果配置文件中没有，则尝试从环境变量获取
    if not license_key:
        license_key = os.environ.get('COMFYUI_RHAPI_LICENSE_KEY')
    if not user_id:
        user_id = os.environ.get('COMFYUI_RHAPI_USER_ID')
    if not phone:
        phone = os.environ.get('COMFYUI_RHAPI_PHONE')

    if license_key and user_id and phone and EncryptionManager.verify_license_key(license_key, user_id, phone):
        print("ComfyUI-RHAPI plugin is activated successfully.")
        # 导入所有节点类
        from .RunningHubInit import RunningHubInitNode
        from .RunningHubNodeInfo import RunningHubNodeInfoNode
        from .RunningHubNodeInfoCollector import RunningHubNodeInfoCollectorNode
        from .RunningHubWorkflowExecutor import RunningHubWorkflowExecutorNode
        from .RunningHubAccountStatus import RunningHubAccountStatusNode
        from .RunningHubFileSaver import RunningHubFileSaverNode
        from .RunningHubWorkflowID import RunningHubWorkflowIDNode
        from .RunningHubFilePreviewer import RunningHubFilePreviewerNode
        from .RunningHubNodeInfoReplace import RunningHubNodeInfoReplaceNode

        NODE_CLASS_MAPPINGS = {
            "RunningHubInit": RunningHubInitNode,
            "RunningHubNodeInfo": RunningHubNodeInfoNode,
            "RunningHubNodeInfoCollector": RunningHubNodeInfoCollectorNode,
            "RunningHubWorkflowExecutor": RunningHubWorkflowExecutorNode,
            "RunningHubAccountStatus": RunningHubAccountStatusNode,
            "RunningHubFileSaver": RunningHubFileSaverNode,
            "RunningHubWorkflowID": RunningHubWorkflowIDNode,
            "RunningHubFilePreviewer": RunningHubFilePreviewerNode,
            "RunningHubNodeInfoReplace": RunningHubNodeInfoReplaceNode,
        }

        NODE_DISPLAY_NAME_MAPPINGS = {
            "RunningHubInit": "RunningHub Initialize",
            "RunningHubNodeInfo": "RunningHub Node Info",
            "RunningHubNodeInfoCollector": "RunningHub Node Info Collector",
            "RunningHubWorkflowExecutor": "RunningHub Workflow Executor",
            "RunningHubAccountStatus": "RunningHub Account Status",
            "RunningHubFileSaver": "RunningHub File Saver",
            "RunningHubWorkflowID": "RunningHub Workflow ID",
            "RunningHubFilePreviewer": "RunningHub File Previewer",
            "RunningHubNodeInfoReplace": "RunningHub Node Info Replace",
        }

        return NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS
    else:
        print("Invalid or missing license key. ComfyUI-RHAPI plugin is disabled.")
        return {}, {}

NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS = load_nodes()

