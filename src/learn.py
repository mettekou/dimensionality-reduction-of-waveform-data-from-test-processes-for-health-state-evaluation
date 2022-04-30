import numpy as np
import pandas as pd
from sklearn.preprocessing import scale
from sklearn.linear_model import LogisticRegressionCV
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


def logistic_regression(data: pd.DataFrame):
    # quantity_train, quantity_test, failure_train, failure_test = train_test_split(
    #    , , test_size=0.5, random_state=0)
    clf = LogisticRegressionCV(max_iter=1000)
    clf.fit(data.select_dtypes(
        include=["float64"]).apply(scale), data.loc[:, 'ok'])
    coefficients = pd.concat(
        [pd.DataFrame(data.select_dtypes(
            include=["float64"]).columns), pd.DataFrame(np.transpose(clf.coef_))], axis=1)
    return coefficients
