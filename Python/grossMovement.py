import globals
import csv
import random

path = globals.projectDirectory

usFileName = path + 'usData/usDivisions.csv'
usUids = [entry['uid'] for entry in csv.DictReader(open(usFileName))]
random.shuffle(usUids)

parameterFilePath = path + 'parameters/parameters/parametersU'
outputCountiesFilePath = path + 'parameters/similarCanada/canadaEquivalentUsCounties'
outputFluxFileName = path + 'usData/canadaEquivalentFlux.csv'

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

output = ['uid,usFluxModel,usFluxData,canadaFluxModel,canadaFluxData']

for uid in usUids:
	fluxFileName = fluxFilePath + uid + '.csv'
	fluxFile = [line.strip().split(',') for line in open(fluxFileName)]
	del fluxFile[0]
	otherFluxModel = 0
	for destUid, n in fluxFile:
		if destUid[0] == 'C':
			otherFluxModel += int(n)

	otherFluxData = 0
	for dest in data[uid]:
		if dest == '301':
			otherFluxData += data[uid][dest]

	if (otherFluxData < 20) and (otherFluxModel < 20):
		continue

	parameterFileName = parameterFilePath + uid + '.csv'
	outputCountiesFileName = outputCountiesFilePath + uid + '.csv'

	other = []
	us = []
	parameterFile = csv.DictReader(open(parameterFileName))
	otherPopSum = 0
	otherRadPopSum = 0
	for entry in parameterFile:
		destUid = entry['uid']
		population = int(entry['population'])
		radiusPopulation = int(entry['radiusPopulation'])
		if destUid[0] == 'C':
			otherPopSum += population
			otherRadPopSum += radiusPopulation
			other.append([destUid, population, radiusPopulation])
		elif destUid[0] == 'U' and destUid[1:3] != '02':
			us.append([destUid, population, radiusPopulation])

	otherPopMean = float(otherPopSum) / len(other)
	otherRadPopMean = float(otherRadPopSum) / len(other)

	equivalentCountiesUid = []
	equivalentCountiesPop = []
	equivalentCountiesRadPop = []
	while len(equivalentCountiesUid) < len(other):
		selectedUid = ''
		minDiff = float('inf')
		minPopDiff = float('inf')
		minRadPopDiff = float('inf')
		for usUid, pop, radPop in us:
			meanPop = float(sum(equivalentCountiesPop) + pop) / (len(equivalentCountiesPop) + 1)
			meanRadPop = float(sum(equivalentCountiesRadPop) + radPop) / (len(equivalentCountiesRadPop) + 1)
			popDiff = float(abs(otherPopMean - meanPop)) / otherPopMean
			radPopDiff = float(abs(otherRadPopMean - meanRadPop)) / otherRadPopMean
			
			if popDiff + radPopDiff < minDiff and popDiff <= 0.1 and radPopDiff <= 0.1:
				minDiff = popDiff + radPopDiff
				minPopDiff = popDiff
				minRadPopDiff = radPopDiff
				selectedUid = usUid

		if minPopDiff > 0.1 or minRadPopDiff > 0.1:
			break

		for i in range(len(us)):
			if us[i][0] == selectedUid:
				print len(equivalentCountiesUid)
				equivalentCountiesUid.append(us[i][0])
				equivalentCountiesPop.append(us[i][1])
				equivalentCountiesRadPop.append(us[i][2])
				del us[i]
				break

		print uid
		print 'targetPop', otherPopMean
		print 'meanPop',float(sum(equivalentCountiesPop))/len(equivalentCountiesPop)
		print 'targetRadPop', otherRadPopMean
		print 'meanRadPop',float(sum(equivalentCountiesRadPop))/len(equivalentCountiesRadPop)


	if len(equivalentCountiesUid) < len(other):
		continue

	open(outputCountiesFileName,'w').write('\n'.join(['uid'] + equivalentCountiesUid))

	fluxFileName = fluxFilePath + uid + '.csv'
	fluxFile = [line.strip().split(',') for line in open(fluxFileName)]
	del fluxFile[0]
	usFluxModel = 0
	otherFluxModel = 0
	for destUid, n in fluxFile:
		if destUid in equivalentCountiesUid:
			usFluxModel += int(n)
		elif destUid[0] == 'C':
			otherFluxModel += int(n)

	usFluxData = 0
	otherFluxData = 0
	for dest in data[uid]:
		if ('U'+dest) in equivalentCountiesUid:
			usFluxData += data[uid][dest]
		elif dest == '301':
			otherFluxData += data[uid][dest]

	output.append(','.join([uid, str(usFluxModel), str(usFluxData), str(otherFluxModel), str(otherFluxData)]))

	outFile = open(outputFluxFileName, 'w')
	outFile.write('\n'.join(output))
	outFile.close()
