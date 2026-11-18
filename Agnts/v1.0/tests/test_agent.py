import unittest
from core.agent import Agent
from tools.registry import ToolRegistry
from security.permissions import PermissionManager
from security.validator import validate_action
from memory.working_memory import WorkingMemory
from memory.conversation import ConversationMemory
from memory.retrieval import RetrievalMemory

class FakeLLM:
    def __init__(self):
        self.actions = [
            '{"type":"tool","tool":"calculator","arguments":{"expression":"6*7"},"reason":"calculate"}',
            '{"type":"final","answer":"The answer is 42."}'
        ]
    def generate(self, prompt):
        return self.actions.pop(0)

class FakeDB:
    def insert_memory(self, q, a): pass
    def search_memory(self, q, limit=3): return []

class AgentTests(unittest.TestCase):
    def test_tool_then_final(self):
        registry = ToolRegistry()
        from tools.calculator import calculate
        registry.register("calculator", calculate)
        agent = Agent(
            FakeLLM(), registry, PermissionManager({"calculator"}), validate_action,
            WorkingMemory(), ConversationMemory(), RetrievalMemory(FakeDB())
        )
        self.assertEqual(agent.run("What is 6 times 7?"), "The answer is 42.")

if __name__ == "__main__":
    unittest.main()
