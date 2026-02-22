import pytest
from main import Calculator

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
