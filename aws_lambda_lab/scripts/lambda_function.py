import numpy as np


def lambda_handler(event: dict, context):
    sum_array = np.array([1, 2, 3]) + np.array([7, 6, 5])
    print(sum_array)
    return event
