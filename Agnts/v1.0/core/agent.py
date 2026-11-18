from core.context import AgentContext
from core.planner import Planner
from core.controller import Controller
from core.evaluator import Evaluator

class Agent:
    def __init__(self, llm, tools, permissions, validator,
                 working_memory, conversation, retrieval, max_steps=5):
        self.llm = llm
        self.planner = Planner()
        self.controller = Controller(tools, permissions, validator)
        self.evaluator = Evaluator()
        self.working_memory = working_memory
        self.conversation = conversation
        self.retrieval = retrieval
        self.max_steps = max_steps

    def run(self, user_input):
        context = AgentContext(user_input=user_input)
        recalled = self.retrieval.search(user_input)
        if recalled:
            context.observations.append({"memory_recall": recalled})

        for step in range(1, self.max_steps + 1):
            context.step = step
            action = self.planner.plan(self.llm, context)

            if action.get("type") == "final":
                answer = str(action.get("answer", ""))
                self._remember(user_input, answer)
                self.conversation.add("user", user_input)
                self.conversation.add("assistant", answer)
                return answer

            if action.get("type") != "tool":
                context.observations.append({"ok": False, "error": "Unknown action type."})
                continue

            observation = self.controller.execute(action)
            context.observations.append(observation)
            self.working_memory.add({"step": step, "action": action, "observation": observation})

        answer = self.evaluator.stop_reason(self.max_steps, self.max_steps)
        self._remember(user_input, answer)
        return answer

    def _remember(self, question, answer):
        self.retrieval.add(question, answer)
