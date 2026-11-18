import sqlite3

class Database:
    def __init__(self, path="agent_memory.sqlite"):
        self.path = path

    def _connect(self):
        return sqlite3.connect(self.path)

    def initialize(self):
        with self._connect() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS memories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    query TEXT NOT NULL,
                    answer TEXT NOT NULL
                )
            """)

    def insert_memory(self, query, answer):
        with self._connect() as conn:
            conn.execute("INSERT INTO memories(query, answer) VALUES (?, ?)", (query, answer))

    def search_memory(self, query, limit=3):
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT query, answer FROM memories WHERE query LIKE ? ORDER BY id DESC LIMIT ?",
                (f"%{query}%", limit)
            ).fetchall()
        return [{"query": q, "answer": a} for q, a in rows]
