# %%
import pandas as pd
import numpy as np
from tqdm import tqdm
import seaborn as sns

# %%
"""
1. Categorical columns
2. Numerical columns
"""
# %%
WIDTH = 3
LENGTH = 100000


def generate_random_data(_width, _length):
    cats = pd.DataFrame(
        np.random.choice(["foo", "bar", "baz"], size=(_length, _width)),
        columns=["cat_" + str(idx) for idx in range(_width)],
    )
    nums = pd.DataFrame(
        np.random.rand(_length, _width),
        columns=["num_" + str(idx) for idx in range(_width)],
    )
    return pd.concat([cats, nums], axis=1)


generate_random_data(WIDTH, LENGTH)


# %%
from timeit import default_timer as timer, timeit

df = generate_random_data(3, 100)
# %%
def basic_filter_time(df):
    start = timer()
    df[(df["cat_0"] == "bar") & (df["num_0"] < 0.5)]
    end = timer()
    return end - start


basic_filter_time(df)
# %%
def basic_query_time(df):
    start = timer()
    df.query("`cat_0` == 'bar' and `num_0` < 0.5")
    end = timer()
    return end - start


basic_query_time(df)

# %%
def repeat(num_of_reps, function, df):
    return [function(df) for _ in range(num_of_reps)]


def repeat_over_log_len_spread(
    num_of_reps, function_1, function_2, df, max_val, num_splits
):
    out = []
    idx = []
    # range_space = np.geomspace(1, max_val, num_splits)
    range_space = np.linspace(1, max_val, num_splits)
    for length in tqdm(range_space):
        length = int(length)
        df = generate_random_data(1, length)
        func_1_times = repeat(num_of_reps, function_1, df)
        func_2_times = repeat(num_of_reps, function_2, df)
        out.append([func_1_times, func_2_times])
        idx.append(length)
    return pd.DataFrame(out, columns=["func_1", "func_2"], index=idx)


out = repeat_over_log_len_spread(
    25, basic_filter_time, basic_query_time, df, 10_000_000, 5
)
# %%
def mean_times(times: list):
    return np.mean(times)


avgs = out.applymap(mean_times)

melted = out.reset_index().melt(id_vars="index").explode("value").reset_index(drop=True)
sns.lineplot(x="index", y="value", style="variable", data=melted)
# %%
