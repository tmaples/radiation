from radiation import *
import globals
import numpy as np

outputFileName = globals.projectDirectory + 'usData/fluxByStateLowerGammaM.csv'

defineModel(['us', 'alaska'], ['us', 'alaska', 'canada', 'mexico'])
calculateRadiusPopulations()
loadCommuters()
rows = getRows(dataCompatible=True)
cols = getColumns(dataCompatible=True)

def editMatrix(data):
	rowBoundaries = []
	for i in range(1,len(rows)):
		if rows[i][:3] != rows[i - 1][:3]:
			rowBoundaries.append(i)
		
	colBoundaries = []
	for i in range(1,len(cols)-2):
		if cols[i][:3] != cols[i - 1][:3]:
			colBoundaries.append(i)

	lastB = 0
	output = []
	for rb in rowBoundaries:
		output.append(np.nansum(data[lastB:rb,:], axis=0).tolist())
		lastB = rb
	output.append(np.nansum(data[lastB:,:], axis=0).tolist())

	data = np.array(output)

	output = np.nansum(data[:,0:colBoundaries[0]], axis=1)[np.newaxis].T
	lastB = colBoundaries[0]
	for cb in colBoundaries[1:]:
		output = np.concatenate((output, np.nansum(data[:,lastB:cb], axis=1)[np.newaxis].T), axis=1)
		lastB = cb
	output = np.concatenate((output, np.nansum(data[:,lastB:-2], axis=1)[np.newaxis].T), axis=1)
	output = np.concatenate((output, data[:,-2:-1]), axis=1)
	return np.concatenate((output, data[:,-1:]), axis=1)

def getNewRowsAndColumns():
	newRows = [x[:3] for x in rows]
	newCols = [x[:3] for x in cols[:-2]]
	newRows = list(set(newRows))
	newCols = list(set(newCols))
	newRows.sort()
	newCols.sort()
	newCols += ['C', 'M']
	return newRows, newCols

def output(parameters):
	model1 = editMatrix(fluxMatrix(dataCompatible=True, parameters=parameters, round=True, formulation='Standard'))
	model2 = editMatrix(fluxMatrix(dataCompatible=True, parameters=parameters, round=True, formulation='Power'))
	data = editMatrix(commuterMatrix())

	newRows, newCols = getNewRowsAndColumns()
	output = ['uid']
	for a in newCols:
		output[0] += ','+a+'DATA,'+a+'OLD,'+a+'NEW'

	for i in range(len(newRows)):
		outputRow = [newRows[i]]
		for j in range(len(newCols)):
			outputRow += [str(data[i][j]), str(model1[i][j]), str(model2[i][j])]
		output.append(','.join(outputRow))
	open(outputFileName, 'w').write('\n'.join(output))

output([0.01216617, 0.0417])