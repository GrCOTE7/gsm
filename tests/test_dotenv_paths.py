"""Guard: python-dotenv must always be given an explicit .env path.

`load_dotenv()` without a path calls `find_dotenv()`, which walks the call stack
until it finds a frame whose file exists on disk. In a Serious Python Android
build the stack only contains build-machine paths (`/home/runner/...`,
`<sp_script>`) that do not exist on the device, so the walk exhausts every frame
and raises `AssertionError` — the app died at startup that way.
"""

import ast
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "src"


def _python_files():
    for path in SRC.rglob("*.py"):
        if "__pycache__" in path.parts:
            continue
        yield path


def test_dotenv_calls_always_pass_a_path():
    offenders = []
    for path in _python_files():
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            func = node.func
            name = (
                func.attr
                if isinstance(func, ast.Attribute)
                else getattr(func, "id", "")
            )
            if name not in {"load_dotenv", "find_dotenv"}:
                continue
            if not node.args and not node.keywords:
                offenders.append(f"{path.relative_to(SRC.parent)}:{node.lineno}")

    assert not offenders, (
        "load_dotenv()/find_dotenv() called without a path (raises AssertionError "
        f"in the Android build): {offenders}"
    )
