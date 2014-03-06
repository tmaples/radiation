US contiguous -> US contiguous
US -> Canada + US
US contiguous -> Mexico + US contiguous
US -> US + Canada + Mexico

import csv
import globals

path = globals.projectDirectory + 'usData/'
divisionFileName = path + 'usDivisions.csv'
movementFileName = path + 'usMovementDataProcessed.csv'
outputFileName = path + 'usDivisionsCommutersToContinent.csv'

reader = csv.DictReader(open(divisionFileName), delimiter=',', quotechar='"')
divisionUids = [division['uid'] for division in reader]
divisionFile = [line.strip() for line in open(divisionFileName)]

movements = [line.strip().split(',') for line in open(movementFileName)]
commuters = {}
for movement in movements:
	if movement[0] == movement[1]:
		continue
	if movement[0] not in commuters:
		commuters[movement[0]] = int(movement[2])
	else:
		commuters[movement[0]] += int(movement[2])

output = []

output.append(divisionFile[0] + ',commuters')

for i in range(len(divisionUids)):
	divisionUid = divisionUids[i]

	if divisionUid in commuters:
		output.append(divisionFile[i+1] + ',' + str(commuters[divisionUid]))
	else:
		output.append(divisionFile[i+1] + ',0')

outputFile = open(outputFileName, 'w')
outputFile.write('\n'.join(output))
outputFile.close()