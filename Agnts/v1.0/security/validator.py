TOOL_FIELDS = {
    "calculator": {"expression"},
    "search": {"query"},
    "read_file": {"path"},
    "write_file": {"path", "content"},
}

def validate_action(action):
    if not isinstance(action, dict):
        return False, "Action must be a JSON object."
    if action.get("type") == "final":
        return isinstance(action.get("answer"), str), "Final action needs a string answer."
    if action.get("type") != "tool":
        return False, "Action type must be 'tool' or 'final'."
    tool = action.get("tool")
    if tool not in TOOL_FIELDS:
        return False, f"Tool not allowed: {tool}"
    args = action.get("arguments")
    if not isinstance(args, dict):
        return False, "Tool arguments must be an object."
    required = TOOL_FIELDS[tool]
    if set(args) != required:
        return False, f"{tool} requires exactly these arguments: {sorted(required)}"
    if not all(isinstance(v, str) for v in args.values()):
        return False, "All tool arguments must be strings."
    return True, "OK"
