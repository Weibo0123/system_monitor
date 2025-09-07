import pytest
from main import get_positive_int, check_and_warning, load_thresholds
import argparse

def test_get_postive_int():
    assert get_positive_int(10) == 10
    assert get_positive_int(0) == 0
    assert get_positive_int(100) == 100
    assert get_positive_int("80") == 80
    assert get_positive_int("75") == 75
    with pytest.raises(argparse.ArgumentTypeError):
        get_positive_int("-5")
    with pytest.raises(argparse.ArgumentTypeError):
        get_positive_int("120")
    with pytest.raises(argparse.ArgumentTypeError):
        get_positive_int("cat")


    
    

