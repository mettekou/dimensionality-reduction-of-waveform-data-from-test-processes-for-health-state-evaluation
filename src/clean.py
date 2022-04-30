import numpy as np
import pandas as pd


def clean(data: pd.DataFrame):
    return data.drop(columns=["Maximum_pressure_hysteresis_current_point", "Maximum_current_hysteresis", "Maximum_current_hysteresis_pressure_point",
                              "Maximum_current_hysteresis_pressure_point_0,1-32bar", "Maximum_pressure_hysteresis",
                              "Rising_current_at_0bar", "Maximum_current_hysteresis_pressure_point_0-32bar", "Maximum_current_hysteresis_pressure_point_0,5-32bar"]).replace([np.inf, -np.inf], np.nan).dropna()
