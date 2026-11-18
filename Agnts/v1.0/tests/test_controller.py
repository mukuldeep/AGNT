import unittest
from core.controller import Controller
from tools.registry import ToolRegistry
from security.permissions import PermissionManager
from security.validator import validate_action

class ControllerTests(unittest.TestCase):
    def test_valid_tool_call(self):
        registry = ToolRegistry()
        registry.register("calculator", lambda expression: 4)
        controller = Controller(registry, PermissionManager({"calculator"}), validate_action)
        result = controller.execute({
            "type": "tool", "tool": "calculator",
            "arguments": {"expression": "2+2"}
        })
        self.assertTrue(result["ok"])
        self.assertEqual(result["result"], 4)

    def test_permission_denied(self):
        registry = ToolRegistry()
        registry.register("calculator", lambda expression: 4)
        controller = Controller(registry, PermissionManager(), validate_action)
        result = controller.execute({
            "type": "tool", "tool": "calculator",
            "arguments": {"expression": "2+2"}
        })
        self.assertFalse(result["ok"])

if __name__ == "__main__":
    unittest.main()
