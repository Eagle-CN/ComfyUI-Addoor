class RunningHubNodeInfoCollectorNode:
    """Node for collecting multiple nodeInfo entries"""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "node_info_1": ("NODEINFO",),
            },
            "optional": {
                "node_info_2": ("NODEINFO",),
                "node_info_3": ("NODEINFO",),
                "node_info_4": ("NODEINFO",),
                "node_info_5": ("NODEINFO",),
            }
        }

    RETURN_TYPES = ("NODEINFOLIST",)
    FUNCTION = "collect_node_info"
    CATEGORY = "🌻 Addoor/RHAPI"

    def collect_node_info(self, node_info_1, node_info_2=None, node_info_3=None, node_info_4=None, node_info_5=None):
        node_info_list = [node_info_1]
        for node_info in [node_info_2, node_info_3, node_info_4, node_info_5]:
            if node_info is not None:
                node_info_list.append(node_info)
        return (node_info_list,)

