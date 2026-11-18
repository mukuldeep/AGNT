class RetrievalMemory:
    """Minimal SQLite-backed exact/substring retrieval, not vector search."""
    def __init__(self, database):
        self.db = database

    def add(self, query, answer):
        self.db.insert_memory(query, answer)

    def search(self, query, limit=3):
        return self.db.search_memory(query, limit)
