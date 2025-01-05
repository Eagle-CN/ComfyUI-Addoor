"""
Addoor Nodes for ComfyUI
Provides nodes for image processing and other utilities
"""

import os
import glob
import logging
import importlib

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 首先定义映射字典
NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

# 获取当前目录下所有的 .py 文件
current_dir = os.path.dirname(os.path.abspath(__file__))
py_files = glob.glob(os.path.join(current_dir, "*.py"))

# 直接注册所有节点
for file_path in py_files:
    # 跳过 __init__.py
    if "__init__.py" in file_path:
        continue
        
    try:
        # 获取模块名（不含.py）
        module_name = os.path.basename(file_path)[:-3]
        # 使用相对导入
        module = importlib.import_module(f".{module_name}", package=__package__)
        
        # 如果模块有节点映射，则更新
        if hasattr(module, 'NODE_CLASS_MAPPINGS'):
            NODE_CLASS_MAPPINGS.update(module.NODE_CLASS_MAPPINGS)
        if hasattr(module, 'NODE_DISPLAY_NAME_MAPPINGS'):
            NODE_DISPLAY_NAME_MAPPINGS.update(module.NODE_DISPLAY_NAME_MAPPINGS)
            
        logger.info(f"Imported {module_name} successfully")
    except ImportError as e:
        logger.error(f"Error importing {module_name}: {str(e)}")
    except Exception as e:
        logger.error(f"Error processing {module_name}: {str(e)}")

# 如果允许测试节点，导入测试节点
allow_test_nodes = True
if allow_test_nodes:
    try:
        from .excluded.experimental_nodes import *
        # 更新映射
        if 'NODE_CLASS_MAPPINGS' in locals():
            NODE_CLASS_MAPPINGS.update(locals().get('NODE_CLASS_MAPPINGS', {}))
        if 'NODE_DISPLAY_NAME_MAPPINGS' in locals():
            NODE_DISPLAY_NAME_MAPPINGS.update(locals().get('NODE_DISPLAY_NAME_MAPPINGS', {}))
    except ModuleNotFoundError:
        pass

logger.debug(f"Registered nodes: {list(NODE_CLASS_MAPPINGS.keys())}")

WEB_DIRECTORY = "./web"
__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS'] 