import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import scale
from sklearn.linear_model import LogisticRegressionCV
from sklearn.metrics import (confusion_matrix, roc_curve, roc_auc_score, RocCurveDisplay)
import matrixprofile as mp
import matplotlib.pyplot as plt

independents = [  "CS_AvgFalSlp",
                  "CS_AvgPrsHyst_400_1200",
                  "CS_AvgRisSlp",
                  "CS_BlkTmp",
                  "CS_FalPrs_100",
                  "CS_FalSlpDev",
                  "CS_MaxAPrsRip",
                  "CS_MaxCurrHyst_0_32",
                  "CS_MaxPrsHyst_100_400",
                  "CS_MaxPrsHyst_1200_1500",
                  "CS_MaxPrsHyst_400_1200",
                  "CS_PPrs",
                  "CS_RisCurr_10",
                  "CS_RisCurr_100m",
                  "CS_RisCurr_20",
                  "CS_RisCurr_30",
                  "CS_RisCurr_800m",
                  "CS_RisPrs_1000",
                  "CS_RisPrs_1100",
                  "CS_RisPrs_1200",
                  "CS_RisPrs_1300",
                  "CS_RisPrs_1400",
                  "CS_RisPrs_300",
                  "CS_RisPrs_400",
                  "CS_RisPrs_500",
                  "CS_RisPrs_600",
                  "CS_RisPrs_700",
                  "CS_RisPrs_800",
                  "CS_RisPrs_900",
 "CS_RisSlpDev"
]

dependent_name = [ "ok" ]

def logistic_regression_forward(data: pd.DataFrame):
    available_independents = independents.copy()
    selected_independents = []
    better_model_found = True
    better_model = None
    better_model_bic = float('inf')
    scaled_data = data.select_dtypes(include=["float64"]).apply(scale)
    x_train, x_test, y_train, y_test = train_test_split(scaled_data, data.loc[:, dependent_name], test_size = 0.2, random_state=0)
    while better_model_found:
        models = {}
        bics = {}
        for independent in available_independents:
            models[independent] = sm.Logit(y_train, x_train[selected_independents + [independent]]).fit(method='lbfgs',maxiter=1000, disp=False)
            bics[independent] = models[independent].bic
        best_model_bic = min(bics.items(), key=lambda x:x[1])
        if best_model_bic[1] < better_model_bic:
            if len(selected_independents) > 0:
                vif = variance_inflation_factor(x_train[selected_independents + [best_model_bic[0]]], len(selected_independents))
                if vif <= 5:
                    better_model = models[best_model_bic[0]]
                    better_model_bic = best_model_bic[1]
                    selected_independents.append(best_model_bic[0])
            else:
                better_model = models[best_model_bic[0]]
                better_model_bic = best_model_bic[1]
                selected_independents.append(best_model_bic[0])
            available_independents.remove(best_model_bic[0])
        else:
            better_model_found = False
    return better_model
    #y_pred = better_model.predict(x_test[selected_independents])
    #RocCurveDisplay.from_predictions(y_test, y_pred)
    #plt.show()
    #return better_model#, confusion_matrix(y_test, y_pred)

def logistic_regression_lasso(data: pd.DataFrame):
    scaled_data = data.select_dtypes(include=["float64"]).apply(scale)
    x_train, x_test, y_train, y_test = train_test_split(scaled_data, data.loc[:, dependent_name], test_size = 0.2, random_state=0)
    model = LogisticRegressionCV(max_iter=10000,penalty="elasticnet",l1_ratios=[0.5,0.5],solver="saga",n_jobs=-1)
    model.fit(x_train, y_train.values.ravel())
    coefficients = pd.concat(
        [pd.DataFrame(data.select_dtypes(
            include=["float64"]).columns), pd.DataFrame(np.transpose(model.coef_))], axis=1)
    y_pred = model.decision_function(x_test)
    RocCurveDisplay.from_predictions(y_test.values.ravel(), y_pred)
    #plt.show()
    return coefficients

def logistic_regression_matrix_profile(x: np.ndarray, y: np.ndarray, window_size, k):
    #_, columns = np.shape(x)
    #failed_x = x[np.where(np.logical_not(y))]
    #passed_x = x[np.where(y)]
    #failed_x_1d = failed_x.flatten()
    #passed_x_1d = passed_x.flatten()
    #profile_failed = mp.compute(failed_x_1d, query = passed_x_1d, n_jobs = -1)
    #profile_passed = mp.compute(passed_x_1d, windows = 30000, n_jobs = -1)
    #mp.visualize(profile_failed)
    #plt.show()
    #print(mp.discover.motifs(profile_passed, exclusion_zone = 0))
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state=0)
    #motifs = {}
    discords = {}
    for row in range(np.shape(x_train)[0]):
        profile = mp.compute(x_train[row], windows = window_size, n_jobs = -1)
    #    for motif in mp.discover.motifs(profile, k = 1)["motifs"]:
    #        indices = motif["motifs"]
    #        for i in range(indices[0], indices[1] + 1):
    #            motifs[i] = motifs.setdefault(i, 0) + 1
        for discord in mp.discover.discords(profile, k = window_size)["discords"]:
            discords[discord] = discords.setdefault(discord, 0) + 1
    top_discords = sorted(discords.items(), key=lambda x:x[1])[0:(k - 1)]
    print(top_discords)
    top_indices = []
    for index, _ in top_discords:
        top_indices.append(index)
    model = LogisticRegressionCV(max_iter=10000,penalty="elasticnet",l1_ratios=[0.5,0.5],solver="saga",n_jobs=-1)
    model.fit(x_train[:,top_indices], y_train)
    y_pred = model.decision_function(x_test[:,top_indices])
    RocCurveDisplay.from_predictions(y_test, y_pred)
    #plt.show()
    #print(motifs)
