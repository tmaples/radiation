import csv
import math
import globals

path = globals.projectDirectory
usDivisionFileName = path + 'usData/usContiguousDivisionsCommutersToContiguous.csv'
outputFileName = path + 'usData/distancesWithinUsContiguous.csv'

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

usDivisions = {division['uid']:processDivision(division) for division in csv.DictReader(us, delimiter=',', quotechar='"')}

output = ['source+dest,distance']

uids = usDivisions.keys()
uids.sort()

for source in uids:
	for dest in uids:
		if source == dest:
			continue
		dist = distance(usDivisions[source], usDivisions[dest])
		output.append(source + dest + ',' + str(dist))

open(outputFileName,'w').write('\n'.join(output))