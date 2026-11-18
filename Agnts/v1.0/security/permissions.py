class PermissionManager:
    def __init__(self, allowed_tools=None):
        self.allowed_tools = set(allowed_tools or [])

    def is_allowed(self, tool_name):
        return tool_name in self.allowed_tools
