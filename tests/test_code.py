import os
import csv
import random
import time
import os

from src.router import router


SAMPLE_SIZE = 10


def test_correctness(dataset):
    dataset_sample = random.sample(dataset, SAMPLE_SIZE)
    errors = []
    for row in dataset_sample:
        query = row[0]
        expected_topic = int(row[1])
        predicted_topic = router(query)
        time.sleep(1)
        if expected_topic != predicted_topic:
            errors.append(f"Для запроса \"{query}\" ожидалось {expected_topic}, получено {predicted_topic}")
    assert len(errors) == 0, "\n".join(errors)


def test_reliability(dataset):
    row = dataset[0]
    query = row[0]
    result1 = router(query)
    time.sleep(1)
    result2 = router(query)
    time.sleep(1)
    assert result1 == result2, f"Результат детекции не стабилен для запроса \"{query}\""
