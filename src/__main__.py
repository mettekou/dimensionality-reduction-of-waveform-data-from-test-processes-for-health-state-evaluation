import matplotlib.pyplot as plt

from load import load
from clean import clean
from explore import bivariate
from learn import logistic_regression


def main():
    data = clean(load('postgresql://redline:redline@redline:5432/redline'))
    print(logistic_regression(data))
    # bivariate(data)
    # plt.show()
    # print(data[data["Maximum_pressure_hysteresis_current_point"].notna()])


if __name__ == '__main__':
    # execute only if run as the entry point into the program
    main()
