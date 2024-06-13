import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Dados exemplo
x = np.array([1, 2, 3, 4, 5])
y = np.array([2, 4, 6, 8, 10])

# Ajuste linear
def linear_model(x, a, b):
    return a * x + b

params, covariance = curve_fit(linear_model, x, y)
a, b = params

# Plot
plt.scatter(x, y, label='Dados')
plt.plot(x, linear_model(x, a, b), label='Ajuste Linear', color='red')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.show()
