from radiation import *
import numpy as np
import time

defineModel(['us','alaska'],['us','mexico','canada','alaska'])
calculateRadiusPopulations()
loadCommuters()

T = commuterMatrix()
Ttot = float(np.sum(T))
Ti = np.sum(T, axis=1)
qi = np.divide(Ti, Ttot)

Lfirst = np.sum(np.multiply(Ti, np.log(qi)))

def getLikelihood(parameter):
	t = time.time()
	p = probabilityMatrix(dataCompatible=True, parameter=parameter)
	Lsecond = Lfirst + np.nansum(np.multiply(T, np.log(p)))
	print 'PARAMETER:',parameter,'LIKELIHOOD:',-Lsecond,'TIME:', time.time() - t
	return -Lsecond