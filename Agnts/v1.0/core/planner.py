import json
import re

SYSTEM_PROMPT = """You are the decision-making component of a small tool-using AI agent.
Choose exactly one action per turn. Available tools:
- calculator(expression: string)
- search(query: string)
- read_file(path: string)
- write_file(path: string, content: string)

Return ONLY one JSON object, with one of these forms:
{"type":"tool","tool":"calculator","arguments":{"expression":"2+2"},"reason":"..."}
{"type":"tool","tool":"search","arguments":{"query":"..."},"reason":"..."}
{"type":"tool","tool":"read_file","arguments":{"path":"notes.txt"},"reason":"..."}
{"type":"tool","tool":"write_file","arguments":{"path":"notes.txt","content":"..."},"reason":"..."}
{"type":"final","answer":"..."}

Use tool results as evidence. Do not claim a tool succeeded unless its observation says so.
If no tool is needed, return a final answer. Never output markdown fences."""

class Planner:
    def plan(self, llm, context):
        prompt = self._build_prompt(context)
        raw = llm.generate(prompt)
        return self._parse(raw)

    def _build_prompt(self, context):
        parts = [SYSTEM_PROMPT, f"\nUser task:\n{context.user_input}"]
        if context.history:
            parts.append("\nRecent conversation:\n" + "\n".join(
                f"{m['role']}: {m['content']}" for m in context.history[-8:]
            ))
        if context.observations:
            parts.append("\nTool observations:\n" + json.dumps(context.observations[-6:], ensure_ascii=False))
        parts.append("\nChoose the next action. JSON only:")
        return "\n".join(parts)

    def _parse(self, raw):
        # First try strict JSON; then extract the first JSON object if prose leaked in.
        try:
            obj = json.loads(raw)
        except json.JSONDecodeError:
            match = re.search(r"\{.*\}", raw, flags=re.S)
            if not match:
                return {"type": "final", "answer": raw.strip() or "I couldn't produce a response."}
            try:
                obj = json.loads(match.group(0))
            except json.JSONDecodeError:
                return {"type": "final", "answer": raw.strip()}
        if not isinstance(obj, dict):
            return {"type": "final", "answer": "The model returned an invalid action."}
        return obj
