import os

import pandas as pd
import scipy as sp
import matplotlib.pyplot as plt

from pathlib import Path
data_path = Path("data/")
output = Path("output/")


def answer(func):
    try:
        counter = answer.cache[func.__name__]
    except AttributeError:
        answer.cache = {func.__name__: 1}
        counter = 1
    except KeyError:
        counter = len(answer.cache) + 1
        answer.cache[func.__name__] = counter


    output_file = output/(str(counter).zfill(2) + "_" + func.__name__ + ".dat")
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    def wrapped():
        with open(output_file, "w") as f:
            func(f)

        print(f"*** OUTPUT ({output_file}) ***")
        with open(output_file, "r") as f:
            print(f.read())
    return wrapped
