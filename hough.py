from sklearn.datasets import make_regression
from matplotlib import pyplot as plt
from sklearn.linear_model import LinearRegression
import seaborn as sns
from sklearn.model_selection import train_test_split
import generateShape as gs
import polygonManipulation as pm

sns.set()
import numpy as np
data = gs.double_row(0,15,True)
data = pm.rotate(data,45)
# X = np.array([5, 15, 25, 35, 45, 55]).reshape((-1, 1))
# Y = np.array([5, 20, 14, 32, 22, 38])
X = np.array([point.x for point in data]).reshape((-1,1))
Y = np.array([point.y for point in data])

linear_regressor = LinearRegression()  # create object for the class
linear_regressor.fit(X, Y)  # perform linear regression
Y_pred = linear_regressor.predict(X)  # make predictions

plt.scatter(X, Y)
plt.plot(X, Y_pred, c='red')
plt.show()

#
# def mse(y_actual, y_pred):
#     error = 0
#
#     for y, y_prime in zip(y_actual, y_pred):
#         error += (y - y_prime) ** 2
#
#     return error
#
# mse(y, starting_slope * x + starting_intercept
#
#
# def calculate_partial_derivatives(x, y, intercept, slope):
#     partial_derivative_slope = 0
#     partial_derivative_intercept = 0
#     n = len(x)
#     for i in range(n):
#         xi = x[i]
#         yi = y[i]
#     partial_derivative_intercept += - (2 / n) * (yi - ((slope * xi) + intercept))
#     partial_derivative_slope += - (2 / n) * xi * (yi - ((slope * xi) + intercept))
#
#     return partial_derivative_intercept, partial_derivative_slope
#
# learning_rate = 0.01
# iterations = 300
# intercept, slope = train(x, y, learning_rate, iterations, starting_intercept, starting_slope)
# linear_regression_line = [slope * xi + intercept for xi in x]
#
# plt.scatter(x, y)
# plt.plot(x, linear_regression_line, c='red')