"""
RunningHub API (RHAPI) for ComfyUI
Provides nodes for interacting with RunningHub API
"""

import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = "https://www.runninghub.cn"

def validate_api_key(api_key: str) -> bool:
    """Validate the format of the API key"""
    if not api_key or len(api_key) != 32:
        return False
    return True

# 直接注册所有节点
NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

node_modules = [
    ('RunningHubInit', 'RunningHubInitNode', 'RunningHub Initialize'),
    ('RunningHubNodeInfo', 'RunningHubNodeInfoNode', 'RunningHub Node Info'),
    ('RunningHubWorkflowExecutor', 'RunningHubWorkflowExecutorNode', 'RunningHub Workflow Executor'),
    ('RunningHubAccountStatus', 'RunningHubAccountStatusNode', 'RunningHub Account Status'),
    ('RunningHubFileSaver', 'RunningHubFileSaverNode', 'RunningHub File Saver'),
    ('RunningHubWorkflowID', 'RunningHubWorkflowIDNode', 'RunningHub Workflow ID'),
    ('RunningHubFilePreviewer', 'RunningHubFilePreviewerNode', 'RunningHub File Previewer'),
    ('RunningHubNodeInfoReplace', 'RunningHubNodeInfoReplaceNode', 'RunningHub Node Info Replace'),
    ('RunningHubImageUploader', 'RunningHubImageUploaderNode', 'RunningHub Image Uploader'),
]

# 导入并注册节点
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

