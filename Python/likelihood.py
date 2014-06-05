from radiation import *
import numpy as np
import time

defineModel(['us','alaska'],['us','alaska','canada','mexico'])
calculateRadiusPopulations()
loadCommuters() 

T = commuterMatrix()
Ttot = float(np.sum(T))
Ti = np.sum(T, axis=1)
qi = np.divide(Ti, Ttot)

Lfirst = np.sum(np.multiply(Ti, np.log(qi)))

def getLikelihood(parameters):
	t = time.time()
	p = probabilityMatrix(dataCompatible=True, parameters=parameters, formulation='Power')
	Lsecond = Lfirst + np.nansum(np.multiply(T, np.log(p)))
	print 'PARAMETER:',parameters,'LIKELIHOOD:',-Lsecond,'TIME:', time.time() - t
	return -Lsecond