import csv
import globals
import radiation as rad

rad.defineModel(['us'],['us'])
rad.calculateRadiusPopulations()
rad.loadCommuters()

modelMatrix = rad.fluxMatrix(dataCompatible=True)
dataMatrix = rad.commuterMatrix()
rows = rad.getRowsCompatible()
columns = rad.getColumnsCompatible()

path = globals.projectDirectory + 'usData/'
outputFileName = path + 'dataVsModelUsContiguous.csv'

output = ['source,dest,data,model']
zeros = 0

for rowIndex in range(len(rows)):
	for colIndex in range(len(columns)):
		source = rows[rowIndex]
		dest = columns[colIndex]
		if source == dest:
			continue
		data = dataMatrix[rowIndex][colIndex]
		model = modelMatrix[rowIndex][colIndex]
		if data == 0 and model == 0:
			zeros += 1
			continue
		output.append(','.join([source,dest,str(int(data)),str(int(model))]))

open(outputFileName, 'w').write('\n'.join(output))
print zeros