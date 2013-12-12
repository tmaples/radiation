import globals

movementData = []

path = globals.projectDirectory + 'usData/'
movementDataFileName = path + 'usMovementData.txt'
outputFileName = path + 'usMovementDataProcessed.csv'

def loadMovementData():
	global movementData
	movementFile = open(movementDataFileName, 'r')
	for line in movementFile:
		processLine(line.split())

def processLine(lineIn):
	lineOut = []

	for x in lineIn:
		if isNumber(x) or x == '*':
			lineOut.append(x)

	if lineIn[-2] == 'MEXICO' or lineIn[-2] == 'CANADA':
		sourceFIPS = lineOut[0] + lineOut[1]
		destFIPS = lineOut[4]
		commuters = lineOut[6]
		movementData.append(','.join([sourceFIPS, destFIPS, commuters]))
	elif len(lineOut) == 9 and int(lineOut[4]) != 15 and int(lineOut[0]) != 15:
		sourceFIPS = lineOut[0] + lineOut[1]
		destFIPS = lineOut[4][1:] + lineOut[5]
		commuters = lineOut[8]
		movementData.append(','.join([sourceFIPS, destFIPS, commuters]))

def isNumber(string):
    try:
        float(string)
        return 1
    except ValueError:
        return 0

loadMovementData()
outFile = open(outputFileName, 'w')
outFile.write('\n'.join(movementData))
outFile.close()