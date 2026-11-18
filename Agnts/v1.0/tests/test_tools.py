import unittest
from tools.calculator import calculate
from tools.registry import ToolRegistry

class ToolTests(unittest.TestCase):
    def test_calculator(self):
        self.assertEqual(calculate("2 + 3 * 4"), 14)

    def test_calculator_rejects_code(self):
        with self.assertRaises(Exception):
            calculate("__import__('os').system('echo unsafe')")

    def test_registry(self):
        registry = ToolRegistry()
        registry.register("double", lambda x: x * 2)
        self.assertEqual(registry.call("double", x=4), 8)

if __name__ == "__main__":
    unittest.main()
