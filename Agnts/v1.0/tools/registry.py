class ToolRegistry:
    def __init__(self):
        self._tools = {}

    def register(self, name, function, description=""):
        if name in self._tools:
            raise ValueError(f"Tool already registered: {name}")
        self._tools[name] = {"function": function, "description": description}

    def call(self, name, **kwargs):
        if name not in self._tools:
            raise KeyError(f"Unknown tool: {name}")
        return self._tools[name]["function"](**kwargs)

    def describe(self):
        return {name: item["description"] for name, item in self._tools.items()}

    def names(self):
        return list(self._tools)
