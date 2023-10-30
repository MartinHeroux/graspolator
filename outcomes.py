import statsmodels.api as sm
import numpy as np


def regression(actual, perceived):
    actual = sm.add_constant(actual)
    model = sm.OLS(perceived, actual).fit()
    r_squared = model.rsquared
    intercept, slope = model.params
    return r_squared, intercept, slope


def mean_abs_error(actual, perceived):
    abs_error = list()
    for actual_value, perceived_value in zip(actual, perceived):
        abs_error.append(abs(perceived_value - actual_value))
    return np.mean(abs_error)
