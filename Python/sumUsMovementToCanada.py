import globals
import csv

path = globals.projectDirectory + 'usData/'

movementFileName = path + 'usMovementDataProcessed.csv'
divisionFileName = path + 'usDivisions.csv'
outputFileName = path + 'usMovementToCanada.csv'
borderCountiesFileName = path + 'canadaBorderCounties'

movementData = [line.strip().split(',') for line in open(movementFileName)]
reader = csv.DictReader(open(divisionFileName), delimiter=',', quotechar='"')
divisionUids = [division['uid'] for division in reader]
borderCounties = [line.strip() for line in open(borderCountiesFileName)]

data = {}

for movement in movementData:
	source = movement[0]
	destination = movement[1]
	n = int(movement[2])
	if destination == '301':
		data[source] = n

model = {}
fileNameBase = globals.projectDirectory + 'flux/flux'

for divisionUid in divisionUids:
	fileName = fileNameBase + divisionUid + '.csv'
	lines = [line.strip().split(',') for line in open(fileName)]
	del lines[0]
	movement = 0
	for line in lines:
		if len(line[0]) == 4:
			movement += int(line[1])
	if movement > 0:
		model[divisionUid] = movement

output = ['uid,data,model,error,border']
for uid in divisionUids:
	d = data[uid] if uid in data else 0
	m = model[uid] if uid in model else 0
	
	if d == m:
		error = 0
	elif d > m:
		error = -(d - m) / float(d)
	else:
		error = (m - d) / float(m)
	
	border = '1' if uid in borderCounties else '0'

	output.append(','.join([uid,str(d),str(m),str(round(error,2)),border]))

open(outputFileName, 'w').write('\n'.join(output))