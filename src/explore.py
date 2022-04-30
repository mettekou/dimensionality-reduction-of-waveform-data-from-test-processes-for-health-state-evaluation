import pandas as pd


def bivariate(data: pd.DataFrame):
    return pd.plotting.scatter_matrix(data.select_dtypes(include=["float64"]))
