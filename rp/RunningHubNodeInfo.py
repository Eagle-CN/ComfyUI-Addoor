class RunningHubNodeInfoNode:
    """Node for creating and chaining nodeInfo entries"""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "node_id": ("STRING", {"default": ""}),
                "field_name": ("STRING", {"default": ""}),
                "field_value": ("STRING", {"default": "", "multiline": True}),
                "comment": ("STRING", {"default": ""}),
            },
            "optional": {
                "previous_node_info": ("NODEINFOLIST",),  # 用于串联
            }
        }

    RETURN_TYPES = ("NODEINFOLIST",)  # 改为返回列表类型
    FUNCTION = "create_node_info"
    CATEGORY = "🌻 Addoor/RHAPI"

    def create_node_info(self, node_id: str, field_name: str, field_value: str, comment: str, previous_node_info=None):
        # 创建当前节点信息
        current_node_info = {
            "nodeId": node_id,
            "fieldName": field_name,
            "fieldValue": field_value,
            "comment": comment
        }
        
        # 初始化节点信息列表
        node_info_list = []
        
        # 如果有前置节点信息，添加到列表
        if previous_node_info is not None:
            if isinstance(previous_node_info, list):
                node_info_list.extend(previous_node_info)
            else:
                node_info_list.append(previous_node_info)
        
        # 添加当前节点信息
        node_info_list.append(current_node_info)
        
        return (node_info_list,)

