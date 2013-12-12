import xml.etree.ElementTree as ET

census = [{}, {}, {}]

tree = ET.parse('canadaMovement2001.xml')
root = tree.getroot()

dataSet = root.find('{http://www.SDMX.org/resources/SDMXML/schemas/v2_0/message}DataSet')

for series in dataSet.findall('{http://www.SDMX.org/resources/SDMXML/schemas/v2_0/generic}Series'):
	seriesKey = series.find('{http://www.SDMX.org/resources/SDMXML/schemas/v2_0/generic}SeriesKey')
	obs = series.find('{http://www.SDMX.org/resources/SDMXML/schemas/v2_0/generic}Obs')
	
	data = {}

	for value in seriesKey:
		data[value.get('concept')] = value.get('value')
	data['people'] = obs.find('{http://www.SDMX.org/resources/SDMXML/schemas/v2_0/generic}ObsValue').get('value')

	category = census[int(data['DIM0']) - 1]
	category[data['GEO']] = {}
	category[data['GEO']][data['POWGEO']] = data['people']

output = ['res,work,total,male,female']
for x in census[0]:
	for y in census[0][x]:
		line = x + ',' + y + ',' + census[0][x][y] + ',' + census[1][x][y] + ',' + census[2][x][y]
		output.append(line)

outFile = open('canadaMovementSubdivisions.csv','w')
outFile.write('\n'.join(output))
outFile.close()