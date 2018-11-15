import os
import inspect

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

    func_args = inspect.signature(func).parameters
    try:
        file_num = func_args["fout"].default
        file_num = 1 if file_num == inspect.Signature.empty else file_num
    except KeyError:
        file_num = 1

    def get_filenames():
        output_file = output/(str(counter).zfill(2) + "_" + func.__name__ + "{}.dat")
        output_file = str(output_file)

        if file_num > 1:
            return [output_file.format(f"-{i}") for i in range(1, file_num+1)]
        else:
            return [output_file.format("")]

    file_names = get_filenames()
    os.makedirs(os.path.dirname(file_names[0]), exist_ok=True)

    def wrapped():
        files = []

        for fname in file_names:
            f = open(fname, "w")
            files.append(f)

        if len(files) == 1:
            func(files[0])
        else:
            func(fout=files)

        for f in files:
            f.close()

        for fname in file_names:
            print(f"*** OUTPUT ({fname}) ***")
            with open(fname, "r") as f:
                print(f.read())
    return wrapped
