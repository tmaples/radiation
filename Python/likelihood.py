from radiation import *
import numpy as np
import time

defineModel(['us','alaska'],['us','alaska','canada','mexico'])
calculateRadiusPopulations(False)
loadCommuters()

T = commuterMatrix()
Ttot = float(np.sum(T))
Ti = np.sum(T, axis=1)
qi = np.divide(Ti, Ttot)

L = np.sum(np.multiply(Ti, np.log(qi)))

def getLikelihood(parameter):
	p = probabilityMatrix(parameter, True)
	L += np.nansum(np.multiply(T, np.log(p)))
	return L

t = time.time()
print getLikelihood()
print 'TIME: ', time.time() - t