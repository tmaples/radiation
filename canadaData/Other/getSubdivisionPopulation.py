import urllib2

output = ['name,type,population']
for i in range(0,224):
	index = i*25 + 1
	address="http://www12.statcan.ca/english/census01/products/standard/popdwell/Table-CSD-N.cfm?T=1&SR=%s&S=20&O=A"%index
	html = urllib2.urlopen(address).read()
	table = html.split('12,548,588')[1].split('<table width="100%" cellpadding="0" cellspacing="2">')[0]
	entries = table.split('<tr >')
	for i in range(len(entries)):
		entries[i] = entries[i].replace('>', ' ').replace('<', ' ').split()
	for i in range(1,26):
		endName = entries[i].index('/td')
		name = ' '.join(entries[i][1:endName])
		t = entries[i][entries[i].index('align="center"') + 1]
		pop = entries[i][entries[i].index('align="right"') + 1].replace(',', '')
		output.append(name+','+t+','+pop)

outputFile = open('canadaPop.csv', 'w')
outputFile.write('\n'.join(output))
outputFile.close()