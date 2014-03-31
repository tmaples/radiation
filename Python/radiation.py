import csv
import math
import globals
import numpy as np
import os

############ GLOBAL VARIABLES ############

path = globals.projectDirectory
divisionFileName = path + 'continentDivisions.csv'
movementFileName = path + 'usData/usMovementDataProcessed.csv'
fluxDirectoryName = path + 'flux/'

divisions = {}
sourceUids = []
destUids = []

commuters = {}

mi = np.array([])
nj = np.array([])
aij = np.array([])
bij = np.array([])

uij = np.array([])
cij = np.array([])
mij = np.array([])

################ FUNCTIONS ###############

def loadDivisionsFromFile():
	global divisions
	divisionFile = open(divisionFileName)
	reader = csv.DictReader(divisionFile)
	divisions = {division['uid']:processDivision(division) for division in reader}
	divisionFile.close()

def processDivision(division):
	return {
			'population':float(division['population']),
			'latitude':float(division['latitude']),
			'longitude':float(division['longitude'])
			}

def loadCommuters():
	global commuters
	movementFile = open(movementFileName)
	for move in csv.DictReader(movementFile):
		sourceUid = 'U' + move['source']
		destUid = move['dest']
		if destUid == '301':
			destUid = 'C'
		elif destUid == '303':
			destUid = 'M'
		else:
			destUid = 'U' + destUid
		n = int(move['n'])
		if sourceUid not in commuters:
			commuters[sourceUid] = {}
		commuters[sourceUid][destUid] = n
	movementFile.close()

def getRows(dataCompatible):
	return sourceUids

def getColumns(dataCompatible):
	if dataCompatible:
		columns = []
		for destUid in destUids:
			country = destUid[0]
			if country == 'U':
				columns.append(destUid)
		if 'C' in [uid[0] for uid in destUids]:
			columns.append('C')
		if 'M' in [uid[0] for uid in destUids]:
			columns.append('M')
		return columns
	else:
		return destUids

def defineModel(sourceFileNames, destFileNames):
	global sourceUids, destUids
	for sourceFileName in sourceFileNames:
		sourceFileName = path + 'regions/' + sourceFileName
		sourceUids += [line.strip() for line in open(sourceFileName)]
	for destFileName in destFileNames:
		destFileName = path + 'regions/' + destFileName
		destUids += [line.strip() for line in open(destFileName)]
	sourceUids.sort()
	destUids.sort()
	
	global mi, nj
	miList, njList = [], []
	for sourceUid in sourceUids:
		miList.append(divisions[sourceUid]['population'])
	for destUid in destUids:
		njList.append(divisions[destUid]['population'])
	mi = np.array(miList)[np.newaxis].T
	nj = np.array(njList)

def calculateRadiusPopulations():
	global aij, bij
	aijMatrix = []
	bijMatrix = []
	
	for sourceUid in sourceUids:
		aijRow = []
		bijRow = []

		dests = []
		for destUid in destUids:
			if sourceUid == destUid:
				continue
			dest = {}
			dest['uid'] = destUid
			dest['distance'] = distance(sourceUid, destUid)
			dest['population'] = divisions[destUid]['population']
			dest['a'] = 0.0
			dest['b'] = 0.0
			dests.append(dest)
		
		dests.sort(key=lambda x: x['distance'])

		for i in range(1, len(dests)):
			previous = dests[i - 1]
			current = dests[i]

			previousCountry = previous['uid'][0]
			
			if previousCountry == 'U':
				current['a'] = previous['a'] + previous['population']
				current['b'] = previous['b']
			else:
				current['a'] = previous['a']
				current['b'] = previous['b'] + previous['population']

		if sourceUid in destUids:
			dest = {}
			dest['uid'] = sourceUid
			dest['a'] = np.nan
			dest['b'] = np.nan
			dests.append(dest)

		dests.sort(key=lambda x: x['uid'])

		for dest in dests:
			aijRow.append(dest['a'])
			bijRow.append(dest['b'])

		aijMatrix.append(aijRow)
		bijMatrix.append(bijRow)

	aij = np.array(aijMatrix)
	bij = np.array(bijMatrix)

def calculateRadiusPopulations2():
	global uij, cij, mij
	uijMatrix = []
	cijMatrix = []
	mijMatrix = []
	
	for sourceUid in sourceUids:
		uijRow = []
		cijRow = []
		mijRow = []

		dests = []
		for destUid in destUids:
			if sourceUid == destUid:
				continue
			dest = {}
			dest['uid'] = destUid
			dest['distance'] = distance(sourceUid, destUid)
			dest['population'] = divisions[destUid]['population']
			dest['u'] = 0.0
			dest['c'] = 0.0
			dest['m'] = 0.0

			dests.append(dest)
		
		dests.sort(key=lambda x: x['distance'])

		for i in range(1, len(dests)):
			previous = dests[i - 1]
			current = dests[i]

			previousCountry = previous['uid'][0]
			
			if previousCountry == 'U':
				current['u'] = previous['u'] + previous['population']
				current['c'] = previous['c']
				current['m'] = previous['m']
			elif previousCountry == 'C':
				current['c'] = previous['c'] + previous['population']
				current['u'] = previous['u']
				current['m'] = previous['m']
			else:
				current['m'] = previous['m'] + previous['population']
				current['c'] = previous['c']
				current['u'] = previous['u']

		if sourceUid in destUids:
			dest = {}
			dest['uid'] = sourceUid
			dest['u'] = np.nan
			dest['c'] = np.nan
			dest['m'] = np.nan
			dests.append(dest)

		dests.sort(key=lambda x: x['uid'])

		for dest in dests:
			uijRow.append(dest['u'])
			cijRow.append(dest['c'])
			mijRow.append(dest['m'])

		uijMatrix.append(uijRow)
		cijMatrix.append(cijRow)
		mijMatrix.append(mijRow)

	uij = np.array(uijMatrix)
	cij = np.array(cijMatrix)
	mij = np.array(mijMatrix)

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
		if 'C' in [uid[0] for uid in destUids]:
			row.append(getCommuters(sourceUid, 'C'))
		if 'M' in [uid[0] for uid in destUids]:
			row.append(getCommuters(sourceUid, 'M'))
		matrix.append(row)
	return np.array(matrix)

def getCommuters(sourceUid, destUid):
	if sourceUid in commuters and destUid in commuters[sourceUid]:
		return commuters[sourceUid][destUid]
	return 0

def probabilityMatrix(dataCompatible, parameter):

	# RADIATION MODEL
	sij = aij + bij
	probs = mi*nj / ((mi+sij)*(mi+nj+sij))
	
	# HAZARD FORMULATION
	# prob = (mi*pow(parameter, bij))*((1.0/(mi+sij))-(pow(parameter,nj)*(1.0/(mi+nj+sij))))
	
	# P_Z AND Q_Z POWER RELATIONSHIP FORMULATION
	# gamma = parameter
	# probs = mi*(1.0/(mi + aij + gamma*bij) - 1.0/(mi + aij + gamma*bij + gamma*nj))

	if dataCompatible:
		countries = [i[0] for i in destUids]
		canadaIndex = countries.index('C') if 'C' in countries else -1
		mexicoIndex = countries.index('M') if 'M' in countries else -1
		usIndex = countries.index('U') if 'U' in countries else -1

		usProb = probs[:,usIndex:]

		if canadaIndex > -1 and mexicoIndex > -1:
			canadaProb = np.nansum(probs[:,:mexicoIndex], axis=1)[np.newaxis].T
			mexicoProb = np.nansum(probs[:,mexicoIndex:usIndex], axis=1)[np.newaxis].T
			probs = np.concatenate((usProb,canadaProb,mexicoProb), axis=1)
		elif canadaIndex > -1:
			canadaProb = np.nansum(probs[:,canadaIndex:usIndex], axis=1)[np.newaxis].T
			probs = np.concatenate((usProb,canadaProb), axis=1)
		elif mexicoIndex > -1:
			mexicoProb = np.nansum(probs[:,mexicoIndex:usIndex], axis=1)[np.newaxis].T
			probs = np.concatenate((usProb,mexicoProb), axis=1)

	# Normalize probabilities
	rowSums  = np.nansum(probs, axis=1)[np.newaxis].T
	probs = probs / rowSums

	return probs

def probabilityMatrix2(dataCompatible, parameters):

	# RADIATION MODEL
	# sij = aij + bij
	# probs = mi*nj / ((mi+sij)*(mi+nj+sij))
	
	# HAZARD FORMULATION
	# prob = (mi*pow(parameter, bij))*((1.0/(mi+sij))-(pow(parameter,nj)*(1.0/(mi+nj+sij))))
	
	# P_Z AND Q_Z POWER RELATIONSHIP FORMULATION
	gammaC, gammaM = parameters
	probs = mi*(1.0/(mi + uij + gammaC*cij + gammaM*mij) - 1.0/(mi + uij + gammaC*cij + gammaM*mij + ((gammaC+gammaM)/2)*nj))

	if dataCompatible:
		countries = [i[0] for i in destUids]
		canadaIndex = countries.index('C') if 'C' in countries else -1
		mexicoIndex = countries.index('M') if 'M' in countries else -1
		usIndex = countries.index('U') if 'U' in countries else -1

		usProb = probs[:,usIndex:]

		if canadaIndex > -1 and mexicoIndex > -1:
			canadaProb = np.nansum(probs[:,:mexicoIndex], axis=1)[np.newaxis].T
			mexicoProb = np.nansum(probs[:,mexicoIndex:usIndex], axis=1)[np.newaxis].T
			probs = np.concatenate((usProb,canadaProb,mexicoProb), axis=1)
		elif canadaIndex > -1:
			canadaProb = np.nansum(probs[:,canadaIndex:usIndex], axis=1)[np.newaxis].T
			probs = np.concatenate((usProb,canadaProb), axis=1)
		elif mexicoIndex > -1:
			mexicoProb = np.nansum(probs[:,mexicoIndex:usIndex], axis=1)[np.newaxis].T
			probs = np.concatenate((usProb,mexicoProb), axis=1)

	# Normalize probabilities
	rowSums  = np.nansum(probs, axis=1)[np.newaxis].T
	probs = probs / rowSums

	return probs

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

def distanceMatrix():
	matrix = []
	for sourceUid in sourceUids:
		row = []
		for destUid in destUids:
			row.append(distance(sourceUid, destUid))
		matrix.append(row)
	return np.array(matrix)

def fluxMatrix(dataCompatible, parameter, round):
	Ti = np.sum(commuterMatrix(), axis=1)[np.newaxis].T
	p = probabilityMatrix(dataCompatible, parameter)
	if round:
		return np.round(np.multiply(Ti, p))
	else:
		return np.multiply(Ti, p)

def outputFlux(parameter):
	if not os.path.exists(fluxDirectoryName):
		os.makedirs(fluxDirectoryName)
	rows = getRowsCompatible()
	columns = getColumnsCompatible()
	flux = fluxMatrix(dataCompatible=False, parameter=parameter, round=True)
	for i in range(len(rows)):
		sourceUid = rows[i][1:]
		output = ['uid,movement']
		for j in range(len(columns)):
			country = columns[j][0]
			if country != 'U':
				continue
			n = flux[i][j]
			if not np.isnan(n) and n != 0:
				destUid = columns[j][1:]
				output.append(','.join([destUid, str(int(n))]))
		outputFileName = fluxDirectoryName + sourceUid + '.csv'
		open(outputFileName, 'w').write('\n'.join(output))

################ MAIN ###############

loadDivisionsFromFile()