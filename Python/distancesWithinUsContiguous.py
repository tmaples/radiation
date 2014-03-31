import csv
import math
import globals
import radiation as rad

outputFileName = globals.projectDirectory + 'usData/distancesWithinUsContiguous.csv'

rad.defineModel(['us'],['us'])

sources = rad.getRows()
dests = rad.getColumns()

output = ['source,dest,distance']

for source in sources:
	for dest in dests:
		if source == dest:
			continue
		dist = rad.distance(source, dest)
		output.append(','.join([source, dest, str(dist)]))

open(outputFileName,'w').write('\n'.join(output))