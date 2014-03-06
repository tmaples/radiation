import csv
import globals
import math

path = globals.projectDirectory
fluxFileName = path + 'usData/fluxToUsMexicoCanada.csv'
outputFileName = path + 'usData/errorToUsMexicoCanada.csv'

uid = []
usModel = []
usData = []
mexicoModel = []
mexicoData = []
canadaModel = []
canadaData = []

for entry in csv.DictReader(open(fluxFileName)):
	uid.append(entry['uid'])
	usModel.append(int(entry['usModel']))
	usData.append(int(entry['usData']))
	mexicoModel.append(int(entry['mexicoModel']))
	mexicoData.append(int(entry['mexicoData']))
	canadaModel.append(int(entry['canadaModel']))
	canadaData.append(int(entry['canadaData']))

usError = []
mexicoError = []
canadaError = []

for i in range(len(uid)):
	usError.append(math.log10(usData[i] + 1) - math.log10(usModel[i] + 1))
	mexicoError.append(math.log10(mexicoData[i] + 1) - math.log10(mexicoModel[i] + 1))
	canadaError.append(math.log10(canadaData[i] + 1) - math.log10(canadaModel[i] + 1))

maxError = max(abs(max(usError)), abs(min(usError)), abs(max(mexicoError)), abs(min(mexicoError)),abs(max(canadaError)), abs(min(canadaError)))

output = ['uid,usColor,usOpacity,mexicoColor,mexicoOpacity,canadaColor,canadaOpacity']
for i in range(len(uid)):
	positiveColor = 'darkgreen'
	negativeColor = 'darkorange'
	usColor = positiveColor if usError[i] > 0 else negativeColor
	mexicoColor = positiveColor if mexicoError[i] > 0 else negativeColor
	canadaColor = positiveColor if canadaError[i] > 0 else negativeColor
	usOpacity = str(float(abs(usError[i])) / maxError)
	mexicoOpacity = str(float(abs(mexicoError[i])) / maxError)
	canadaOpacity = str(float(abs(canadaError[i])) / maxError)
	output.append(','.join([uid[i],usColor,usOpacity,mexicoColor,mexicoOpacity,canadaColor,canadaOpacity]))

open(outputFileName, 'w').write('\n'.join(output))