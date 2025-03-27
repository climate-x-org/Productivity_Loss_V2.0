# tests/test_assets_csv.py
import pytest
import sys
import os
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src import validation


def test_assets_csv_validation():
    file_path = "data/test_assets.csv"
    try:
        # Validate the CSV file using the custom function.
        df = validation.validate_csv(file_path)
    except Exception as e:
        pytest.fail(f"Validation of {file_path} failed with error: {e}")
