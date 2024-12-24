class RunningHubNodeInfoNode:
    """Node for creating individual nodeInfo entries"""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "node_id": ("STRING", {"default": ""}),
                "field_name": ("STRING", {"default": ""}),
                "comment": ("STRING", {"default": ""}),
                "field_value": ("STRING", {"default": "", "multiline": True}),
            }
        }

    RETURN_TYPES = ("NODEINFO",)
    FUNCTION = "create_node_info"
    CATEGORY = "🌻 Addoor/RHAPI"

    def create_node_info(self, node_id: str, field_name: str, comment: str, field_value: str):
        node_info = {
            "nodeId": node_id,
            "fieldName": field_name,
            "fieldValue": field_value
        }
        return (node_info,)

