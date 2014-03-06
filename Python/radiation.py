import csv
import math
import globals
import numpy

############ GLOBAL VARIABLES ############

path = globals.projectDirectory
divisionFileName = path + 'continentDivisions.csv'
movementFileName = path + 'usData/usMovementDataProcessed.csv'

divisions = {}
sourceUids = []
destUids = []
canada, mexico = False, False

commuters = {}
radiusPopulations = {}

################ FUNCTIONS ###############

def loadDivisionsFromFile():
	global divisions
	divisionFile = open(divisionFileName)
	reader = csv.DictReader(divisionFile)
	divisions = {division['uid']:processDivision(division) for division in reader}
	divisionFile.close()

def processDivision(division):
	return {
			'population':int(division['population']),
			'latitude':float(division['latitude']),
			'longitude':float(division['longitude'])
			}

def loadCommuters():
	global commuters
	movementFile = open(movementFileName)
	for move in csv.DictReader(movementFile):
		sourceUid = 'U' + move['source']
		destUid = move['dest']
		if sourceUid not in sourceUids:
			continue
		if destUid == '301' and canada:
			destUid = 'C'
		elif destUid == '303' and mexico:
			destUid = 'M'
		elif ('U' + destUid) in destUids:
			destUid = 'U' + destUid
		else:
			continue
		n = int(move['n'])
		if sourceUid not in commuters:
			commuters[sourceUid] = {}
		commuters[sourceUid][destUid] = n
	movementFile.close()

def defineModel(sourceFileNames, destFileNames):
	global canada, mexico
	canada = 'canada' in destFileNames
	mexico = 'mexico' in destFileNames
	global sourceUids, destUids
	for sourceFileName in sourceFileNames:
		sourceFileName = path + 'regions/' + sourceFileName
		sourceUids += [line.strip() for line in open(sourceFileName)]
	for destFileName in destFileNames:
		destFileName = path + 'regions/' + destFileName
		destUids += [line.strip() for line in open(destFileName)]
	sourceUids.sort()
	destUids.sort()

def calculateRadiusPopulations():
	global radiusPopulations
	for sourceUid in sourceUids:
		radiusPopulations[sourceUid] = {}
		distances = []
		for destUid in destUids:
			if sourceUid == destUid:
				continue
			distances.append([destUid, distance(sourceUid, destUid)])
		distances.sort(key=lambda x: x[1])
		previousRadPop = 0
		previousPop = 0
		for destUid, _ in distances:
			currentRadPop = previousRadPop + previousPop
			radiusPopulations[sourceUid][destUid] = currentRadPop
			previousRadPop = currentRadPop
			previousPop = divisions[destUid]['population']

def commuterMatrix():
	matrix = []
	for sourceUid in sourceUids:
		row = []
		for destUid in destUids:
			country = destUid[0]
			if country == 'U':
				if sourceUid == destUid:
					row.append(0)
				else:
					row.append(getCommuters(sourceUid, destUid))
		if canada:
			row.append(getCommuters(sourceUid, 'C'))
		if mexico:
			row.append(getCommuters(sourceUid, 'M'))
		matrix.append(row)
	return numpy.array(matrix)

def getCommuters(sourceUid, destUid):
	if sourceUid in commuters and destUid in commuters[sourceUid]:
		return commuters[sourceUid][destUid]
	return 0

def probabilityMatrix(parameters, dataCompatible):
	matrix = []
	for sourceUid in sourceUids:
		mi = divisions[sourceUid]['population']
		row = []
		canadaProb, mexicoProb = 0, 0
		for destUid in destUids:
			prob = numpy.nan
			if sourceUid != destUid:
				nj = divisions[destUid]['population']
				sij = radiusPopulations[sourceUid][destUid]
				prob = float(mi*nj) / ((mi+sij)*(mi+nj+sij))
			if dataCompatible:
				country = destUid[0]
				if country == 'U':
					row.append(prob)
				elif country == 'C':
					canadaProb += prob
				elif country == 'M':
					mexicoProb += prob
			else:
				row.append(prob)
		if dataCompatible:
			if canada:
				row.append(canadaProb)
			if mexico:
				row.append(mexicoProb)
		# Normalize probabilities
		rowSum = numpy.nansum(row)
		for i in range(len(row)):
			row[i] = float(row[i]) / rowSum
		matrix.append(row)
	return numpy.array(matrix)

def distance(sourceUid, destUid):
	source = divisions[sourceUid]
	dest = divisions[destUid]
	earthRadius = 6371
	deltaLat = math.radians(dest['latitude'] - source['latitude'])
	deltaLong = math.radians(dest['longitude'] - source['longitude'])
	sinDeltaLat = math.sin(deltaLat / 2)
	sinDeltaLong = math.sin(deltaLong / 2)
	a = math.pow(sinDeltaLat, 2) + math.pow(sinDeltaLong, 2) * \
		math.cos(math.radians(source['latitude'])) * \
		math.cos(math.radians(dest['latitude']))
	c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
	distance = earthRadius * c
	return distance

################ MAIN ###############

loadDivisionsFromFile()