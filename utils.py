from timeit import default_timer as timer
import numpy as np
import pandas as pd


def generate_random_data(width: int, length: int) -> pd.DataFrame:
    """Generates DataFrame determined width and length of categorical and numeric values.

    Args:
        width (int): Width of DataFrame. EG: Number of categorical and numeric column
        length (int): Length of DataFrame.

    Returns:
        pd.DataFrame: Number of columns 2 * width due to categorical and numeric columns.
    """
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
    """Decorator which calculates the run time of a given function."""

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


def convert_to_df(_func_times: dict) -> pd.DataFrame:
    """Converts dictionary of function run times to a DataFrame

    Args:
        _func_times (dict): Output from calc_run_times function

    Returns:
        pd.DataFrame:
    """

    def remove_dict(cell: dict):
        try: # EAFP
            return list(cell.values())[0]
        except AttributeError:
            return

    def get_cols_from_keys(cell: dict):
        try:  # EAFP
            return list(cell.keys())[0]
        except AttributeError:
            return

    _df = pd.DataFrame().from_records(_func_times).T
    first_row = _df.iloc[0]
    _df.columns = first_row.apply(get_cols_from_keys).to_list()
    return _df.applymap(remove_dict)
