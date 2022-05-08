# %%
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


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


LONG_LOC = R"output\entries_20_4_100000000.csv"
SHORT_LOC = R"output\entries_50_50_100000.csv"
VERY_SHORT_LOC = R"output\entries_25_33_100000.csv"
# %%
line_graph(get_agg(LONG_LOC))
# %%
line_graph(get_agg(SHORT_LOC))

# %%
get_agg(SHORT_LOC)
# %%
sns.lmplot(
    x="Length of DataFrame",
    y="Time (s) mean",
    hue="variable",
    scatter_kws={"s": 1},
    data=get_agg(SHORT_LOC).reset_index(),
)
# %%
line_graph(get_agg(LONG_LOC))
# %%
get_agg(LONG_LOC)
# where + where and values
# Standard + loc + mask + mask & values
# Query
"""
Adding a mask to standard filtering (as a variable) speeds things up

Adding .loc sometimes speeds things up a bit. 
    Faster without a mask
    Slower with a mask

Mask values is the fastest, but it is the most cumbersome

For a small performance cost, you can use np.where as the filtering method
alonside values, this just a little slower than mask_values

Query is relativily slow on smaller data and it is around 20_000 when you 
should start using it. Bonus, is that it is very readable



"""
get_agg(LONG_LOC)
# %%
_length = 2000
get_agg(SHORT_LOC).reset_index().query("`Length of DataFrame` == @_length")
# %%
_length = 99000
get_agg(VERY_SHORT_LOC).reset_index().query("`Length of DataFrame` == @_length")
