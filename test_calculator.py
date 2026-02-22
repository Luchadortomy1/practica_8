import os
import sys
import pathlib
import importlib.util
import pytest

def _find_src_dir() -> pathlib.Path | None:
    here = pathlib.Path(__file__).resolve()
    cwd = pathlib.Path.cwd()
    workspace_env = os.environ.get("GITHUB_WORKSPACE")
    workspace = pathlib.Path(workspace_env).resolve() if workspace_env else None

    bases = []
    bases.extend([here.parent, *here.parents])
    bases.extend([cwd, *cwd.parents])
    if workspace:
        bases.extend([workspace, *workspace.parents])

    seen: set[str] = set()
    candidates: list[pathlib.Path] = []

    for base in bases:
        key = str(base)
        if key in seen:
            continue
        seen.add(key)
        candidates.append(base / "src" / "main.py")
        # Also consider nested repo folders one level down
        candidates.extend(base.glob("*/src/main.py"))

    for main_path in candidates:
        if main_path.exists():
            return main_path.parent

    # As a last resort, search recursively under likely roots
    search_roots = []
    if workspace:
        search_roots.append(workspace)
    search_roots.append(cwd)
    for root in search_roots:
        for main_path in root.rglob("src/main.py"):
            return main_path.parent
    return None

SRC_DIR = _find_src_dir()

if SRC_DIR is None:
    raise RuntimeError("Could not locate src/main.py for imports")

# Ensure the src directory is on sys.path
sys.path.insert(0, str(SRC_DIR.parent))

try:
    from src.main import Calculator
except ModuleNotFoundError:
    # Fallback: load main.py directly
    main_path = SRC_DIR / "main.py"
    spec = importlib.util.spec_from_file_location("src.main", main_path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader  # guard for type checkers
    spec.loader.exec_module(module)
    Calculator = module.Calculator


def test_sum():
    assert Calculator().sum(2, 2) == 4


def test_subtract():
    assert Calculator().subtract(5, 3) == 2


def test_multiply():
    assert Calculator().multiply(3, 4) == 12


def test_divide():
    assert Calculator().divide(10, 2) == 5


def test_divide_by_zero():
    with pytest.raises(ValueError):
        Calculator().divide(10, 0)
