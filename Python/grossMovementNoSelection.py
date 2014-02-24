import globals
import csv
import random

path = globals.projectDirectory

usFileName = path + 'usData/usDivisions.csv'
usUids = [entry['uid'] for entry in csv.DictReader(open(usFileName))]

outputFluxFileName = path + 'usData/fluxToUsMexicoCanada.csv'

fluxFilePath = path + 'fluxUsToContinent/fluxU'
dataFileName = path + 'usData/usMovementDataProcessed.csv'

data = {}
for line in open(dataFileName):
	source, dest, n = line.strip().split(',')
	n = int(n)
	if source in data:
		data[source][dest] = n
	else:
		data[source] = {}
		data[source][dest] = n

output = ['uid,usFluxModel,usFluxData,mexicoFluxModel,mexicoFluxData,canadaFluxModel,canadaFluxData']

for uid in usUids:
	fluxFileName = fluxFilePath + uid + '.csv'
	fluxFile = [line.strip().split(',') for line in open(fluxFileName)]
	del fluxFile[0]
	usFluxModel, mexicoFluxModel, canadaFluxModel = 0, 0, 0
	for destUid, n in fluxFile:
		if destUid[0] == 'U':
			usFluxModel += int(n)
		elif destUid[0] == 'M':
			mexicoFluxModel += int(n)
		elif destUid[0] == 'C':
			canadaFluxModel += int(n)

	usFluxData, mexicoFluxData, canadaFluxData = 0, 0, 0
	for dest in data[uid]:
		if len(dest) == 5:
			usFluxData += data[uid][dest]
		elif dest == '303':
			mexicoFluxData += data[uid][dest]
		elif dest == '301':
			canadaFluxData += data[uid][dest]

	output.append(','.join([uid, str(usFluxModel), str(usFluxData), str(mexicoFluxModel), str(mexicoFluxData), str(canadaFluxModel), str(canadaFluxData)]))

	outFile = open(outputFluxFileName, 'w')
	outFile.write('\n'.join(output))
	outFile.close()