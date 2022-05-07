# %%
import pandas as pd
from tqdm import tqdm

from utils import run_time, generate_random_data

"""
Simple filtering with .loc or not
Simple filtering via .values
Set_index then filter
Query
Np.where / np based filtering
"""


@run_time
def standard_filtering(df: pd.DataFrame, *, num_of_reps: int = 1):
    df[(df["cat_0"] == "bar") & (df["num_0"] < 0.5)]


@run_time
def standard_filtering_with_loc(df: pd.DataFrame, *, num_of_reps: int = 1):
    df.loc[(df["cat_0"] == "bar") & (df["num_0"] < 0.5)]


@run_time
def standard_filtering_via_mask(df: pd.DataFrame, *, num_of_reps: int = 1):
    mask = (df["cat_0"] == "bar") & (df["num_0"] < 0.5)
    df[mask]


@run_time
def standard_filtering_via_mask_and_loc(df: pd.DataFrame, *, num_of_reps: int = 1):
    mask = (df["cat_0"] == "bar") & (df["num_0"] < 0.5)
    df.loc[mask]


MAX_LENGTH = 100_000
STEP = 10_000
NUM_OF_REPS = 10
func_times = {}
for length in tqdm(range(0, MAX_LENGTH, STEP)):
    df = generate_random_data(2, length)
    func_times[length] = [
        standard_filtering(df, num_of_reps=NUM_OF_REPS),
        standard_filtering_with_loc(df, num_of_reps=NUM_OF_REPS),
    ]

print("DONE")
