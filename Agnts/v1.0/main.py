from llm.local_adapter import LocalQwenAdapter
from tools.registry import ToolRegistry
from tools.calculator import calculate
from tools.search import search
from tools.filesystem import read_text, write_text
from security.permissions import PermissionManager
from security.validator import validate_action
from memory.working_memory import WorkingMemory
from memory.conversation import ConversationMemory
from memory.retrieval import RetrievalMemory
from storage.database import Database
from core.agent import Agent

def build_agent(model_name="Qwen/Qwen2.5-1.5B-Instruct"):
    llm = LocalQwenAdapter(model_name=model_name)
    tools = ToolRegistry()
    tools.register("calculator", calculate, "Evaluate a basic arithmetic expression.")
    tools.register("search", search, "Search the web (demo stub; replace with a search API).")
    tools.register("read_file", read_text, "Read a text file inside the workspace.")
    tools.register("write_file", write_text, "Write a text file inside the workspace.")

    permissions = PermissionManager(allowed_tools={"calculator", "search", "read_file", "write_file"})
    db = Database("agent_memory.sqlite")
    db.initialize()
    return Agent(
        llm=llm, tools=tools, permissions=permissions,
        validator=validate_action,
        working_memory=WorkingMemory(),
        conversation=ConversationMemory(),
        retrieval=RetrievalMemory(db),
    )

if __name__ == "__main__":
    agent = build_agent()
    print("Qwen Agent ready. Type 'exit' to stop.")
    while True:
        try:
            user_input = input("\nYou: ").strip()
            if user_input.lower() in {"exit", "quit"}:
                break
            if user_input:
                print("\nAgent:", agent.run(user_input))
        except KeyboardInterrupt:
            print("\nExiting.")
            break
