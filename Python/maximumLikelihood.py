import likelihood
from scipy.optimize import minimize

print minimize(likelihood.getLikelihood, [0.5, 0.5], method='L-BFGS-B', bounds=[(1e-10,1), (1e-10,1)])
# print minimize(likelihood.getLikelihood, [1.0], method='Nelder-Mead')