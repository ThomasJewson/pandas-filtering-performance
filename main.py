# %%
import pandas as pd
from tqdm import tqdm

from utils import run_time, generate_random_data


@run_time
def countdown(n, *, num_of_reps: int = 1):
    while n > 0:
        n -= 1


@run_time
def basic_filter(df, *, num_of_reps: int = 1):
    df[(df["cat_0"] == "bar") & (df["num_0"] < 0.5)]


MAX_LENGTH = 100_000
STEP = 10_000
NUM_OF_REPS = 10
func_times = {}
for length in tqdm(range(0, MAX_LENGTH, STEP)):
    df = generate_random_data(2, length)
    func_times[length] = [basic_filter(df, num_of_reps=NUM_OF_REPS)]

func_times
