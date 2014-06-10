from radiation import *
import globals

outputFilePath = globals.projectDirectory + 'error2/'

defineModel(['us'],['us'])
calculateRadiusPopulations()
loadCommuters()

def outputError(parameter, formulation):
	rows = getRows(dataCompatible=True)
	columns = getColumns(dataCompatible=True)
	
	model = fluxMatrix(dataCompatible=True, parameters=parameter, round=True, formulation=formulation)
	data = commuterMatrix()
	error = np.log(data + 1) - np.log(model + 1)
	
	for i in range(len(rows)):
		sourceUid = rows[i][1:]
		outputFileName = outputFilePath + sourceUid + '.csv'
		output = ['uid,error']
		for j in range(len(columns)):
			destUid = columns[j][1:]
			if sourceUid == destUid or error[i][j] == 0:
				continue
			output.append(','.join([destUid, str(error[i][j])]))
		open(outputFileName, 'w').write('\n'.join(output))

outputError(None, 'Standard')