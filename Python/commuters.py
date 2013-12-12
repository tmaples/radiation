import csv

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

csvFile = open('usaData/usaDivisions2000.csv')
reader = csv.DictReader(csvFile, delimiter=',', quotechar='"')
divisions = {division['uid']:processDivision(division) for division in reader}
csvFile.close()

lines = [line.strip().split(',') for line in open('movementDataProcessed2000')]
commuters = {}
for line in lines:
	if line[1] == '303':
		continue
	if line[0] == line[1]:
		continue
	if line[0] not in commuters:
		commuters[line[0]] = int(line[2])
	else:
		commuters[line[0]] += int(line[2])

output = []
for source in divisions:
	if source in commuters:
		output.append(','.join([source, str(commuters[source])]))
	else:
		output.append(','.join([source, '0']))

outputFile = open('commutersToUSAandCanadaFullData.csv', 'w')
outputFile.write('\n'.join(output))
outputFile.close()