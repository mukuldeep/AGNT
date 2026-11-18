class Controller:
    def __init__(self, tools, permissions, validator):
        self.tools = tools
        self.permissions = permissions
        self.validator = validator

    def execute(self, action):
        valid, message = self.validator(action)
        if not valid:
            return {"ok": False, "error": message}
        name = action["tool"]
        if not self.permissions.is_allowed(name):
            return {"ok": False, "error": f"Permission denied for tool: {name}"}
        try:
            result = self.tools.call(name, **action.get("arguments", {}))
            return {"ok": True, "tool": name, "result": result}
        except Exception as exc:
            return {"ok": False, "tool": name, "error": str(exc)}
