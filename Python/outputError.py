from radiation import *
from scipy.stats.stats import pearsonr
import globals

outputFileName = globals.projectDirectory + 'error/correlations.csv'

defineModel(['us'],['us'])
calculateRadiusPopulations()
loadCommuters()

def outputError(parameter):
	rows = getRows(dataCompatible=True)
	columns = getColumns(dataCompatible=True)
	
	model = fluxMatrix(dataCompatible=True, parameter=parameter, round=False)
	data = commuterMatrix()
	error = np.log(data + 1) - np.log(model + 1)
	distance = distanceMatrix()
	output = ['source,cor,p-value']
	
	for i in range(len(rows)):
		sourceUid = rows[i]
		errorList = []
		distanceList = []
		for j in range(len(columns)):
			destUid = columns[j]
			if sourceUid == destUid:
				continue
			errorList.append(error[i][j])
			distanceList.append(distance[i][j])
		cor, p = pearsonr(errorList, distanceList)
		output.append(','.join([sourceUid, str(cor), str(p)]))
	open(outputFileName, 'w').write('\n'.join(output))

outputError(None)