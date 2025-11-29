import pandas as pd


def load_csv(path, nrows=None):
    return pd.read_csv(path, parse_dates=['date'], nrows=nrows)
