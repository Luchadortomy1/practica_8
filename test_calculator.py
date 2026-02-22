import sys
import pathlib
import importlib.util
import pytest

# Robustly locate the project root that contains src/main.py, even if the
# runner executes tests from a different working directory.
HERE = pathlib.Path(__file__).resolve()
PROJECT_ROOT = None

# First, search upward from the test file location.
for parent in [HERE.parent, *HERE.parents]:
    if (parent / "src" / "main.py").exists():
        PROJECT_ROOT = parent
        break

# If not found (e.g., when the runner relocates the test file), search from CWD.
if PROJECT_ROOT is None:
    cwd = pathlib.Path.cwd()
    for parent in [cwd, *cwd.parents]:
        if (parent / "src" / "main.py").exists():
            PROJECT_ROOT = parent
            break

if PROJECT_ROOT is None:
    raise RuntimeError("Could not locate src/main.py relative to tests or cwd")

# Ensure the project root is first on sys.path so `import src.main` works.
sys.path.insert(0, str(PROJECT_ROOT))

try:
    from src.main import Calculator
except ModuleNotFoundError:
    # Absolute import failed; load directly from the located file.
    main_path = PROJECT_ROOT / "src" / "main.py"
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
