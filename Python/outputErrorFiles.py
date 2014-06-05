from radiation import *
import globals

outputFilePath = globals.projectDirectory + 'error/'

defineModel(['us','alaska'],['us','alaska','mexico','canada'])
calculateRadiusPopulations()
loadCommuters()

def outputError(parameters):
	rows = getRows(dataCompatible=True)
	columns = getColumns(dataCompatible=True)
	
	model = fluxMatrix(dataCompatible=True, parameters=[0.01216617, 0.04228784], round=True)
	data = commuterMatrix()
	error = np.log(data + 1) - np.log(model + 1)
	
	for i in range(len(rows)):
		sourceUid = rows[i]
		output = ['uid,error']
		for j in range(len(columns)):
			destUid = columns[j]
			if sourceUid == destUid or error[i][j] == 0:
				continue
			output.append(','.join([destUid[1:], str(error[i][j])]))
		outputFileName = outputFilePath + sourceUid[1:] + '.csv'
		open(outputFileName, 'w').write('\n'.join(output))

outputError(None)