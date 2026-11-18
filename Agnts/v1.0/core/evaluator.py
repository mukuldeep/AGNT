class Evaluator:
    """Small deterministic evaluator: validates terminal action and iteration budget."""
    def is_complete(self, action, step, max_steps):
        if step >= max_steps:
            return True
        return action.get("type") == "final"

    def stop_reason(self, step, max_steps):
        return f"Stopped after reaching the {max_steps}-step execution limit."
