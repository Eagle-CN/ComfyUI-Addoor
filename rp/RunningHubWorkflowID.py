class RunningHubWorkflowIDNode:
    """Node for inputting RunningHub workflow ID"""
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "workflow_id": ("STRING", {"default": "", "multiline": False}),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    FUNCTION = "set_workflow_id"
    CATEGORY = "🌻 Addoor/RHAPI"
    
    def set_workflow_id(self, workflow_id: str):
        if not workflow_id.strip():
            raise ValueError("Workflow ID cannot be empty")
        return (workflow_id,)

