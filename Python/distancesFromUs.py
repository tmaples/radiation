import csv
import math
import globals

path = globals.projectDirectory
usDivisionFileName = path + 'usData/usDivisions.csv'
canadaDivisionFileName = path + 'canadaData/canadaDivisions.csv'
mexicoDivisionFileName = path + 'mexicoData/mexicoDivisions.csv'
outputFileName = path + 'usData/distanceToMexico.csv'

def processDivision(division):
	return {	
			'uid':division['uid'],
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

us = open(usDivisionFileName)
canada = open(mexicoDivisionFileName)

usDivisions = {division['uid']:processDivision(division) for division in csv.DictReader(us, delimiter=',', quotechar='"')}
canadaDivisions = {division['uid']:processDivision(division) for division in csv.DictReader(canada, delimiter=',', quotechar='"')}

output = ['uid,distance']

uids = usDivisions.keys()
uids.sort()

for usDiv in uids:
	minDistance = float('inf')
	for canDiv in canadaDivisions:
		dist = distance(usDivisions[usDiv], canadaDivisions[canDiv])
		if dist < minDistance:
			minDistance = dist
	output.append(usDiv + ',' + str(minDistance))

open(outputFileName,'w').write('\n'.join(output))