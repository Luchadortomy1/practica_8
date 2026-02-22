import os
import sys
import pathlib
import importlib.util
import pytest

# Ensure imports work whether tests run from repo root or inside src
ROOT = pathlib.Path(__file__).resolve().parent
REPO_ROOT = ROOT if (ROOT / "src").exists() else ROOT.parent
sys.path.insert(0, str(REPO_ROOT))

try:
    from src.main import Calculator
except ModuleNotFoundError:
    # Fallback: load directly from file if src is not on sys.path in CI
    candidate = (REPO_ROOT / "src" / "main.py").resolve()
    spec = importlib.util.spec_from_file_location("src.main", candidate)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader  # mypy/pyright guard
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
