import globals
import csv
import math

def loadDivisions(fileName):
	csvFile = open(fileName)
	reader = csv.DictReader(csvFile, delimiter=',', quotechar='"')
	divisions = {division['uid']:processDivision(division) for division in reader}
	csvFile.close()
	return divisions

def processDivision(division):
	return {	
			'uid':division['uid'],
			'name':division['name'],
			'region':division['region'],
			'population':float(division['population']),
			'latitude':float(division['latitude']),
			'longitude':float(division['longitude'])
			}

def distance(x, y):
	earthRadius = 6371
	deltaLat = math.radians(y['latitude'] - x['latitude'])
	deltaLong = math.radians(y['longitude'] - x['longitude'])
	sinDeltaLat = math.sin(deltaLat / 2)
	sinDeltaLong = math.sin(deltaLong / 2)
	a = math.pow(sinDeltaLat, 2) + math.pow(sinDeltaLong, 2) * \
		math.cos(math.radians(x['latitude'])) * \
		math.cos(math.radians(y['latitude']))
	c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
	distance = earthRadius * c
	return distance

def getAverageDistance(sourceUid, sourceDirectory, regionNames, regionDirectory):
	source = sourceDirectory[sourceUid]
	sumPopTimesDist = 0
	sumPop = 0
	for destUid in regionDirectory:
		dest = regionDirectory[destUid]
		if dest['region'] in regionNames:
			dist = distance(source, dest)
			pop = dest['population']
			sumPopTimesDist += pop * dist
			sumPop += pop
	return float(sumPopTimesDist) / sumPop

path = globals.projectDirectory
mexicoFileName = path + 'mexicoData/mexicoDivisions.csv'
usFileName = path + 'usData/usDivisions.csv'
region1FileName = path + 'usData/centralMexico.txt'
outputFileName = path + 'usData/centralMexicoCounties.csv'
fluxFilePath = path + 'fluxUsToContinent/fluxU'
dataFileName = path + 'usData/usMovementDataProcessed.csv'
outputFluxFileName = path + 'usData/centralMexicoFluxes.csv'

mexico = loadDivisions(mexicoFileName)
us = loadDivisions(usFileName)

sourceDirectory = us
region1Directory = us
region2Directory = mexico
region1Names = [line.strip() for line in open(region1FileName)]
region2Names = ['Mexico']

divisions = []

for sourceUid in sourceDirectory:
	if sourceUid[:2] == '02':
		continue
	distToRegion1 = getAverageDistance(sourceUid, sourceDirectory, region1Names, region1Directory)
	distToRegion2 = getAverageDistance(sourceUid, sourceDirectory, region2Names, region2Directory)
	maxDist = max(distToRegion1, distToRegion2)
	minDist = min(distToRegion1, distToRegion2)
	if (maxDist/minDist) <= 1.1:
		divisions.append(sourceUid)

divisions.sort()
divisions = ['uid'] + divisions

open(outputFileName,'w').write('\n'.join(divisions))

# divisions = [line.strip() for line in open(outputFileName)]

del divisions[0]

fluxes = {}
for uid in divisions:
	fluxes[uid] = {}
	fluxFileName = fluxFilePath + uid + '.csv'
	fluxFile = [line.strip().split(',') for line in open(fluxFileName)]
	del fluxFile[0]
	region1Flux = 0
	region2Flux = 0
	for dest, n in fluxFile:
		destUid = dest[1:]
		if dest[0] == 'U':
			region = region1Directory[destUid]['region']
			if region in region1Names:
				region1Flux += int(n)
		elif dest[0] == 'M':
			region = region2Directory[dest]['region']
			if region in region2Names:
				region2Flux += int(n)
	fluxes[uid]['region1Model'] = str(region1Flux)
	fluxes[uid]['region2Model'] = str(region2Flux)

data = {}
for line in open(dataFileName):
	source, dest, n = line.strip().split(',')
	n = int(n)
	if source in data:
		data[source][dest] = n
	else:
		data[source] = {}
		data[source][dest] = n

for uid in divisions:
	region1Flux = 0
	region2Flux = 0
	for dest in data[uid]:
		if len(dest) == 5:
			region = region1Directory[dest]['region']
			if region in region1Names:
				region1Flux += data[uid][dest]
		elif dest == '303':
			region2Flux += data[uid][dest]
	fluxes[uid]['region1Data'] = str(region1Flux)
	fluxes[uid]['region2Data'] = str(region2Flux)

output = ['uid,region1Model,region1Data,region2Model,region2Data']
for uid in divisions:
	output.append(','.join([uid, fluxes[uid]['region1Model'], fluxes[uid]['region1Data'], fluxes[uid]['region2Model'], fluxes[uid]['region2Data']]))

open(outputFluxFileName,'w').write('\n'.join(output))