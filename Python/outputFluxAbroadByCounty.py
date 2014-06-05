from radiation import *
import globals
import numpy as np

outputFileName = globals.projectDirectory + 'usData/fluxAbroadByCounty.csv'

defineModel(['us', 'alaska'], ['us', 'alaska', 'canada', 'mexico'])
calculateRadiusPopulations()
loadCommuters()
rows = getRows(dataCompatible=True)
cols = ['C','M']

def output(parameters):
	model1 = fluxMatrix(dataCompatible=True, parameters=parameters, round=True, formulation='Standard')[:,-2:]
	model2 = fluxMatrix(dataCompatible=True, parameters=parameters, round=True, formulation='Power')[:,-2:]
	data = commuterMatrix()[:,-2:]

	output = ['uid']
	for col in cols:
		output[0] += ','+col+'DATA,'+col+'OLD,'+col+'NEW'

	for i in range(len(rows)):
		outputRow = [rows[i]]
		for j in range(len(cols)):
			outputRow += [str(data[i][j]), str(model1[i][j]), str(model2[i][j])]
		output.append(','.join(outputRow))
	open(outputFileName, 'w').write('\n'.join(output))

output([0.01216617, 0.04228784])