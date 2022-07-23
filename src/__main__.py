import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from load import load, load_waveform_values
from clean import clean
from explore import univariate, bivariate, waveform_heatmap
from logistic_regression import logistic_regression_forward, logistic_regression_lasso
from learn import learning_shapelets
#from pca import pca

def myplot(score,coeff,labels=None):
    xs = score[:,0]
    ys = score[:,1]
    n = coeff.shape[0]
    scalex = 1.0/(xs.max() - xs.min())
    scaley = 1.0/(ys.max() - ys.min())
    plt.scatter(xs * scalex,ys * scaley)
    for i in range(n):
        plt.arrow(0, 0, coeff[i,0], coeff[i,1],color = 'r',alpha = 0.5)
        if labels is None:
            plt.text(coeff[i,0]* 1.15, coeff[i,1] * 1.15, "Var"+str(i+1), color = 'g', ha = 'center', va = 'center')
        else:
            plt.text(coeff[i,0]* 1.15, coeff[i,1] * 1.15, labels[i], color = 'g', ha = 'center', va = 'center')
    plt.xlim(-1,1)
    plt.ylim(-1,1)
    plt.xlabel("PC{}".format(1))
    plt.ylabel("PC{}".format(2))
    plt.grid()

connection_string = 'postgresql://redline:redline@localhost:5432/redline'

def main():
    #plt.rcParams['font.family'] = 'sans-serif'
    #plt.rcParams['font.sans-serif'] = ['UGent Panno Text']
    np.random.seed(42)
    #data = clean(load(connection_string))
    #model_forward = logistic_regression_forward(data)
    #plt.savefig("../report/roc_forward.png",bbox_inches="tight",dpi=300)
    #print(model_forward.summary())
    #model_lasso = logistic_regression_lasso(data)
    #plt.savefig("../report/roc_lasso.png",bbox_inches="tight",dpi=300)
    #print(model_lasso)
    #bivariate(data)
    x, y = load_waveform_values(connection_string)
    #waveform_heatmap(x)
    #plt.savefig("../report/waveform_passed_heatmap.png",bbox_inches='tight',dpi=300)
    rows, columns = np.shape(x)
    learning_shapelets(np.reshape(x, (rows, columns, 1)), y)
    plt.savefig("../report/roc_shapelet_learning.png",bbox_inches='tight',dpi=300)
    #pcs, pca_, labels = pca(data)
    #myplot(pcs[:,0:2],np.transpose(pca_.components_[0:2, :]), labels)
    #print(pca_.explained_variance_)
    #print(pcs)
    #y_score = clf.predict_proba(pd.DataFrame(data.select_dtypes(include=["float64"]).columns))
    #roc_auc_score(data["ok"], y_score)
    #univariate(data)
    # print(data[data["Maximum_pressure_hysteresis_current_point"].notna()])


if __name__ == '__main__':
    main()
