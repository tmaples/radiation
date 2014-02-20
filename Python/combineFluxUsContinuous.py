import csv
import globals

path = globals.projectDirectory
divisionFileName = path + 'usData/usContiguousDivisionsCommutersToContiguous.csv'
probFilePath = path + 'probUsContiguousToUsContiguous/prob'
dataFileName = path + 'usData/usMovementDataProcessed.csv'
modelOutputFileName = path + 'usData/probsWithinUsContiguousModel.csv'
dataOutputFileName = path + 'usData/probWithinUsContiguousData.csv'

reader = csv.DictReader(open(divisionFileName), delimiter=',', quotechar='"')
divisionUids = [division['uid'] for division in reader]
divisionUids.sort()

modelOutput = ['source+dest,prob']

for source in divisionUids:
	sourceFileName = probFilePath + source + '.csv'
	sourceFile = [line.strip().split(',') for line in open(sourceFileName)]
	del sourceFile[0]
	for line in sourceFile:
		modelOutput.append(','.join([source+line[0],line[1]]))

dataTemp = [line.strip().split(',') for line in open(dataFileName)]

dataTotal = {}
for source,dest,n in dataTemp:
	if source == dest:
		continue
	if source in dataTotal:
		dataTotal[source] += int(n)
	else:
		dataTotal[source] = int(n)

data = {}
for source,dest,n in dataTemp:
	if source == dest:
		continue
	if source in data:
		data[source][dest] = int(n)
	else:
		data[source] = {}
		data[source][dest] = int(n)

dataOutput = ['source+dest,prob']
for source in data:
	for dest in data[source]:
		if dest == '301' or dest == '303':
			continue
		if source[:2] == '02' or dest[:2] == '02':
			continue
		n = float(data[source][dest]) / dataTotal[source]
		dataOutput.append(','.join([source+dest, str(n)]))

open(modelOutputFileName, 'w').write('\n'.join(modelOutput))
open(dataOutputFileName, 'w').write('\n'.join(dataOutput))