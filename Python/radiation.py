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
sij = {'U':[], 'C':[], 'M':[]}

masks = {'U':[], 'C':[], 'M':[]}

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
	mi = np.array([divisions[uid]['population'] for uid in sourceUids])[np.newaxis].T
	nj = np.array([divisions[uid]['population'] for uid in destUids])
	
	global masks
	for mask in masks:
		masks[mask] = np.array([uid[0] == mask for uid in destUids])

def calculateRadiusPopulations():
	global sij
	
	for sourceUid in sourceUids:
		dests = []
		for destUid in destUids:
			if sourceUid == destUid:
				continue
			dest = {}
			dest['uid'] = destUid
			dest['distance'] = distance(sourceUid, destUid)
			dest['population'] = divisions[destUid]['population']
			dest['s'] = {'U':0.0, 'C':0.0, 'M':0.0}
			dests.append(dest)
		
		dests.sort(key=lambda x: x['distance'])

		for i in range(1, len(dests)):
			previous = dests[i - 1]
			current = dests[i]

			previousCountry = previous['uid'][0]
			otherCountries = current['s'].keys()
			otherCountries.remove(previousCountry)
			
			current['s'][previousCountry] = previous['s'][previousCountry] + previous['population']
			for otherCountry in otherCountries:
				current['s'][otherCountry] = previous['s'][otherCountry]

		if sourceUid in destUids:
			dest = {}
			dest['uid'] = sourceUid
			dest['s'] = {'U':np.nan, 'C':np.nan, 'M':np.nan}
			dests.append(dest)

		dests.sort(key=lambda x: x['uid'])

		row = {'U':[], 'C':[], 'M':[]}
		for dest in dests:
			for country in row:
				row[country].append(dest['s'][country])

		for country in sij:
			sij[country].append(row[country])

	for country in sij:
		sij[country] = np.array(sij[country])

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

def probabilityMatrix(dataCompatible, parameters):

	# RADIATION MODEL
	# sij = sij['U'] + sij['M'] + sij['C']
	# probs = mi*nj / ((mi+sij)*(mi+nj+sij))
	
	# HAZARD FORMULATION
	# bij = sij['M'] + sij['C']
	# sij = bij + sij['U']
	# gamma = parameters[0]
	# prob = (mi*pow(gamma, bij))*((1.0/(mi+sij))-(pow(gamma,nj)*(1.0/(mi+nj+sij))))
	
	# P_Z AND Q_Z POWER RELATIONSHIP FORMULATION
	gammaC, gammaM = parameters[0], parameters[0]
	gamma = (gammaC * masks['C']) + (gammaM * masks['M']) + masks['U']
	probs = mi * (1.0/(mi + sij['U'] + (gammaC * sij['C']) + (gammaM * sij['M'])) - \
		1.0/(mi + sij['U'] + (gammaC * sij['C']) + (gammaM * sij['M']) + gamma*nj))

	if dataCompatible:
		usProb = probs[:, masks['U']]
		canadaProb = np.nansum(probs[:, masks['C']], axis=1)[np.newaxis].T
		mexicoProb = np.nansum(probs[:, masks['M']], axis=1)[np.newaxis].T
		if 'C' in [uid[0] for uid in destUids] and 'M' in [uid[0] for uid in destUids]:
			probs = np.concatenate((usProb, canadaProb, mexicoProb), axis=1)
		elif 'C' in [uid[0] for uid in destUids]:
			probs = np.concatenate((usProb, canadaProb), axis=1)
		elif 'M' in [uid[0] for uid in destUids]:
			probs = np.concatenate((usProb, mexicoProb), axis=1)

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

def fluxMatrix(dataCompatible, parameters, round):
	Ti = np.sum(commuterMatrix(), axis=1)[np.newaxis].T
	p = probabilityMatrix(dataCompatible, parameters)
	if round:
		return np.round(np.multiply(Ti, p))
	else:
		return np.multiply(Ti, p)

def outputFlux(parameters):
	if not os.path.exists(fluxDirectoryName):
		os.makedirs(fluxDirectoryName)
	rows = getRowsCompatible()
	columns = getColumnsCompatible()
	flux = fluxMatrix(dataCompatible=False, parameters=parameters, round=True)
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