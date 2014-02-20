import globals
import csv

path = globals.projectDirectory + 'usData/'

movementFileName = path + 'usMovementDataProcessed.csv'
divisionFileName = path + 'usDivisions.csv'
outputFileName = path + 'usMovementToCanadaAndMexico.csv'

# canadaBorderCountiesFileName = path + 'canadaBorderCounties'
# canadaBorderCounties = [line.strip() for line in open(canadaBorderCountiesFileName)]
# mexicoBorderCountiesFileName = path + 'mexicoBorderCounties'
# mexicoBorderCounties = [line.strip() for line in open(mexicoBorderCountiesFileName)]

movementData = [line.strip().split(',') for line in open(movementFileName)]

reader = csv.DictReader(open(divisionFileName), delimiter=',', quotechar='"')
uids = [division['uid'] for division in reader]
uids.sort()

canadaData = {}
mexicoData = {}

for movement in movementData:
	source = movement[0]
	dest = movement[1]
	n = int(movement[2])
	if dest == '301':
		canadaData[source] = n
	if dest == '303':
		mexicoData[source] = n

canadaModel = {}
mexicoModel = {}

fileNameBase = globals.projectDirectory + 'fluxUsToContinent/fluxU'

for uid in uids:
	fileName = fileNameBase + uid + '.csv'
	lines = [line.strip().split(',') for line in open(fileName)]
	del lines[0]
	
	canadaMovement = 0
	mexicoMovement = 0
	
	for line in lines:
		if line[0][0] == 'C':
			canadaMovement += int(line[1])
		if line[0][0] == 'M':
			mexicoMovement += int(line[1])
	
	canadaModel[uid] = canadaMovement
	mexicoModel[uid] = mexicoMovement

output = ['source,dest,data,model']

for uid in uids:
	cd = canadaData[uid] if uid in canadaData else 0
	cm = canadaModel[uid]
	md = mexicoData[uid] if uid in mexicoData else 0
	mm = mexicoModel[uid]

	output.append(','.join([uid,'Canada',str(cd),str(cm)]))
	output.append(','.join([uid,'Mexico',str(md),str(mm)]))

open(outputFileName, 'w').write('\n'.join(output))