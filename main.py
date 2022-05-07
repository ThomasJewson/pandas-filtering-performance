# %%
import pandas as pd
import numpy as np
from tqdm import tqdm
import seaborn as sns
import matplotlib.pyplot as plt

from utils import run_time, generate_random_data, convert_to_df


class Filters:
    @run_time
    def standard(df: pd.DataFrame, *, num_of_reps: int = 1):
        df[(df["cat_0"] == "bar") & (df["num_0"] < 0.5)]

    @run_time
    def loc(df: pd.DataFrame, *, num_of_reps: int = 1):
        df.loc[(df["cat_0"] == "bar") & (df["num_0"] < 0.5)]

    @run_time
    def mask(df: pd.DataFrame, *, num_of_reps: int = 1):
        mask = (df["cat_0"] == "bar") & (df["num_0"] < 0.5)
        df[mask]

    @run_time
    def mask_loc(df: pd.DataFrame, *, num_of_reps: int = 1):
        mask = (df["cat_0"] == "bar") & (df["num_0"] < 0.5)
        df.loc[mask]

    @run_time
    def mask_values_loc(df: pd.DataFrame, *, num_of_reps: int = 1):
        mask = (df["cat_0"].values == "bar") & (df["num_0"].values < 0.5)
        df.loc[mask]

    @run_time
    def where(df: pd.DataFrame, *, num_of_reps: int = 1):
        df.loc[np.where((df["cat_0"] == "bar") & (df["num_0"] < 0.5))]

    @run_time
    def query(df: pd.DataFrame, *, num_of_reps: int = 1):
        df.query("`cat_0` == 'bar' and `num_0` < 0.5")

    @run_time
    def values_where(df: pd.DataFrame, *, num_of_reps: int = 1):
        df.loc[np.where((df["cat_0"].values == "bar") & (df["num_0"].values < 0.5))]


def calc_run_times(Filters, max_length_of_test_data, step, num_of_repetitions):
    _func_times = {}
    for length in tqdm(range(0, max_length_of_test_data, step)):
        df = generate_random_data(2, length)
        _func_times[length] = [
            Filters.standard(df, num_of_reps=num_of_repetitions),
            Filters.loc(df, num_of_reps=num_of_repetitions),
            Filters.mask(df, num_of_reps=num_of_repetitions),
            Filters.mask_loc(df, num_of_reps=num_of_repetitions),
            Filters.mask_values_loc(df, num_of_reps=num_of_repetitions),
            Filters.query(df, num_of_reps=num_of_repetitions),
            Filters.where(df, num_of_reps=num_of_repetitions),
            Filters.values_where(df, num_of_reps=num_of_repetitions),
        ]

    return _func_times


class Config:
    MAX_LENGTH = 10_000_000
    STEP = 5_000_000
    NUM_OF_REPS = 5


def main():
    func_times = calc_run_times(
        Filters, Config.MAX_LENGTH, Config.STEP, Config.NUM_OF_REPS
    )

    entries = (
        convert_to_df(func_times)
        .reset_index()
        .melt(id_vars="index")
        .explode("value")
        .reset_index(drop=True)
    )

    entries.to_csv(
        f"output/entries_{str(Config.NUM_OF_REPS)}_{str(int(Config.MAX_LENGTH/Config.STEP))}_{str(Config.MAX_LENGTH)}.csv"
    )

    sns.lineplot(x="index", y="value", style="variable", hue="variable", data=entries)


if __name__ == "__main__":
    main()