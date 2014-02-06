border = []
nonBorder = []

for line in open('usMovementToCanada.csv'):
	lineSplit = line.strip().split(',')
	if lineSplit[4] == 'border':
		continue
	
	b = int(lineSplit[4])
	if b == 1:
		border.append(lineSplit[1] + ',' + lineSplit[2])
	elif b == 0:
		nonBorder.append(lineSplit[1] + ',' + lineSplit[2])

open('movementToCanadaObservedVsExpectedBorder', 'w').write('\n'.join(border))
open('movementToCanadaObservedVsExpectedNonBorder', 'w').write('\n'.join(nonBorder))