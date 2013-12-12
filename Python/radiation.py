import csv
import math
import globals

############ GLOBAL VARIABLES ############

path = globals.projectDirectory
divisionDataFileName = path + 'usData/usDivisionsCommuters.csv'

divisions = {}

################ FUNCTIONS ###############

# Loads divisions from csv file 
def loadDivisions():
	global divisions
	csvFile = open(divisionDataFileName)
	reader = csv.DictReader(csvFile, delimiter=',', quotechar='"')
	divisions = {division['uid']:processDivision(division) for division in reader}
	csvFile.close()

# Returns dictionary representing a division
def processDivision(division):
	return {	
			'uid':division['uid'],
			'name':division['name'],
			'region':division['region'],
			'population':float(division['population']),
			'commuters':float(division['commuters']),
			'latitude':float(division['latitude']),
			'longitude':float(division['longitude'])
			}

# Returns true if divisionOne and divisionTwo have same uid
def equal(divisionOne, divisionTwo):
	return divisionOne['uid'] == divisionTwo['uid']

# Returns distance between divisions i and j in km
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

# Returns total population in all divisions (except i and j) 
# within a circle of radius rij centered at i 
# (rij is the distance between i and j)
def radiusPopulation(i, j):
	global divisions
	radius = distance(i, j)
	population = 0
	for division in divisions.itervalues():
		if equal(division, i) or equal(division, j):
			continue
		if distance(i, division) > radius:
			continue
		population += division['population']
	return population

# Probability that a particle emitted from division i with population m
# is absorbed in division j with population n, given that sij is the total 
# population in all divisions (except i and j) within a circle of radius rij 
# centered at i (rij is the distance between i and j)
def absorptionProbability(i, j):
	mi = i['population']
	nj = j['population']
	sij = radiusPopulation(i, j)
	if (equal(i, j)):
		return 0
	else:
		return (mi*nj) / ((mi+sij)*(mi+nj+sij))

def flux(i, j):
	return i['commuters'] * absorptionProbability(i, j)

# Calculates the absorption probabilities from all divisions
# to all other divisions and writes them to files
def outputAbsorptionProbs():
	for i in divisions.itervalues():
		outputFileName = 'csv/movement' + i['uid'] + '.csv'
		if (os.path.isfile(outputFileName)):
			continue
		output = ['uid,movement']
		for j in divisions.itervalues():
			p = absorptionProbability(i, j)
			output.append(','.join([j['uid'],str(p)]))
		outputFile = open(outputFileName, 'w')
		outputFile.write('\n'.join(output))
		outputFile.close()
		print i['name'] + " Complete."

# Calculates the flux from all divisions
# to all other divisions and writes them to files
def outputFlux():
	for source in divisions:
		outputFileName = path + '/flux/flux' + source + '.csv'
		if (os.path.isfile(outputFileName)):
			continue
		outputFile = open(outputFileName, 'w')
		output = ['uid,movement']
		for dest in divisions:
			if source == dest:
				continue
			model = int(round(flux(divisions[source], divisions[dest])))
			if model > 0:
				output.append(','.join([dest, str(model)]))
		outputFile.write('\n'.join(output))
		outputFile.close()
		print divisions[source]['name'] + " Complete."	

############### MAIN METHOD ##############

loadDivisions()
outputFlux()