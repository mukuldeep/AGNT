from llm.interface import LLMInterface

class OpenAIAdapter(LLMInterface):
    """Optional extension point. Install/configure an API client before implementing."""
    def __init__(self, *args, **kwargs):
        raise NotImplementedError(
            "This Colab project uses LocalQwenAdapter. Implement this adapter only "
            "if you later want a hosted OpenAI-compatible endpoint."
        )
    def generate(self, prompt: str) -> str:
        raise NotImplementedError
