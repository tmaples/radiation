import csv
import globals

path = globals.projectDirectory + 'usData/'
divisionFileName = path + 'usContiguousDivisionsCommutersToContiguous.csv'
movementFileName = path + 'usMovementDataProcessed.csv'
outputFileName = path + 'dataVsModelUsContiguousToContiguous.csv'

reader = csv.DictReader(open(divisionFileName), delimiter=',', quotechar='"')
divisionUids = [division['uid'] for division in reader]
divisionUids.sort()

movements = {(line.strip().split(',')[0]+line.strip().split(',')[1]):line.strip().split(',')[2] for line in open(movementFileName)}

output = ['source,dest,data,model']
zeros = 0

for source in divisionUids:
	sourceFileName = globals.projectDirectory + 'fluxUsContiguousToUsContiguous/fluxC' + source + '.csv'
	modelFile = {line.strip().split(',')[0]:line.strip().split(',')[1] for line in open(sourceFileName)}
	for dest in divisionUids:
		if source == dest:
			continue

		data = '0'
		model = '0'
		if (source+dest) in movements:
			data = movements[source+dest]
		if dest in modelFile:
			model = modelFile[dest]

		# if data == '0' and model == '0':
		# 	zeros += 1
		# 	continue

		output.append(','.join([source,dest,data,model]))

open(outputFileName, 'w').write('\n'.join(output))
print zeros