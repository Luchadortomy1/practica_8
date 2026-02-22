import sys
import pathlib
import importlib.util
import pytest

# Try a list of candidate src directories and use the first that exists.
HERE = pathlib.Path(__file__).resolve()
cwd = pathlib.Path.cwd()

src_candidates = []

# From the test file location and its parents
for parent in [HERE.parent, *HERE.parents]:
    src_candidates.append(parent / "src")

# From the working directory and its parents
for parent in [cwd, *cwd.parents]:
    src_candidates.append(parent / "src")

SRC_DIR = next((p for p in src_candidates if (p / "main.py").exists()), None)

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
