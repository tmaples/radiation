from radiation import *
import globals
import numpy as np

outputFileName = globals.projectDirectory + 'usData/errorNew.csv'

defineModel(['us', 'alaska'], ['us', 'alaska', 'canada', 'mexico'])
calculateRadiusPopulations()
loadCommuters()

def outputError(parameters):
	rows = getRows(dataCompatible=True)
	
	model = fluxMatrix(dataCompatible=True, parameters=parameters, round=True)
	model = np.concatenate((np.nansum(model[:,:-2], axis=1)[np.newaxis].T, model[:,-2:]), axis=1)
	data = commuterMatrix()
	data = np.concatenate((np.nansum(data[:,:-2], axis=1)[np.newaxis].T, data[:,-2:]), axis=1)
	error = np.log(data + 1) - np.log(model + 1)
	
	output = ['uid,usError,canError,mexError']
	for i in range(len(rows)):
		uid = rows[i][1:]
		usError = str(error[i][0])
		canError = str(error[i][1])
		mexError = str(error[i][2])
		output.append(','.join([uid, usError, canError, mexError]))
	open(outputFileName, 'w').write('\n'.join(output))

outputError([0.01216617, 0.04228784])