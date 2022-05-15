# %%
from timeit import timeit
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from utils import generate_random_data


def get_agg(filepath: str) -> pd.DataFrame:
    _df = pd.read_csv(filepath, index_col="Unnamed: 0")
    df_agg = _df.groupby(["variable", "Length of DataFrame"]).agg(
        {"Time (s)": [np.mean, np.std]}
    )
    df_agg.columns = [" ".join(col) for col in df_agg.columns]
    return df_agg


def line_graph(_df_agg: pd.DataFrame):
    _df_agg.reset_index()
    sns.set_style("darkgrid")
    sns.lineplot(
        x="Length of DataFrame",
        y="Time (s) mean",
        # style="variable",
        hue="variable",
        data=_df_agg.reset_index(),
    )
# %% Generating random data
df = generate_random_data(1,1_000_000)
df
# %% Standard with Loc
%%timeit
df.loc[(df["cat_0"] == "bar") & (df["num_0"] < 0.5)]
# %% Standard
%%timeit
df[(df["cat_0"] == "bar") & (df["num_0"] < 0.5)]
# %% Standard with mask
%%timeit
mask = (df["cat_0"].values == "bar") & (df["num_0"].values < 0.5)
df[mask]
# %% Standard with values
%%timeit
df[(df["cat_0"].values == "bar") & (df["num_0"].values < 0.5)]
# %% numpy.where with values
%%timeit
df.loc[np.where((df["cat_0"].values == "bar") & (df["num_0"].values < 0.5))]
# %% Query
%%timeit
df.query("`cat_0` == 'bar' and `num_0` < 0.5")

# %%
# Files to use:
# output\entries_20_10_100000000.csv
# output\entries_120_25_250000.csv
import matplotlib.style as style

long = pd.read_csv(R"output\entries_20_10_100000000.csv", index_col="Unnamed: 0")
short = pd.read_csv(R"output\entries_120_25_250000.csv", index_col="Unnamed: 0")
style.use('seaborn-poster') #sets the size of the charts
style.use('ggplot')

def change_names(inp_str):
    if inp_str == "values_where":
        return "np.where"
    if inp_str == "query":
        return ".query"
    if inp_str == "standard_values":
        return "standard with .values"
    return inp_str

short["variable"] = short["variable"].apply(change_names)
long["variable"] = long["variable"].apply(change_names)

sns.lineplot(
    x="Length of DataFrame",
    y="Time (s)",
    style="variable",
    hue="variable",
    data=long,
)
# %%
sns.lineplot(
    x="Length of DataFrame",
    y="Time (s)",
    style="variable",
    hue="variable",
    data=short,
)