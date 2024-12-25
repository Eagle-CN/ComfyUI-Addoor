"""
RunningHub API (RHAPI) for ComfyUI
Provides nodes for interacting with RunningHub API
"""

import os
import configparser
import base64
import hashlib
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    try:
        # 读取配置文件
        config = configparser.ConfigParser()
        config_path = os.path.join(os.path.dirname(__file__), 'config.ini')
        if not os.path.exists(config_path):
            logger.error(f"Config file not found: {config_path}")
            return {}, {}
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

        if not all([license_key, user_id, phone]):
            logger.error("Missing license key, user ID, or phone number.")
            return {}, {}

        if EncryptionManager.verify_license_key(license_key, user_id, phone):
            logger.info("ComfyUI-RHAPI plugin is activated successfully.")
            # 导入所有节点类
            NODE_CLASS_MAPPINGS = {}
            NODE_DISPLAY_NAME_MAPPINGS = {}

            node_modules = [
                ('RunningHubInit', 'RunningHubInitNode', 'RunningHub Initialize'),
                ('RunningHubNodeInfo', 'RunningHubNodeInfoNode', 'RunningHub Node Info'),
                ('RunningHubNodeInfoCollector', 'RunningHubNodeInfoCollectorNode', 'RunningHub Node Info Collector'),
                ('RunningHubWorkflowExecutor', 'RunningHubWorkflowExecutorNode', 'RunningHub Workflow Executor'),
                ('RunningHubAccountStatus', 'RunningHubAccountStatusNode', 'RunningHub Account Status'),
                ('RunningHubFileSaver', 'RunningHubFileSaverNode', 'RunningHub File Saver'),
                ('RunningHubWorkflowID', 'RunningHubWorkflowIDNode', 'RunningHub Workflow ID'),
                ('RunningHubFilePreviewer', 'RunningHubFilePreviewerNode', 'RunningHub File Previewer'),
                ('RunningHubNodeInfoReplace', 'RunningHubNodeInfoReplaceNode', 'RunningHub Node Info Replace'),
            ]

            for module_name, class_name, display_name in node_modules:
                try:
                    module = __import__(f'ComfyUI-Addoor.rp.{module_name}', fromlist=[class_name])
                    node_class = getattr(module, class_name)
                    NODE_CLASS_MAPPINGS[module_name] = node_class
                    NODE_DISPLAY_NAME_MAPPINGS[module_name] = display_name
                except ImportError as e:
                    logger.error(f"Error importing {module_name}: {str(e)}")
                except AttributeError as e:
                    logger.error(f"Error getting class {class_name} from {module_name}: {str(e)}")

            return NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS
        else:
            logger.error("Invalid license key. ComfyUI-RHAPI plugin is disabled.")
            return {}, {}
    except Exception as e:
        logger.exception(f"Unexpected error in load_nodes: {str(e)}")
        return {}, {}

NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS = load_nodes()

