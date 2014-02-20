import globals
from random import shuffle

path = globals.projectDirectory
uidFileName = path + 'canadaData/canadaUids.csv'
movementFileName = path + 'canadaData/canadaMovementDivisions.csv'
fluxPath = path + 'fluxCanadaToUsAndCanada/fluxC'
outputFileName = path + 'canadaData/20over20modelCombined.csv'

uids = [line.strip() for line in open(uidFileName)]
movementTemp = [line.strip().split(',') for line in open(movementFileName)]
movement = {}
for source,dest,n in movementTemp:
	if source == dest:
		continue
	if source in movement:
		movement[source] += int(n)
	else:
		movement[source] = int(n)

allMovement = []

for source in uids:
	fluxFileName = fluxPath + source + '.csv'
	lines = [line.strip().split(',') for line in open(fluxFileName)]
	del lines[0]

	for dest, n in lines:
		if dest[0] == 'U':
			continue
		n = int(n)
		for i in range(n):
			allMovement.append([source,dest[1:]])

shuffle(allMovement)

sample = {}
for i in range(int(len(allMovement) * 0.20)):
	source, dest = allMovement[i]
	if source+dest in sample:
		sample[source+dest] += 1
	else:
		sample[source+dest] = 1

sampleSources = {}
for key in sample:
	if sample[key] <= 20:
		continue
	source = key[:4]
	dest = key[4:]
	if source in sampleSources:
		sampleSources[source] += sample[key]
	else:
		sampleSources[source] = sample[key]

output = ['source,data,model']
for uid in uids:
	model = 0
	if uid in sampleSources:
		model = sampleSources[uid]
	data = 0
	if uid in movement:
		data = movement[uid]
	output.append(','.join([uid,str(data),str(model)]))

open(outputFileName,'w').write('\n'.join(output))