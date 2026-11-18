class ConversationMemory:
    def __init__(self):
        self.messages = []

    def add(self, role, content):
        self.messages.append({"role": role, "content": content})

    def recent(self, n=10):
        return self.messages[-n:]
