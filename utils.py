# %%
from timeit import default_timer as timer
import numpy as np
import pandas as pd


def generate_random_data(width, length, **kwargs):
    cats = pd.DataFrame(
        np.random.choice(["foo", "bar", "baz"], size=(length, width)),
        columns=["cat_" + str(idx) for idx in range(width)],
    )
    nums = pd.DataFrame(
        np.random.rand(length, width),
        columns=["num_" + str(idx) for idx in range(width)],
    )
    return pd.concat([cats, nums], axis=1)


def run_time(func):
    def wrapper(*args, **kwargs):
        if "num_of_reps" not in kwargs:
            kwargs["num_of_reps"] = 1

        times = np.empty(kwargs["num_of_reps"])

        for rep in range(kwargs["num_of_reps"]):
            start_time = timer()
            func(*args, **kwargs)
            end_time = timer()
            times[rep] = end_time - start_time
        return {func.__name__: times}

    return wrapper


@run_time
def countdown(n, *, num_of_reps: int = 1):
    while n > 0:
        n -= 1


@run_time
def basic_filter(df, *, num_of_reps: int = 1):
    df[(df["cat_0"] == "bar") & (df["num_0"] < 0.5)]


df = generate_random_data(2, 100)
basic_filter(df, num_of_reps=10)
