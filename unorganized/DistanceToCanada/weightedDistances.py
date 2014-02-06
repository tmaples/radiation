import csv
import math

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

us = open('usDivisions.csv')
canada = open('canadaDivisions.csv')

usDivisions = {division['uid']:processDivision(division) for division in csv.DictReader(us, delimiter=',', quotechar='"')}
canadaDivisions = {division['uid']:processDivision(division) for division in csv.DictReader(canada, delimiter=',', quotechar='"')}

output = ['uid,distance']
maxDistance = 0

for usDiv in usDivisions:
	n = 0
	d = 0
	minDistance = float('inf')
	for canDiv in canadaDivisions:
		dist = distance(usDivisions[usDiv], canadaDivisions[canDiv])
		scaledDist = dist * (1 - (canadaDivisions[canDiv]['population'] / 30007094))
		n += dist * canadaDivisions[canDiv]['population']
		d += dist
		if scaledDist < minDistance:
			minDistance = scaledDist
	if minDistance > maxDistance:
		maxDistance = minDistance
	weightedDistance = float(n) / d
	output.append(usDiv + ',' + str(minDistance))

open('minWeightedDistanceToCanada.csv', 'w').write('\n'.join(output))
print maxDistance