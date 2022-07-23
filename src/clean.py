import numpy as np
import pandas as pd


def clean(data: pd.DataFrame):
    return data.replace([np.inf, -np.inf], np.nan).dropna()
