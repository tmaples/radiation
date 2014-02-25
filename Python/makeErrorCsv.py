import csv
import globals
import math

path = globals.projectDirectory
fluxFileName = path + 'usData/fluxToUsMexicoCanada.csv'
outputFileName = path + 'figures & graphics/continent/error.csv'

uid = []
usFluxModel = []
usFluxData = []
mexicoFluxModel = []
mexicoFluxData = []
canadaFluxModel = []
canadaFluxData = []

for entry in csv.DictReader(open(fluxFileName)):
	uid.append(entry['uid'])
	usFluxModel.append(int(entry['usFluxModel']))
	usFluxData.append(int(entry['usFluxData']))
	mexicoFluxModel.append(int(entry['mexicoFluxModel']))
	mexicoFluxData.append(int(entry['mexicoFluxData']))
	canadaFluxModel.append(int(entry['canadaFluxModel']))
	canadaFluxData.append(int(entry['canadaFluxData']))

usError = []
mexicoError = []
canadaError = []

for i in range(len(uid)):
	usError.append(math.log10(usFluxData[i] + 1) - math.log10(usFluxModel[i] + 1))
	mexicoError.append(math.log10(mexicoFluxData[i] + 1) - math.log10(mexicoFluxModel[i] + 1))
	canadaError.append(math.log10(canadaFluxData[i] + 1) - math.log10(canadaFluxModel[i] + 1))

maxError = max(abs(max(usError)), abs(min(usError)), abs(max(mexicoError)), abs(min(mexicoError)),abs(max(canadaError)), abs(min(canadaError)))

output = ['uid,usColor,usOpacity,mexicoColor,mexicoOpacity,canadaColor,canadaOpacity']
for i in range(len(uid)):
	usColor = 'green' if usError[i] > 0 else 'blue'
	mexicoColor = 'green' if mexicoError[i] > 0 else 'blue'
	canadaColor = 'green' if canadaError[i] > 0 else 'blue'
	usOpacity = str(float(abs(usError[i])) / maxError)
	mexicoOpacity = str(float(abs(mexicoError[i])) / maxError)
	canadaOpacity = str(float(abs(canadaError[i])) / maxError)
	output.append(','.join([uid[i],usColor,usOpacity,mexicoColor,mexicoOpacity,canadaColor,canadaOpacity]))

open(outputFileName, 'w').write('\n'.join(output))