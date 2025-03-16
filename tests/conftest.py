import os
import csv
import pytest


DATA_PATH = os.path.join(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "data.csv"))


@pytest.fixture
def dataset():
    with open(DATA_PATH, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        _ = next(reader) # skip header
        rows = list(reader)
    return rows
