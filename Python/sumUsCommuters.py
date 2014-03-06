import globals
import csv

path = globals.projectDirectory + 'usData/'
divisionFileName = path + 'usDivisions.csv'
movementFileName = path + 'usMovementDataProcessed.csv'
outputFileName = path + 'usCommuters.csv'

movements = [line.strip().split(',') for line in open(movementFileName)]
del movements[0]
divisions = {entry['uid']:entry['population'] for entry in csv.DictReader(open(divisionFileName))}

total = {}

for movement in movements:
	if movement[0] == movement[1]:
		continue
	if movement[0] in total:
		total[movement[0]] += int(movement[2])
	else:
		total[movement[0]] = int(movement[2])

keys = total.keys()
keys.sort()

output = ['uid,population,commuters,ratio']
for key in keys:
	population = int(divisions['U'+key])
	commuters = total[key]
	ratio = float(commuters) / population
	output.append(','.join([key, str(population), str(commuters), str(ratio)]))

open(outputFileName, 'w').write('\n'.join(output))