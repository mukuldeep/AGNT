from pathlib import Path

WORKSPACE = Path("workspace").resolve()
WORKSPACE.mkdir(parents=True, exist_ok=True)

def _safe_path(path):
    candidate = (WORKSPACE / path).resolve()
    if candidate != WORKSPACE and WORKSPACE not in candidate.parents:
        raise PermissionError("Path must stay inside the workspace directory.")
    return candidate

def read_text(path: str):
    target = _safe_path(path)
    return target.read_text(encoding="utf-8")

def write_text(path: str, content: str):
    target = _safe_path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    return {"written": str(target.relative_to(WORKSPACE))}
